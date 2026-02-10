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

class Solution {
    public List<String> addOperators(String num, int target) {
        /**
         * Генерирует все комбинации операторов +, -, *, которые дают target.
         *
         * @param num Строка цифр (например, "123")
         * @param target Целевое значение выражения
         * @return Список строк с валидными выражениями
         * @example
         *   addOperators("123", 6) → ["1+2+3", "1*2*3"]
         *   addOperators("232", 8) → ["2*3+2", "2+3*2"]
         *
         * Сложность:
         *   Время: O(4^n) — на каждой позиции 4 варианта
         *   Память: O(n) для рекурсии
         */
        List<String> result = new ArrayList<>();
        
        backtrack(num, target, 0, "", 0, 0, result);
        return result;
    }
    
    private void backtrack(String num, int target, int index, String path, 
                          long currentVal, long prevOperand, List<String> result) {
        if (index == num.length()) {
            if (currentVal == target) {
                result.add(path);
            }
            return;
        }
        
        for (int i = index; i < num.length(); i++) {
            // Пропускаем числа с ведущим нулем
            if (i > index && num.charAt(index) == '0') {
                break;
            }
            
            String currentStr = num.substring(index, i + 1);
            long currentNum = Long.parseLong(currentStr);
            
            if (index == 0) {
                // Первое число
                backtrack(num, target, i + 1, currentStr, 
                         currentNum, currentNum, result);
            } else {
                // Сложение
                backtrack(num, target, i + 1, path + "+" + currentStr, 
                         currentVal + currentNum, currentNum, result);
                
                // Вычитание
                backtrack(num, target, i + 1, path + "-" + currentStr, 
                         currentVal - currentNum, -currentNum, result);
                
                // Умножение: корректируем предыдущую операцию
                backtrack(num, target, i + 1, path + "*" + currentStr, 
                         currentVal - prevOperand + prevOperand * currentNum, 
                         prevOperand * currentNum, result);
            }
        }
    }
}