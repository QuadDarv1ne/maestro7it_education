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
	"runtime"
	"strings"
	
	"golang.org/x/crypto/pbkdf2"
)

func main() {
	filePtr := flag.String("file", "", "Path to file")
	passPtr := flag.String("password", "", "Encryption password")
	modePtr := flag.String("mode", "encrypt", "Mode: encrypt/decrypt")
	flag.Parse()

	// Валидация параметров
	if *filePtr == "" || *passPtr == "" {
		fmt.Println("Error: missing required parameters")
		flag.Usage()
		return
	}

	// Проверка существования файла
	if _, err := os.Stat(*filePtr); os.IsNotExist(err) {
		fmt.Printf("Error: file '%s' does not exist\n", *filePtr)
		return
	}

	// Нормализация режима
	*modePtr = strings.ToLower(*modePtr)

	// Чтение файла
	data, err := os.ReadFile(*filePtr)
	if err != nil {
		fmt.Printf("Error reading file: %v\n", err)
		return
	}

	var result []byte
	switch *modePtr {
	case "encrypt":
		// Генерация соли
		salt := make([]byte, 8)
		if _, err := rand.Read(salt); err != nil {
			fmt.Printf("Error generating salt: %v\n", err)
			return
		}

		// Генерация ключа
		key := pbkdf2.Key([]byte(*passPtr), salt, 4096, 32, sha256.New)
		defer clear(key)

		// Шифрование
		encrypted, err := encrypt(data, key)
		if err != nil {
			fmt.Printf("Encryption error: %v\n", err)
			return
		}

		result = append(salt, encrypted...)
		outputFile := *filePtr + ".enc"
		if err := os.WriteFile(outputFile, result, 0600); err != nil {
			fmt.Printf("Error writing file: %v\n", err)
			return
		}

		fmt.Printf("Success: encrypted. Output: %s\n", outputFile)

	case "decrypt":
		// Проверка минимальной длины
		if len(data) < 8 {
			fmt.Println("Error: file too short for decryption")
			return
		}

		// Извлечение соли и данных
		salt := data[:8]
		ciphertext := data[8:]
		if len(ciphertext) == 0 {
			fmt.Println("Error: no encrypted data found")
			return
		}

		// Генерация ключа
		key := pbkdf2.Key([]byte(*passPtr), salt, 4096, 32, sha256.New)
		defer clear(key)

		// Дешифрование
		decrypted, err := decrypt(ciphertext, key)
		if err != nil {
			fmt.Printf("Decryption error: %v\n", err)
			return
		}

		result = decrypted
		outputFile := *filePtr + ".dec"
		if err := os.WriteFile(outputFile, result, 0600); err != nil {
			fmt.Printf("Error writing file: %v\n", err)
			return
		}

		fmt.Printf("Success: decrypted. Output: %s\n", outputFile)

	default:
		fmt.Println("Error: invalid mode. Use 'encrypt' or 'decrypt'")
		return
	}

	// Запись результата
	outputFile := *filePtr + "." + *modePtr
	if err := os.WriteFile(outputFile, result, 0600); err != nil {
		fmt.Printf("Error writing file: %v\n", err)
		return
	}

	fmt.Printf("Success: %s completed\nOutput file: %s\n", 
		*modePtr, 
		outputFile,
	)
}

func clear(b []byte) {
	for i := range b {
		b[i] = 0
	}
	runtime.KeepAlive(b)
}

func encrypt(data, key []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, fmt.Errorf("cipher creation failed: %w", err)
	}

	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return nil, fmt.Errorf("GCM initialization failed: %w", err)
	}

	nonce := make([]byte, gcm.NonceSize())
	if _, err := rand.Read(nonce); err != nil {
		return nil, fmt.Errorf("nonce generation failed: %w", err)
	}

	return gcm.Seal(nonce, nonce, data, nil), nil
}

func decrypt(data, key []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, fmt.Errorf("cipher creation failed: %w", err)
	}

	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return nil, fmt.Errorf("GCM initialization failed: %w", err)
	}

	if len(data) < gcm.NonceSize() {
		return nil, fmt.Errorf("ciphertext too short")
	}

	nonce, ciphertext := data[:gcm.NonceSize()], data[gcm.NonceSize():]
	return gcm.Open(nil, nonce, ciphertext, nil)
}