class Solution {
    public List<List<String>> partition(String s) {
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
        
        List<List<String>> result = new ArrayList<>();
        backtrack(s, 0, new ArrayList<>(), result);
        return result;
    }
    
    private void backtrack(String s, int start, List<String> path, List<List<String>> result) {
        // Если дошли до конца строки, добавляем текущий путь в результат
        if (start == s.length()) {
            result.add(new ArrayList<>(path));
            return;
        }
        
        // Перебираем все возможные окончания текущей подстроки
        for (int end = start + 1; end <= s.length(); end++) {
            String substring = s.substring(start, end);
            
            // Если подстрока - палиндром, продолжаем рекурсию
            if (isPalindrome(substring)) {
                path.add(substring);          // Добавляем подстроку в путь
                backtrack(s, end, path, result); // Рекурсивно обрабатываем остаток
                path.remove(path.size() - 1); // Удаляем подстроку (backtrack)
            }
        }
    }
    
    private boolean isPalindrome(String s) {
        int left = 0, right = s.length() - 1;
        while (left < right) {
            if (s.charAt(left) != s.charAt(right)) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
}