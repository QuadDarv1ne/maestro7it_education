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

public class Solution {
    public IList<IList<int>> CombinationSum3(int k, int n) {
        List<IList<int>> result = new List<IList<int>>();
        List<int> current = new List<int>();
        Backtrack(1, k, n, current, result);
        return result;
    }
    
    private void Backtrack(int start, int k, int remaining, 
                           List<int> current, List<IList<int>> result) {
        // Если комбинация достигла нужной длины
        if (current.Count == k) {
            // Если остаток суммы равен 0 - нашли решение
            if (remaining == 0) {
                result.Add(new List<int>(current));
            }
            return;
        }
        
        // Раннее отсечение
        int remainingNumbers = k - current.Count;
        
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
            
            current.Add(num);
            Backtrack(num + 1, k, remaining - num, current, result);
            current.RemoveAt(current.Count - 1);
        }
    }
}