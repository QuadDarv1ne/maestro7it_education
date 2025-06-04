/**
 * @file rle.cpp
 * @brief Run-Length Encoding (RLE) сжатие и распаковка
 * 
 * Реализация алгоритма RLE для сжатия/распаковки строк.
 * Формат сжатия: "A4B3C2" для "AAAABBBCC"
 * 
 * Особенности:
 * - Работает только с ASCII-символами
 * - Не эффективен для неповторяющихся данных
 */

#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>

using namespace std;

/**
 * @brief Сжимает строку с помощью RLE
 * 
 * @param input Входная строка
 * @return string Сжатая строка в формате "A4B3"
 * 
 * @throws invalid_argument Если входная строка пуста
 */
string rle_compress(const string& input) {
    if (input.empty()) {
        throw invalid_argument("Input string cannot be empty");
    }
    
    ostringstream oss;
    size_t i = 0;
    
    while (i < input.size()) {
        char current = input[i];
        size_t count = 1;
        
        while (i + count < input.size() && input[i + count] == current) {
            count++;
        }
        
        oss << current;
        if (count > 1) {
            oss << count;
        }
        
        i += count;
    }
    return oss.str();
}

/**
 * @brief Распаковывает RLE-строку
 * 
 * @param compressed Сжатая строка
 * @return string Исходная строка
 * 
 * @throws invalid_argument При некорректном формате
 */
string rle_decompress(const string& compressed) {
    if (compressed.empty()) {
        throw invalid_argument("Compressed string cannot be empty");
    }
    
    ostringstream oss;
    size_t i = 0;
    
    while (i < compressed.size()) {
        char c = compressed[i++];
        
        if (isdigit(compressed[i])) {
            size_t count = 0;
            while (i < compressed.size() && isdigit(compressed[i])) {
                count = count * 10 + (compressed[i++] - '0');
            }
            oss << string(count, c);
        } else {
            oss << c;
        }
    }
    return oss.str();
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cerr << "Usage: " << argv[0] << " <string>" << endl;
        return 1;
    }
    
    try {
        string original = argv[1];
        auto compressed = rle_compress(original);
        auto decompressed = rle_decompress(compressed);
        
        cout << "Original: " << original << "\n";
        cout << "Compressed: " << compressed << "\n";
        cout << "Decompressed: " << decompressed << "\n";
        cout << "Ratio: " 
             << (1.0 - static_cast<double>(compressed.size()) / original.size()) * 100 
             << "%\n";
    } catch (const exception& e) {
        cerr << "Error: " << e.what() << endl;
        return 1;
    }
    return 0;
}
