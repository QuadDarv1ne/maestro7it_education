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
    constructor() {
        this.children = new Map();  // Используем Map для детей
        this.isEnd = false;
    }
}

class WordDictionary {
    constructor() {
        this.root = new TrieNode();
    }
    
    /**
     * Добавляет слово в структуру
     * @param {string} word - Слово для добавления
     */
    addWord(word) {
        let node = this.root;
        for (const char of word) {
            if (!node.children.has(char)) {
                node.children.set(char, new TrieNode());
            }
            node = node.children.get(char);
        }
        node.isEnd = true;
    }
    
    /**
     * Ищет слово в структуре
     * @param {string} word - Слово для поиска (может содержать '.')
     * @return {boolean} - Найдено ли слово
     */
    search(word) {
        const dfs = (node, index) => {
            // Базовый случай: дошли до конца слова
            if (index === word.length) {
                return node.isEnd;
            }
            
            const char = word[index];
            
            // Если символ - точка, проверяем всех детей
            if (char === '.') {
                for (const child of node.children.values()) {
                    if (dfs(child, index + 1)) {
                        return true;
                    }
                }
                return false;
            } 
            // Если символ обычный
            else {
                if (!node.children.has(char)) {
                    return false;
                }
                return dfs(node.children.get(char), index + 1);
            }
        };
        
        return dfs(this.root, 0);
    }
}