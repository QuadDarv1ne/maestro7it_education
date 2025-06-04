"""
LZW (Lempel-Ziv-Welch) Compression Algorithm

Features:
- Adaptive dictionary building
- Handles any input data
- Includes compression ratio calculation
"""

def lzw_compress(data: str) -> list:
    """
    Compresses input string using LZW algorithm
    
    Args:
        data: Input string
        
    Returns:
        List of compressed codes
    """
    if not data:
        raise ValueError("Input data cannot be empty")
    
    # Initialize dictionary with ASCII
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    
    result = []
    current = ""
    
    for char in data:
        combined = current + char
        if combined in dictionary:
            current = combined
        else:
            result.append(dictionary[current])
            dictionary[combined] = dict_size
            dict_size += 1
            current = char
    
    if current:
        result.append(dictionary[current])
    
    return result

def lzw_decompress(compressed: list) -> str:
    """
    Decompresses LZW compressed data
    
    Args:
        compressed: List of LZW codes
        
    Returns:
        Original decompressed string
    """
    if not compressed:
        raise ValueError("Compressed data cannot be empty")
    
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}
    
    result = [dictionary[compressed[0]]]
    current = dictionary[compressed[0]]
    
    for code in compressed[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == dict_size:
            entry = current + current[0]
        else:
            raise ValueError("Invalid compressed code")
        
        result.append(entry)
        dictionary[dict_size] = current + entry[0]
        dict_size += 1
        current = entry
    
    return "".join(result)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python lzw.py <string>")
        sys.exit(1)
    
    try:
        original = sys.argv[1]
        compressed = lzw_compress(original)
        decompressed = lzw_decompress(compressed)
        
        print(f"Original: {original}")
        print(f"Compressed: {compressed}")
        print(f"Decompressed: {decompressed}")
        
        # Calculate compression ratio (bytes)
        orig_size = len(original.encode('utf-8'))
        comp_size = len(compressed) * 2  # assuming 16-bit codes
        ratio = (1 - comp_size / orig_size) * 100
        print(f"Compression Ratio: {ratio:.2f}%")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
