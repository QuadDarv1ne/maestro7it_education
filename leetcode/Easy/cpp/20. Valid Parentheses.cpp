/**
 * https://leetcode.com/problems/valid-parentheses/description/
 */

#include <stack>
#include <unordered_map>
#include <string>
using namespace std;

class Solution {
public:
    /**
     * Проверка корректности скобочной последовательности.
     * 
     * Алгоритм:
     * 1. Стек хранит открывающие скобки.
     * 2. При встрече закрывающей скобки проверяем соответствие
     *    с верхом стека.
     * 3. Если стек пуст в конце — последовательность корректна.
     * 
     * @param s Строка, содержащая только '()[]{}'
     * @return true — если корректна, иначе false
     */
    bool isValid(string s) {
        stack<char> st;
        unordered_map<char, char> mapping = {{')','('}, {']','['}, {'}','{'}};
        
        for (char c : s) {
            if (mapping.count(c) == 0) {
                st.push(c);
            } else {
                if (st.empty() || st.top() != mapping[c]) {
                    return false;
                }
                st.pop();
            }
        }
        return st.empty();
    }
};

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/