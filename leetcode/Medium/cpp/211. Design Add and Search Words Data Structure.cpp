/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

class TrieNode {
public:
    TrieNode* children[26];
    bool isEnd;
    
    TrieNode() {
        for (int i = 0; i < 26; i++) {
            children[i] = nullptr;
        }
        isEnd = false;
    }
};

class WordDictionary {
private:
    TrieNode* root;
    
    bool searchInNode(string& word, int index, TrieNode* node) {
        if (index == word.size()) {
            return node->isEnd;
        }
        
        char ch = word[index];
        
        if (ch == '.') {
            // Проверяем всех возможных детей
            for (int i = 0; i < 26; i++) {
                if (node->children[i] != nullptr && 
                    searchInNode(word, index + 1, node->children[i])) {
                    return true;
                }
            }
            return false;
        } else {
            // Проверяем конкретного ребенка
            int idx = ch - 'a';
            if (node->children[idx] == nullptr) {
                return false;
            }
            return searchInNode(word, index + 1, node->children[idx]);
        }
    }
    
public:
    WordDictionary() {
        root = new TrieNode();
    }
    
    void addWord(string word) {
        TrieNode* node = root;
        for (char ch : word) {
            int idx = ch - 'a';
            if (node->children[idx] == nullptr) {
                node->children[idx] = new TrieNode();
            }
            node = node->children[idx];
        }
        node->isEnd = true;
    }
    
    bool search(string word) {
        return searchInNode(word, 0, root);
    }
    
    // Деструктор для очистки памяти (опционально)
    ~WordDictionary() {
        clear(root);
    }
    
private:
    void clear(TrieNode* node) {
        if (!node) return;
        for (int i = 0; i < 26; i++) {
            if (node->children[i]) {
                clear(node->children[i]);
            }
        }
        delete node;
    }
};