# Compression Algorithms Benchmark

## Проект сравнительного анализа алгоритмов сжатия:
- RLE (Run-Length Encoding)
- Алгоритм Хаффмана
- LZW (Lempel-Ziv-Welch)

## Особенности:
1. Реализация на трёх языках (C++, Go, Python)
2. **Единый интерфейс для всех алгоритмов:**
   - compress(input) → compressed_data
   - decompress(compressed) → original_data
3. **Система тестирования:**
   - Тестовые данные 3-х типов
   - Расчёт коэффициента сжатия
   - Визуализация результатов

## Пример использования (Python):
```python
from huffman import HuffmanCoder

data = "hello world sample text"
coder = HuffmanCoder()

# Сжатие
compressed = coder.compress(data)  

# Распаковка
decompressed = coder.decompress(compressed)

print(f"Коэффициент сжатия: {compression_ratio(data, compressed):.1f}%")
```

## Для запуска каждого алгоритма:
```bash
# C++
g++ -std=c++17 -O2 -o rle cpp/rle.cpp && ./rle "AAAABBBCCD"

# Python
python python/rle.py "AAAABBBCCD"

# Go
go run go/rle.go "AAAABBBCCD"
```

---

**Преподаватель:** Дуплей Максим Игоревич

**Дата:** 04.06.2025
