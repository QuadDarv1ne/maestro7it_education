from collections import deque, defaultdict
# from typing import List

class Solution:
    def findLadders(self, beginWord, endWord, wordList):
        """
        Находит все кратчайшие последовательности преобразований от beginWord до endWord.
        
        Параметры:
        -----------
        beginWord : str
            Начальное слово
        endWord : str
            Конечное слово
        wordList : List[str]
            Список доступных слов
        
        Возвращает:
        -----------
        List[List[str]]
            Список всех кратчайших последовательностей
        
        Алгоритм:
        ---------
        1. Проверяем наличие endWord в wordList
        2. Используем BFS для построения графа предшественников
        3. Используем DFS для восстановления всех путей
        
        Сложность:
        ----------
        Время: O(N * L * 26), где N - количество слов, L - длина слова
        Память: O(N^2) в худшем случае
        """
        
        if endWord not in wordList:
            return []
        
        # Преобразуем в множество для быстрого доступа
        wordSet = set(wordList)
        
        # Словарь для хранения всех предшественников каждого слова
        predecessors = defaultdict(list)
        
        # Очередь для BFS
        queue = deque([beginWord])
        
        # Уровень каждого слова
        level = {beginWord: 0}
        
        # Флаг, что нашли конечное слово
        found = False
        
        # BFS
        while queue and not found:
            current_level_size = len(queue)
            visited_this_level = set()
            
            for _ in range(current_level_size):
                current_word = queue.popleft()
                
                # Генерируем все возможные соседние слова
                for i in range(len(current_word)):
                    for c in 'abcdefghijklmnopqrstuvwxyz':
                        if c == current_word[i]:
                            continue
                        new_word = current_word[:i] + c + current_word[i+1:]
                        
                        if new_word == endWord:
                            found = True
                            predecessors[endWord].append(current_word)
                        elif new_word in wordSet:
                            if new_word not in level:
                                level[new_word] = level[current_word] + 1
                                queue.append(new_word)
                                predecessors[new_word].append(current_word)
                                visited_this_level.add(new_word)
                            elif level[new_word] == level[current_word] + 1:
                                # Дополнительный предшественник на том же уровне
                                predecessors[new_word].append(current_word)
            
            # Удаляем посещенные слова из набора
            wordSet -= visited_this_level
        
        # Если не нашли путь
        if not found:
            return []
        
        # Восстанавливаем все пути с помощью DFS
        result = []
        
        def build_paths(word, path):
            if word == beginWord:
                result.append(path[::-1])
                return
            for pred in predecessors[word]:
                build_paths(pred, path + [pred])
        
        build_paths(endWord, [endWord])
        return result