/*
Package rle implements Run-Length Encoding compression

Features:
- Handles repeating and non-repeating sequences
- Supports UTF-8 strings
- Error handling for invalid input
*/
package main

import (
	"bytes"
	"fmt"
	"os"
	"strconv"
	"unicode/utf8"
)

// compressRLE performs RLE compression
func compressRLE(input string) (string, error) {
	if input == "" {
		return "", fmt.Errorf("input cannot be empty")
	}

	var buf bytes.Buffer
	runes := []rune(input)
	i := 0

	for i < len(runes) {
		current := runes[i]
		count := 1

		// Count consecutive same characters
		for i+count < len(runes) && runes[i+count] == current {
			count++
		}

		// Write character
		buf.WriteRune(current)

		// Write count if more than 1
		if count > 1 {
			buf.WriteString(strconv.Itoa(count))
		}

		i += count
	}
	return buf.String(), nil
}

// decompressRLE decompresses RLE data
func decompressRLE(compressed string) (string, error) {
	if compressed == "" {
		return "", fmt.Errorf("compressed data cannot be empty")
	}

	var result bytes.Buffer
	runes := []rune(compressed)
	i := 0

	for i < len(runes) {
		char := runes[i]
		i++

		// Parse number
		numStr := ""
		for i < len(runes) {
			r, size := utf8.DecodeRuneInString(string(runes[i]))
			if r < '0' || r > '9' {
				break
			}
			numStr += string(r)
			i += size
		}

		count := 1
		if numStr != "" {
			var err error
			count, err = strconv.Atoi(numStr)
			if err != nil {
				return "", fmt.Errorf("invalid count: %s", numStr)
			}
		}

		// Write character count times
		for j := 0; j < count; j++ {
			result.WriteRune(char)
		}
	}
	return result.String(), nil
}

func main() {
	if len(os.Args) != 2 {
		fmt.Println("Usage: go run rle.go <string>")
		os.Exit(1)
	}

	input := os.Args[1]
	compressed, err := compressRLE(input)
	if err != nil {
		fmt.Printf("Compression error: %v\n", err)
		os.Exit(1)
	}

	decompressed, err := decompressRLE(compressed)
	if err != nil {
		fmt.Printf("Decompression error: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("Original: %s\n", input)
	fmt.Printf("Compressed: %s\n", compressed)
	fmt.Printf("Decompressed: %s\n", decompressed)

	ratio := float64(len(input)-len(compressed)) / float64(len(input)) * 100
	fmt.Printf("Compression Ratio: %.2f%%\n", ratio)
}
