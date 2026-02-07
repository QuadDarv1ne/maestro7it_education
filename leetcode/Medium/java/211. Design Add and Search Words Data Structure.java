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

// class TrieNode {
//     TrieNode[] children;
//     boolean isEnd;
    
//     public TrieNode() {
//         children = new TrieNode[26];
//         isEnd = false;
//     }
// }

class WordDictionary {
    private TrieNode root;
    
    public WordDictionary() {
        root = new TrieNode();
    }
    
    public void addWord(String word) {
        TrieNode node = root;
        for (char ch : word.toCharArray()) {
            int idx = ch - 'a';
            if (node.children[idx] == null) {
                node.children[idx] = new TrieNode();
            }
            node = node.children[idx];
        }
        node.isEnd = true;
    }
    
    public boolean search(String word) {
        return searchInNode(word, 0, root);
    }
    
    private boolean searchInNode(String word, int index, TrieNode node) {
        if (index == word.length()) {
            return node.isEnd;
        }
        
        char ch = word.charAt(index);
        
        if (ch == '.') {
            // Проверяем всех возможных детей
            for (int i = 0; i < 26; i++) {
                if (node.children[i] != null && 
                    searchInNode(word, index + 1, node.children[i])) {
                    return true;
                }
            }
            return false;
        } else {
            // Проверяем конкретного ребенка
            int idx = ch - 'a';
            if (node.children[idx] == null) {
                return false;
            }
            return searchInNode(word, index + 1, node.children[idx]);
        }
    }
}