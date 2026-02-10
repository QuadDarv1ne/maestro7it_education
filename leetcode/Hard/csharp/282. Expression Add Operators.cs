/**
 * https://leetcode.com/problems/expression-add-operators/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "282. Expression Add Operators"
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
    public IList<string> AddOperators(string num, int target) {
        /**
         * Генерирует все комбинации операторов +, -, *, которые дают target.
         * 
         * @param num Строка цифр (например, "123")
         * @param target Целевое значение выражения
         * @return Список строк с валидными выражениями
         * 
         * @example AddOperators("123", 6) → ["1+2+3", "1*2*3"]
         * @example AddOperators("232", 8) → ["2*3+2", "2+3*2"]
         * 
         * Сложность:
         *   Время: O(4^n) — на каждой позиции 4 варианта
         *   Память: O(n) для рекурсии
         */
        var result = new List<string>();
        
        void Backtrack(int index, string path, long currentVal, long prevOperand) {
            if (index == num.Length) {
                if (currentVal == target) {
                    result.Add(path);
                }
                return;
            }
            
            for (int i = index; i < num.Length; i++) {
                // Пропускаем числа с ведущим нулем
                if (i > index && num[index] == '0') {
                    break;
                }
                
                string currentStr = num.Substring(index, i - index + 1);
                long currentNum = long.Parse(currentStr);
                
                if (index == 0) {
                    // Первое число
                    Backtrack(i + 1, currentStr, currentNum, currentNum);
                } else {
                    // Сложение
                    Backtrack(i + 1, $"{path}+{currentStr}", 
                             currentVal + currentNum, currentNum);
                    
                    // Вычитание
                    Backtrack(i + 1, $"{path}-{currentStr}", 
                             currentVal - currentNum, -currentNum);
                    
                    // Умножение: корректируем предыдущую операцию
                    Backtrack(i + 1, $"{path}*{currentStr}", 
                             currentVal - prevOperand + prevOperand * currentNum, 
                             prevOperand * currentNum);
                }
            }
        }
        
        Backtrack(0, "", 0, 0);
        return result;
    }
}