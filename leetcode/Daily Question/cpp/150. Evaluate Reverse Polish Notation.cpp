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
public:
    int evalRPN(vector<string>& tokens) {
        /*
        Вычисляет выражение в обратной польской записи.
        
        Параметры:
            tokens - вектор строк, представляющих токены выражения
        
        Возвращает:
            Результат вычисления выражения
            
        Алгоритм:
            Использует стек для вычисления выражения.
            Для каждого токена:
                - Если число, преобразует в int и помещает в стек
                - Если оператор, извлекает два числа, выполняет операцию
                  и помещает результат в стек
        */
        stack<int> st;
        
        for (const string& token : tokens) {
            if (token != "+" && token != "-" && token != "*" && token != "/") {
                // Токен - число, добавляем в стек
                st.push(stoi(token));
            } else {
                // Токен - оператор, извлекаем два операнда
                int b = st.top(); st.pop();
                int a = st.top(); st.pop();
                
                // Выполняем соответствующую операцию
                if (token == "+") {
                    st.push(a + b);
                } else if (token == "-") {
                    st.push(a - b);
                } else if (token == "*") {
                    st.push(a * b);
                } else { // token == "/"
                    // В C++ деление целых чисел уже округляет к нулю
                    st.push(a / b);
                }
            }
        }
        
        return st.top();
    }
};