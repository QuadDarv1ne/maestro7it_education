/**
 * @file lzw.cpp
 * @brief LZW (Lempel-Ziv-Welch) сжатие
 * 
 * Реализация алгоритма LZW с динамическим словарем
 * Особенности:
 * - Начальный словарь ASCII (0-255)
 * - Кодирование фраз
 */

#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>
#include <stdexcept>

using namespace std;

/**
 * @brief Сжимает строку алгоритмом LZW
 * 
 * @param input Входная строка
 * @return vector<int> Сжатые коды
 */
vector<int> lzw_compress(const string& input) {
    if (input.empty()) {
        throw invalid_argument("Input string cannot be empty");
    }
    
    unordered_map<string, int> dict;
    for (int i = 0; i < 256; i++) {
        dict[string(1, static_cast<char>(i))] = i;
    }
    
    vector<int> result;
    string current;
    int next_code = 256;
    
    for (char c : input) {
        string combined = current + c;
        if (dict.find(combined) != dict.end()) {
            current = combined;
        } else {
            result.push_back(dict[current]);
            dict[combined] = next_code++;
            current = string(1, c);
        }
    }
    
    if (!current.empty()) {
        result.push_back(dict[current]);
    }
    return result;
}

/**
 * @brief Распаковывает LZW коды
 * 
 * @param compressed Вектор сжатых кодов
 * @return string Исходная строка
 */
string lzw_decompress(const vector<int>& compressed) {
    if (compressed.empty()) {
        throw invalid_argument("Compressed data cannot be empty");
    }
    
    unordered_map<int, string> dict;
    for (int i = 0; i < 256; i++) {
        dict[i] = string(1, static_cast<char>(i));
    }
    
    string result;
    string prev = dict[compressed[0]];
    result += prev;
    
    int next_code = 256;
    
    for (size_t i = 1; i < compressed.size(); i++) {
        int code = compressed[i];
        string entry;
        
        if (dict.find(code) != dict.end()) {
            entry = dict[code];
        } else if (code == next_code) {
            entry = prev + prev[0];
        } else {
            throw invalid_argument("Invalid compressed code");
        }
        
        result += entry;
        dict[next_code++] = prev + entry[0];
        prev = entry;
    }
    return result;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cerr << "Usage: " << argv[0] << " <string>" << endl;
        return 1;
    }
    
    try {
        string text = argv[1];
        auto compressed = lzw_compress(text);
        auto decompressed = lzw_decompress(compressed);
        
        cout << "Original: " << text << "\n";
        cout << "Compressed codes: ";
        for (int code : compressed) {
            cout << code << " ";
        }
        cout << "\nDecompressed: " << decompressed << "\n";
        
        // Расчет коэффициента сжатия
        size_t original_size = text.size();
        size_t compressed_size = compressed.size() * sizeof(int);
        cout << "Compression ratio: " 
             << (1.0 - static_cast<double>(compressed_size) / original_size) * 100 
             << "%\n";
        
    } catch (const exception& e) {
        cerr << "Error: " << e.what() << endl;
        return 1;
    }
    return 0;
}
