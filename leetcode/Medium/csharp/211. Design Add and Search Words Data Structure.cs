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

public class TrieNode {
    public TrieNode[] Children;
    public bool IsEnd;
    
    public TrieNode() {
        Children = new TrieNode[26];
        IsEnd = false;
    }
}

public class WordDictionary {
    private TrieNode root;
    
    public WordDictionary() {
        root = new TrieNode();
    }
    
    public void AddWord(string word) {
        TrieNode node = root;
        foreach (char ch in word) {
            int idx = ch - 'a';
            if (node.Children[idx] == null) {
                node.Children[idx] = new TrieNode();
            }
            node = node.Children[idx];
        }
        node.IsEnd = true;
    }
    
    public bool Search(string word) {
        return SearchInNode(word, 0, root);
    }
    
    private bool SearchInNode(string word, int index, TrieNode node) {
        if (index == word.Length) {
            return node.IsEnd;
        }
        
        char ch = word[index];
        
        if (ch == '.') {
            // Проверяем всех возможных детей
            for (int i = 0; i < 26; i++) {
                if (node.Children[i] != null && 
                    SearchInNode(word, index + 1, node.Children[i])) {
                    return true;
                }
            }
            return false;
        } else {
            // Проверяем конкретного ребенка
            int idx = ch - 'a';
            if (node.Children[idx] == null) {
                return false;
            }
            return SearchInNode(word, index + 1, node.Children[idx]);
        }
    }
}