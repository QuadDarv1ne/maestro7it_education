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
    /**
     * Вычисляет значение арифметического выражения без скобок.
     * 
     * Алгоритм:
     * 1. Использует стек для хранения промежуточных результатов.
     * 2. Операторы * и / обрабатываются немедленно.
     * 3. Операторы + и - откладываются (числа помещаются в стек с соответствующим знаком).
     * 4. В конце суммируются все элементы стека.
     * 
     * Сложность:
     * Время: O(n)
     * Пространство: O(n)
     * 
     * @param s Строка с арифметическим выражением
     * @return Результат вычисления выражения
     * 
     * Примеры:
     * calculate("3+2*2") → 7
     * calculate(" 3/2 ") → 1
     * calculate(" 3+5 / 2 ") → 5
     */
    int calculate(string s) {
        if (s.empty()) return 0;
        
        stack<int> st;
        int num = 0;
        char sign = '+';  // Текущий оператор перед числом
        int n = s.length();
        
        for (int i = 0; i < n; i++) {
            char ch = s[i];
            
            // Если символ - цифра, собираем число
            if (isdigit(ch)) {
                num = num * 10 + (ch - '0');
            }
            
            // Если символ - оператор или последний символ
            if ((!isdigit(ch) && ch != ' ') || i == n - 1) {
                if (sign == '+') {
                    st.push(num);
                } else if (sign == '-') {
                    st.push(-num);
                } else if (sign == '*') {
                    int top = st.top();
                    st.pop();
                    st.push(top * num);
                } else if (sign == '/') {
                    int top = st.top();
                    st.pop();
                    st.push(top / num);  // Целочисленное деление
                }
                
                // Сбрасываем число и обновляем оператор
                num = 0;
                sign = ch;
            }
        }
        
        // Суммируем все элементы в стеке
        int result = 0;
        while (!st.empty()) {
            result += st.top();
            st.pop();
        }
        
        return result;
    }
};