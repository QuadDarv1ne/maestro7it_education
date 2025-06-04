/*
Package huffman implements Huffman coding compression

Features:
- Builds optimal prefix codes
- Handles any character frequencies
- Includes compression ratio calculation
*/
package main

import (
	"container/heap"
	"fmt"
	"os"
)

// Node represents a node in Huffman tree
type Node struct {
	char  rune
	freq  int
	left  *Node
	right *Node
}

// PriorityQueue implements heap.Interface
type PriorityQueue []*Node

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	return pq[i].freq < pq[j].freq
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
}

func (pq *PriorityQueue) Push(x interface{}) {
	*pq = append(*pq, x.(*Node))
}

func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	node := old[n-1]
	*pq = old[0 : n-1]
	return node
}

// buildTree constructs Huffman tree
func buildTree(text string) *Node {
	if text == "" {
		panic("input text cannot be empty")
	}

	freq := make(map[rune]int)
	for _, char := range text {
		freq[char]++
	}

	pq := &PriorityQueue{}
	heap.Init(pq)

	for char, count := range freq {
		heap.Push(pq, &Node{char: char, freq: count})
	}

	for pq.Len() > 1 {
		left := heap.Pop(pq).(*Node)
		right := heap.Pop(pq).(*Node)

		parent := &Node{
			freq:  left.freq + right.freq,
			left:  left,
			right: right,
		}
		heap.Push(pq, parent)
	}
	return heap.Pop(pq).(*Node)
}

// generateCodes creates Huffman codes
func generateCodes(root *Node, prefix string, codes map[rune]string) {
	if root == nil {
		return
	}

	if root.left == nil && root.right == nil {
		codes[root.char] = prefix
	}

	generateCodes(root.left, prefix+"0", codes)
	generateCodes(root.right, prefix+"1", codes)
}

// compress performs Huffman compression
func compress(text string) (string, map[rune]string) {
	root := buildTree(text)
	codes := make(map[rune]string)
	generateCodes(root, "", codes)

	var compressed string
	for _, char := range text {
		compressed += codes[char]
	}
	return compressed, codes
}

// decompress reconstructs original text
func decompress(compressed string, root *Node) string {
	var result []rune
	current := root

	for _, bit := range compressed {
		if bit == '0' {
			current = current.left
		} else {
			current = current.right
		}

		if current.left == nil && current.right == nil {
			result = append(result, current.char)
			current = root
		}
	}
	return string(result)
}

func main() {
	if len(os.Args) != 2 {
		fmt.Println("Usage: go run huffman.go <string>")
		os.Exit(1)
	}

	text := os.Args[1]
	compressed, codes := compress(text)
	decompressed := decompress(compressed, buildTree(text))

	fmt.Printf("Original: %s\n", text)
	fmt.Printf("Compressed: %s\n", compressed)
	fmt.Printf("Codes: %v\n", codes)
	fmt.Printf("Decompressed: %s\n", decompressed)

	// Calculate compression ratio
	origBits := len(text) * 8
	compBits := len(compressed)
	ratio := float64(origBits-compBits) / float64(origBits) * 100
	fmt.Printf("Compression Ratio: %.2f%%\n", ratio)
}
