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
    /**
     * Вычисляет выражение в обратной польской записи.
     * 
     * @param tokens Массив строк, представляющих токены выражения
     * @return Результат вычисления выражения
     * 
     * Алгоритм:
     * 1. Использует стек для хранения операндов
     * 2. Для каждого токена:
     *    - Если токен является числом, преобразует его в int и помещает в стек
     *    - Если токен является оператором, извлекает два операнда из стека,
     *      выполняет операцию и помещает результат обратно в стек
     * 3. В стеке остается один элемент - результат вычислений
     */
    public int evalRPN(String[] tokens) {
        Stack<Integer> stack = new Stack<>();
        
        for (String token : tokens) {
            if (!token.equals("+") && !token.equals("-") && 
                !token.equals("*") && !token.equals("/")) {
                // Токен - число
                stack.push(Integer.parseInt(token));
            } else {
                // Токен - оператор, извлекаем два операнда
                int b = stack.pop();
                int a = stack.pop();
                
                // Выполняем операцию в зависимости от оператора
                switch (token) {
                    case "+":
                        stack.push(a + b);
                        break;
                    case "-":
                        stack.push(a - b);
                        break;
                    case "*":
                        stack.push(a * b);
                        break;
                    case "/":
                        // В Java целочисленное деление округляет к нулю
                        stack.push(a / b);
                        break;
                }
            }
        }
        
        return stack.pop();
    }
}