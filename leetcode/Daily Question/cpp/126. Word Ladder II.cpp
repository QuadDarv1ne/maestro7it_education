class Solution {
public:
    vector<vector<string>> findLadders(string beginWord, string endWord, vector<string>& wordList) {
        /**
         * Находит все кратчайшие последовательности преобразований от beginWord до endWord.
         * 
         * Алгоритм:
         * 1. Используем BFS для построения графа предшественников
         * 2. На каждом уровне BFS отслеживаем всех предшественников для каждого слова
         * 3. Используем DFS для восстановления всех путей
         * 
         * Сложность: O(N * L * 26) время, O(N^2) память
         */
        
        vector<vector<string>> result;
        unordered_set<string> wordSet(wordList.begin(), wordList.end());
        
        // Если endWord нет в списке, пути нет
        if (wordSet.find(endWord) == wordSet.end()) {
            return result;
        }
        
        // Если beginWord совпадает с endWord
        if (beginWord == endWord) {
            result.push_back({beginWord});
            return result;
        }
        
        // Уровни BFS: слово -> минимальный уровень (расстояние от beginWord)
        unordered_map<string, int> level;
        level[beginWord] = 0;
        
        // Граф предшественников: слово -> список слов-предшественников
        unordered_map<string, vector<string>> predecessors;
        
        // Очередь для BFS
        queue<string> q;
        q.push(beginWord);
        
        bool found = false;  // Флаг, что нашли endWord
        
        // BFS для построения графа предшественников
        while (!q.empty() && !found) {
            int currentLevelSize = q.size();
            unordered_set<string> visitedThisLevel;
            
            // Обрабатываем все слова текущего уровня
            for (int i = 0; i < currentLevelSize; i++) {
                string currentWord = q.front();
                q.pop();
                
                // Генерируем все возможные соседние слова
                for (int j = 0; j < currentWord.length(); j++) {
                    char originalChar = currentWord[j];
                    
                    for (char c = 'a'; c <= 'z'; c++) {
                        if (c == originalChar) continue;
                        
                        currentWord[j] = c;
                        string newWord = currentWord;
                        
                        // Если новое слово - это endWord
                        if (newWord == endWord) {
                            predecessors[endWord].push_back(currentWord);
                            found = true;
                        }
                        // Если слово есть в списке и мы его еще не посещали на этом или более раннем уровне
                        else if (wordSet.find(newWord) != wordSet.end()) {
                            // Если слово еще не посещали
                            if (level.find(newWord) == level.end()) {
                                level[newWord] = level[currentWord] + 1;
                                q.push(newWord);
                                predecessors[newWord].push_back(currentWord);
                                visitedThisLevel.insert(newWord);
                            }
                            // Если слово уже посещено на текущем уровне, добавляем предшественника
                            else if (level[newWord] == level[currentWord] + 1) {
                                predecessors[newWord].push_back(currentWord);
                            }
                        }
                    }
                    
                    // Восстанавливаем оригинальный символ
                    currentWord[j] = originalChar;
                }
            }
            
            // Удаляем слова текущего уровня из wordSet, чтобы избежать циклов
            for (const string& word : visitedThisLevel) {
                wordSet.erase(word);
            }
        }
        
        // Если не нашли endWord
        if (!found) {
            return result;
        }
        
        // DFS для восстановления всех путей
        vector<string> path;
        dfs(endWord, beginWord, predecessors, path, result);
        
        return result;
    }
    
private:
    void dfs(string currentWord, string beginWord,
             unordered_map<string, vector<string>>& predecessors,
             vector<string>& path, vector<vector<string>>& result) {
        /**
         * Рекурсивно строит пути от endWord к beginWord.
         */
        
        // Добавляем текущее слово в путь
        path.push_back(currentWord);
        
        // Если дошли до beginWord, добавляем путь в результат
        if (currentWord == beginWord) {
            vector<string> validPath = path;
            reverse(validPath.begin(), validPath.end());
            result.push_back(validPath);
        }
        else {
            // Рекурсивно идем ко всем предшественникам
            if (predecessors.find(currentWord) != predecessors.end()) {
                for (const string& pred : predecessors[currentWord]) {
                    dfs(pred, beginWord, predecessors, path, result);
                }
            }
        }
        
        // Backtrack
        path.pop_back();
    }
};