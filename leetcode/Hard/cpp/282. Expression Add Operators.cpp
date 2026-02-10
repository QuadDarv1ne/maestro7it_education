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
public:
    vector<string> addOperators(string num, int target) {
        /**
         * Генерирует все комбинации операторов +, -, *, которые дают target.
         * 
         * @param num Строка цифр (например, "123")
         * @param target Целевое значение выражения
         * @return Вектор строк с валидными выражениями
         * 
         * @example addOperators("123", 6) → ["1+2+3", "1*2*3"]
         * @example addOperators("232", 8) → ["2*3+2", "2+3*2"]
         * 
         * Сложность:
         *   Время: O(4^n) — на каждой позиции 4 варианта
         *   Память: O(n) для рекурсии
         */
        vector<string> result;
        
        function<void(int, string, long, long)> backtrack = 
            [&](int index, string path, long current_val, long prev_operand) {
            if (index == num.size()) {
                if (current_val == target) {
                    result.push_back(path);
                }
                return;
            }
            
            for (int i = index; i < num.size(); i++) {
                // Пропускаем числа с ведущим нулем
                if (i > index && num[index] == '0') {
                    break;
                }
                
                string current_str = num.substr(index, i - index + 1);
                long current_num = stol(current_str);
                
                if (index == 0) {
                    // Первое число
                    backtrack(i + 1, current_str, current_num, current_num);
                } else {
                    // Сложение
                    backtrack(i + 1, path + "+" + current_str, 
                             current_val + current_num, current_num);
                    
                    // Вычитание
                    backtrack(i + 1, path + "-" + current_str, 
                             current_val - current_num, -current_num);
                    
                    // Умножение: корректируем предыдущую операцию
                    backtrack(i + 1, path + "*" + current_str, 
                             current_val - prev_operand + prev_operand * current_num, 
                             prev_operand * current_num);
                }
            }
        };
        
        backtrack(0, "", 0, 0);
        return result;
    }
};