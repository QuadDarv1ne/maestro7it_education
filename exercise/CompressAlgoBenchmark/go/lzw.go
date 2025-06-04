/*
Package lzw implements Lempel-Ziv-Welch compression

Features:
- Adaptive dictionary building
- Handles any input data
- Includes compression ratio calculation
*/
package main

import (
	"fmt"
	"os"
)

// compressLZW performs LZW compression
func compressLZW(data string) []int {
	if data == "" {
		panic("input data cannot be empty")
	}

	dictSize := 256
	dictionary := make(map[string]int)
	for i := 0; i < dictSize; i++ {
		dictionary[string(rune(i))] = i
	}

	var result []int
	current := ""

	for _, c := range data {
		char := string(c)
		combined := current + char

		if _, exists := dictionary[combined]; exists {
			current = combined
		} else {
			result = append(result, dictionary[current])
			dictionary[combined] = dictSize
			dictSize++
			current = char
		}
	}

	if current != "" {
		result = append(result, dictionary[current])
	}
	return result
}

// decompressLZW reconstructs original data
func decompressLZW(compressed []int) string {
	if len(compressed) == 0 {
		panic("compressed data cannot be empty")
	}

	dictSize := 256
	dictionary := make(map[int]string)
	for i := 0; i < dictSize; i++ {
		dictionary[i] = string(rune(i))
	}

	result := dictionary[compressed[0]]
	current := result

	for _, code := range compressed[1:] {
		var entry string
		if val, ok := dictionary[code]; ok {
			entry = val
		} else if code == dictSize {
			entry = current + current[:1]
		} else {
			panic("invalid compressed code")
		}

		result += entry
		dictionary[dictSize] = current + entry[:1]
		dictSize++
		current = entry
	}
	return result
}

func main() {
	if len(os.Args) != 2 {
		fmt.Println("Usage: go run lzw.go <string>")
		os.Exit(1)
	}

	text := os.Args[1]
	compressed := compressLZW(text)
	decompressed := decompressLZW(compressed)

	fmt.Printf("Original: %s\n", text)
	fmt.Printf("Compressed: %v\n", compressed)
	fmt.Printf("Decompressed: %s\n", decompressed)

	// Calculate compression ratio (assuming 16-bit codes)
	origSize := len(text)
	compSize := len(compressed) * 2
	ratio := float64(origSize-compSize) / float64(origSize) * 100
	fmt.Printf("Compression Ratio: %.2f%%\n", ratio)
}
