"""
RLE (Run-Length Encoding) Implementation

Features:
- Compresses repeating characters: "AAAABBB" -> "A4B3"
- Handles non-repeating characters: "ABCD" -> "A1B1C1D1"
- Supports ASCII and Unicode
"""

def rle_compress(data: str) -> str:
    """
    Compresses a string using RLE algorithm
    
    Args:
        data: Input string to compress
        
    Returns:
        Compressed string in RLE format
        
    Raises:
        ValueError: If input is empty
    """
    if not data:
        raise ValueError("Input cannot be empty")
    
    compressed = []
    i = 0
    n = len(data)
    
    while i < n:
        char = data[i]
        count = 1
        while i + count < n and data[i + count] == char:
            count += 1
        
        compressed.append(char)
        if count > 1:
            compressed.append(str(count))
        
        i += count
    
    return "".join(compressed)

def rle_decompress(compressed: str) -> str:
    """
    Decompresses RLE-encoded string
    
    Args:
        compressed: RLE-compressed string
        
    Returns:
        Original decompressed string
        
    Raises:
        ValueError: If compressed data is invalid
    """
    if not compressed:
        raise ValueError("Compressed data cannot be empty")
    
    result = []
    i = 0
    n = len(compressed)
    
    while i < n:
        char = compressed[i]
        i += 1
        
        count_str = ""
        while i < n and compressed[i].isdigit():
            count_str += compressed[i]
            i += 1
        
        count = int(count_str) if count_str else 1
        result.append(char * count)
    
    return "".join(result)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python rle.py <string>")
        sys.exit(1)
    
    try:
        original = sys.argv[1]
        compressed = rle_compress(original)
        decompressed = rle_decompress(compressed)
        
        print(f"Original: {original}")
        print(f"Compressed: {compressed}")
        print(f"Decompressed: {decompressed}")
        
        ratio = (1 - len(compressed) / len(original)) * 100
        print(f"Compression Ratio: {ratio:.2f}%")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
