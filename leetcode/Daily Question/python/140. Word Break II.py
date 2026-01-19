"""
LeetCode 140: Word Break II

Задача: Дана строка s и словарь строк wordDict. Добавьте пробелы в s, чтобы
построить предложение, где каждое слово является допустимым словом из словаря.
Верните все такие возможные предложения в любом порядке.

Примечание: Одно и то же слово из словаря может быть использовано несколько раз.

Пример 1:
Вход: s = "catsanddog", wordDict = ["cat","cats","and","sand","dog"]
Выход: ["cats and dog","cat sand dog"]

Пример 2:
Вход: s = "pineapplepenapple", wordDict = ["apple","pen","applepen","pine","pineapple"]
Выход: ["pine apple pen apple","pineapple pen apple","pine applepen apple"]

Пример 3:
Вход: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
Выход: []

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1: @quadd4rv1n7
3. Telegram №2: @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
"""

# from typing import List


class TrieNode:
    """Узел префиксного дерева"""
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    """Префиксное дерево для эффективного поиска слов"""
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        """Вставка слова в Trie"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        """Проверка, существует ли слово в Trie"""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end


class Solution:
    # Подход 1: DFS с мемоизацией и Trie (Наиболее оптимальный)
    # Время: O(n * 2^n) в худшем случае, Память: O(n * 2^n)
    def wordBreak(self, s, wordDict):
        """
        Используем Trie для эффективного поиска слов и DFS с мемоизацией
        для построения всех возможных предложений.
        
        Мемоизация сохраняет уже найденные результаты для подстрок,
        чтобы избежать повторных вычислений.
        """
        # Строим Trie из словаря
        trie = Trie()
        for word in wordDict:
            trie.insert(word)
        
        # Словарь для мемоизации: индекс -> список предложений
        memo = {}
        
        def dfs(start):
            """
            Рекурсивная функция для поиска всех возможных разбиений
            начиная с позиции start
            """
            # Если достигли конца строки
            if start == len(s):
                return [""]
            
            # Если результат уже вычислен, возвращаем из кэша
            if start in memo:
                return memo[start]
            
            results = []
            
            # Пробуем все возможные слова, начиная с текущей позиции
            for end in range(start + 1, len(s) + 1):
                word = s[start:end]
                
                # Если слово существует в словаре
                if trie.search(word):
                    # Рекурсивно получаем все предложения для оставшейся части
                    sub_results = dfs(end)
                    
                    # Добавляем текущее слово к каждому результату
                    for sub in sub_results:
                        if sub:
                            results.append(word + " " + sub)
                        else:
                            results.append(word)
            
            # Сохраняем результат в кэш
            memo[start] = results
            return results
        
        return dfs(0)
    
    
    # Подход 2: DFS с мемоизацией (без Trie)
    # Время: O(n * 2^n), Память: O(n * 2^n)
    def wordBreak_simple(self, s, wordDict):
        """
        Простой подход с использованием множества для словаря.
        Подходит для небольших словарей.
        """
        word_set = set(wordDict)
        memo = {}
        
        def dfs(start):
            if start == len(s):
                return [""]
            
            if start in memo:
                return memo[start]
            
            results = []
            
            for end in range(start + 1, len(s) + 1):
                word = s[start:end]
                
                if word in word_set:
                    sub_results = dfs(end)
                    
                    for sub in sub_results:
                        if sub:
                            results.append(word + " " + sub)
                        else:
                            results.append(word)
            
            memo[start] = results
            return results
        
        return dfs(0)
    
    
    # Подход 3: Динамическое программирование
    # Время: O(n^2 * m), где m - количество слов, Память: O(n^2)
    def wordBreak_dp(self, s, wordDict):
        """
        DP подход: dp[i] содержит все возможные предложения для s[0:i]
        """
        word_set = set(wordDict)
        n = len(s)
        
        # dp[i] - список всех возможных предложений для подстроки s[0:i]
        dp = [[] for _ in range(n + 1)]
        dp[0] = [""]
        
        for i in range(1, n + 1):
            for j in range(i):
                word = s[j:i]
                
                if word in word_set and dp[j]:
                    for sentence in dp[j]:
                        if sentence:
                            dp[i].append(sentence + " " + word)
                        else:
                            dp[i].append(word)
        
        return dp[n]