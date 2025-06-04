/**
 * @file huffman.cpp
 * @brief Алгоритм сжатия Хаффмана
 * 
 * Реализация включает:
 * - Построение дерева Хаффмана
 * - Генерацию кодов
 * - Бит-ориентированное сжатие
 */

#include <iostream>
#include <queue>
#include <unordered_map>
#include <stdexcept>
#include <vector>
#include <bitset>

using namespace std;

// Структура узла дерева
struct Node {
    char ch;
    int freq;
    Node *left, *right;
    
    Node(char c, int f) : ch(c), freq(f), left(nullptr), right(nullptr) {}
};

// Компаратор для очереди с приоритетом
struct Compare {
    bool operator()(Node* l, Node* r) {
        return l->freq > r->freq;
    }
};

/**
 * @brief Генерирует коды Хаффмана
 * 
 * @param root Корень дерева
 * @param code Текущий код
 * @param codes Результирующая таблица кодов
 */
void generate_codes(Node* root, string code, unordered_map<char, string>& codes) {
    if (!root) return;
    
    if (!root->left && !root->right) {
        codes[root->ch] = code;
    }
    
    generate_codes(root->left, code + "0", codes);
    generate_codes(root->right, code + "1", codes);
}

/**
 * @brief Строит дерево Хаффмана
 * 
 * @param text Входной текст
 * @return Node* Корень дерева
 */
Node* build_huffman_tree(const string& text) {
    if (text.empty()) throw invalid_argument("Text cannot be empty");
    
    // Подсчет частот
    unordered_map<char, int> freq;
    for (char c : text) {
        freq[c]++;
    }
    
    // Очередь с приоритетом
    priority_queue<Node*, vector<Node*>, Compare> pq;
    for (auto& pair : freq) {
        pq.push(new Node(pair.first, pair.second));
    }
    
    // Построение дерева
    while (pq.size() > 1) {
        Node* left = pq.top(); pq.pop();
        Node* right = pq.top(); pq.pop();
        
        Node* newNode = new Node('\0', left->freq + right->freq);
        newNode->left = left;
        newNode->right = right;
        pq.push(newNode);
    }
    return pq.top();
}

/**
 * @brief Сжимает текст алгоритмом Хаффмана
 * 
 * @param text Входной текст
 * @return pair<string, Node*> Сжатые биты и дерево
 */
pair<string, Node*> huffman_compress(const string& text) {
    Node* root = build_huffman_tree(text);
    unordered_map<char, string> codes;
    generate_codes(root, "", codes);
    
    string compressed;
    for (char c : text) {
        compressed += codes[c];
    }
    return {compressed, root};
}

/**
 * @brief Распаковывает битовую строку
 * 
 * @param compressed Сжатая битовая строка
 * @param root Корень дерева
 * @return string Исходный текст
 */
string huffman_decompress(const string& compressed, Node* root) {
    string result;
    Node* curr = root;
    
    for (char bit : compressed) {
        curr = (bit == '0') ? curr->left : curr->right;
        
        if (!curr->left && !curr->right) {
            result += curr->ch;
            curr = root;
        }
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
        auto [compressed, tree] = huffman_compress(text);
        auto decompressed = huffman_decompress(compressed, tree);
        
        cout << "Original: " << text << "\n";
        cout << "Compressed bits: " << compressed << "\n";
        cout << "Decompressed: " << decompressed << "\n";
        
        // Расчет коэффициента сжатия (биты -> байты)
        size_t original_bits = text.size() * 8;
        size_t compressed_bits = compressed.size();
        cout << "Compression ratio: " 
             << (1.0 - static_cast<double>(compressed_bits) / original_bits) * 100 
             << "%\n";
        
    } catch (const exception& e) {
        cerr << "Error: " << e.what() << endl;
        return 1;
    }
    return 0;
}
