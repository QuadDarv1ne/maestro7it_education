public class Solution {
    public IList<IList<string>> Partition(string s) {
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
        
        var result = new List<IList<string>>();
        var path = new List<string>();
        Backtrack(s, 0, path, result);
        return result;
    }
    
    private void Backtrack(string s, int start, List<string> path, List<IList<string>> result) {
        // Если дошли до конца строки, добавляем текущий путь в результат
        if (start == s.Length) {
            result.Add(new List<string>(path));
            return;
        }
        
        // Перебираем все возможные окончания текущей подстроки
        for (int end = start + 1; end <= s.Length; end++) {
            string substring = s.Substring(start, end - start);
            
            // Если подстрока - палиндром, продолжаем рекурсию
            if (IsPalindrome(substring)) {
                path.Add(substring);               // Добавляем подстроку в путь
                Backtrack(s, end, path, result);   // Рекурсивно обрабатываем остаток
                path.RemoveAt(path.Count - 1);     // Удаляем подстроку (backtrack)
            }
        }
    }
    
    private bool IsPalindrome(string s) {
        int left = 0, right = s.Length - 1;
        while (left < right) {
            if (s[left] != s[right]) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
}