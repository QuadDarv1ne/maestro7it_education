/*
Пакет main предоставляет утилиту для шифрования/дешифрования файлов 
с использованием AES-256 и PBKDF2 для генерации ключа.
*/
package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"crypto/sha256"
	"flag"
	"fmt"
	"os"
	"golang.org/x/crypto/pbkdf2"
)

func main() {
	filePtr := flag.String("file", "", "Path to file")
	passPtr := flag.String("password", "", "Encryption password")
	modePtr := flag.String("mode", "encrypt", "Mode: encrypt/decrypt")
	flag.Parse()

	// Валидация входных параметров
	if *filePtr == "" || *passPtr == "" {
		fmt.Println("Error: missing required parameters")
		flag.Usage()
		return
	}

	// Генерация соли
	salt := make([]byte, 8)
	if _, err := rand.Read(salt); err != nil {
		fmt.Println("Error generating salt:", err)
		return
	}

	// Генерация ключа
	key := pbkdf2.Key([]byte(*passPtr), salt, 4096, 32, sha256.New)

	// Чтение файла
	data, err := os.ReadFile(*filePtr)
	if err != nil {
		fmt.Println("Error reading file:", err)
		return
	}

	switch *modePtr {
	case "encrypt":
		encrypted, err := encrypt(data, key)
		if err != nil {
			fmt.Println("Encryption error:", err)
			return
		}
		if err := os.WriteFile(*filePtr+".enc", append(salt, encrypted...), 0644); err != nil {
			fmt.Println("Error writing encrypted file:", err)
		}

	case "decrypt":
		if len(data) < 8 {
			fmt.Println("Error: file too short for decryption")
			return
		}
		salt = data[:8]
		decrypted, err := decrypt(data[8:], key)
		if err != nil {
			fmt.Println("Decryption error:", err)
			return
		}
		if err := os.WriteFile(*filePtr+".dec", decrypted, 0644); err != nil {
			fmt.Println("Error writing decrypted file:", err)
		}

	default:
		fmt.Println("Error: invalid mode. Use 'encrypt' or 'decrypt'")
	}
}

func encrypt(data, key []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return nil, err
	}

	nonce := make([]byte, gcm.NonceSize())
	if _, err := rand.Read(nonce); err != nil {
		return nil, err
	}

	return gcm.Seal(nonce, nonce, data, nil), nil
}

func decrypt(data, key []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return nil, err
	}

	nonceSize := gcm.NonceSize()
	if len(data) < nonceSize {
		return nil, fmt.Errorf("ciphertext too short")
	}

	nonce, ciphertext := data[:nonceSize], data[nonceSize:]
	return gcm.Open(nil, nonce, ciphertext, nil)
}