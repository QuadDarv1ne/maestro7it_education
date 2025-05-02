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
	"encoding/hex"
	"flag"
	"fmt"
	"io"
	"os"
	"golang.org/x/crypto/pbkdf2"
)

// main обрабатывает флаги командной строки и запускает шифрование/дешифрование.
func main() {
	filePtr := flag.String("file", "", "Path to file")
	passPtr := flag.String("password", "", "Encryption password")
	modePtr := flag.String("mode", "encrypt", "Mode: encrypt/decrypt")
	flag.Parse()

	salt := make([]byte, 8)
	rand.Read(salt)
	key := pbkdf2.Key([]byte(*passPtr), salt, 4096, 32, sha256.New)

	data, _ := os.ReadFile(*filePtr)

	switch *modePtr {
	case "encrypt":
		encrypted := encrypt(data, key)
		os.WriteFile(*filePtr+".enc", append(salt, encrypted...), 0644)
	case "decrypt":
		salt = data[:8]
		decrypted := decrypt(data[8:], key)
		os.WriteFile(*filePtr+".dec", decrypted, 0644)
	}
}

// encrypt шифрует данные с использованием AES-GCM. 
// Возвращает результат в формате [nonce + ciphertext].
func encrypt(data, key []byte) []byte {
	block, _ := aes.NewCipher(key)
	gcm, _ := cipher.NewGCM(block)
	nonce := make([]byte, gcm.NonceSize())
	rand.Read(nonce)
	return gcm.Seal(nonce, nonce, data, nil)
}

// decrypt расшифровывает данные, зашифрованные через encrypt().
func decrypt(data, key []byte) []byte {
	block, _ := aes.NewCipher(key)
	gcm, _ := cipher.NewGCM(block)
	nonce, ciphertext := data[:gcm.NonceSize()], data[gcm.NonceSize():]
	plaintext, _ := gcm.Open(nil, nonce, ciphertext, nil)
	return plaintext
}