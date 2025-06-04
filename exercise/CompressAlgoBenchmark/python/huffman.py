"""
Huffman Coding Implementation

Features:
- Builds optimal prefix codes
- Handles any character frequencies
- Includes compression ratio calculation
"""

import heapq
from collections import Counter
from typing import Dict, Tuple, Optional

class HuffmanNode:
    """Node for Huffman Tree"""
    def __init__(self, char: Optional[str], freq: int):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def build_tree(text: str) -> HuffmanNode:
    """
    Builds Huffman tree from input text
    
    Args:
        text: Input string
        
    Returns:
        Root node of Huffman tree
    """
    if not text:
        raise ValueError("Input text cannot be empty")
    
    freq = Counter(text)
    heap = [HuffmanNode(char, count) for char, count in freq.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    
    return heap[0]

def generate_codes(root: HuffmanNode) -> Dict[str, str]:
    """
    Generates Huffman codes from tree
    
    Args:
        root: Root node of Huffman tree
        
    Returns:
        Dictionary mapping characters to codes
    """
    codes = {}
    
    def traverse(node, code):
        if node.char:
            codes[node.char] = code
        else:
            traverse(node.left, code + "0")
            traverse(node.right, code + "1")
    
    traverse(root, "")
    return codes

def huffman_compress(text: str) -> Tuple[str, Dict[str, str]]:
    """
    Compresses text using Huffman coding
    
    Args:
        text: Input string
        
    Returns:
        Tuple of (compressed_bitstring, code_dict)
    """
    root = build_tree(text)
    codes = generate_codes(root)
    compressed = "".join(codes[char] for char in text)
    return compressed, codes

def huffman_decompress(bitstring: str, codes: Dict[str, str]) -> str:
    """
    Decompresses Huffman-encoded bitstring
    
    Args:
        bitstring: Compressed binary string
        codes: Huffman code dictionary
        
    Returns:
        Original decompressed text
    """
    inv_codes = {v: k for k, v in codes.items()}
    current = ""
    result = []
    
    for bit in bitstring:
        current += bit
        if current in inv_codes:
            result.append(inv_codes[current])
            current = ""
    
    return "".join(result)

if __name__ == "__main__":
    import sys
    import math
    
    if len(sys.argv) != 2:
        print("Usage: python huffman.py <string>")
        sys.exit(1)
    
    try:
        original = sys.argv[1]
        compressed, codes = huffman_compress(original)
        decompressed = huffman_decompress(compressed, codes)
        
        print(f"Original: {original}")
        print(f"Compressed: {compressed}")
        print(f"Codes: {codes}")
        print(f"Decompressed: {decompressed}")
        
        # Calculate compression ratio (bits)
        orig_bits = len(original) * 8
        comp_bits = len(compressed)
        ratio = (1 - comp_bits / orig_bits) * 100
        print(f"Compression Ratio: {ratio:.2f}%")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
