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

class Solution {
    public List<List<Integer>> combinationSum3(int k, int n) {
        List<List<Integer>> result = new ArrayList<>();
        List<Integer> current = new ArrayList<>();
        backtrack(1, k, n, current, result);
        return result;
    }
    
    private void backtrack(int start, int k, int remaining, 
                           List<Integer> current, List<List<Integer>> result) {
        // Если комбинация достигла нужной длины
        if (current.size() == k) {
            // Если остаток суммы равен 0 - нашли решение
            if (remaining == 0) {
                result.add(new ArrayList<>(current));
            }
            return;
        }
        
        // Раннее отсечение
        int remainingNumbers = k - current.size();
        
        // Проверка минимальной и максимальной возможной суммы
        int minPossible = start * remainingNumbers + 
                         remainingNumbers * (remainingNumbers - 1) / 2;
        int maxPossible = 9 * remainingNumbers - 
                         remainingNumbers * (remainingNumbers - 1) / 2;
        
        if (remaining < minPossible || remaining > maxPossible) {
            return;
        }
        
        // Перебираем возможные числа
        for (int num = start; num <= 9; num++) {
            // Если число слишком большое
            if (num > remaining) break;
            
            current.add(num);
            backtrack(num + 1, k, remaining - num, current, result);
            current.remove(current.size() - 1);
        }
    }
}