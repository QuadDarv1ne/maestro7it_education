class Solution {
public:
    vector<vector<string>> partition(string s) {
        /**
         * Находит все возможные разбиения строки на палиндромные подстроки.
         * 
         * Алгоритм:
         * 1. Backtracking для генерации всех возможных разбиений
         * 2. Проверка каждого префикса на палиндромность
         * 3. Рекурсивная обработка оставшейся части
         *
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
        
        vector<vector<string>> result;
        vector<string> path;
        backtrack(s, 0, path, result);
        return result;
    }
    
private:
    void backtrack(const string& s, int start, vector<string>& path, vector<vector<string>>& result) {
        // Если дошли до конца строки, добавляем текущий путь в результат
        if (start == s.length()) {
            result.push_back(path);
            return;
        }
        
        // Перебираем все возможные окончания текущей подстроки
        for (int end = start + 1; end <= s.length(); end++) {
            string substring = s.substr(start, end - start);
            
            // Если подстрока - палиндром, продолжаем рекурсию
            if (isPalindrome(substring)) {
                path.push_back(substring);          // Добавляем подстроку в путь
                backtrack(s, end, path, result);    // Рекурсивно обрабатываем остаток
                path.pop_back();                    // Удаляем подстроку (backtrack)
            }
        }
    }
    
    bool isPalindrome(const string& s) {
        int left = 0, right = s.length() - 1;
        while (left < right) {
            if (s[left] != s[right]) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
};