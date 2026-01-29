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
    /// <summary>
    /// Вычисляет выражение в обратной польской записи.
    /// </summary>
    /// <param name="tokens">Массив строк, представляющих токены выражения.</param>
    /// <returns>Результат вычисления выражения.</returns>
    /// <remarks>
    /// Алгоритм:
    /// 1. Используется стек для хранения операндов.
    /// 2. Каждый токен обрабатывается:
    ///    - Если токен является числом, он преобразуется в int и помещается в стек.
    ///    - Если токен является оператором, из стека извлекаются два операнда,
    ///      выполняется операция и результат помещается обратно в стек.
    /// 3. После обработки всех токенов в стеке остается один элемент - результат.
    /// </remarks>
    public int EvalRPN(string[] tokens) {
        Stack<int> stack = new Stack<int>();
        
        foreach (string token in tokens) {
            if (token != "+" && token != "-" && token != "*" && token != "/") {
                // Токен - число
                stack.Push(int.Parse(token));
            } else {
                // Токен - оператор
                int b = stack.Pop();
                int a = stack.Pop();
                
                // Выполняем соответствующую операцию
                switch (token) {
                    case "+":
                        stack.Push(a + b);
                        break;
                    case "-":
                        stack.Push(a - b);
                        break;
                    case "*":
                        stack.Push(a * b);
                        break;
                    case "/":
                        // В C# целочисленное деление округляет к нулю
                        stack.Push(a / b);
                        break;
                }
            }
        }
        
        return stack.Pop();
    }
}