/**
 * https://leetcode.com/problems/validate-stack-sequences/description/
 */

#include <vector>
#include <stack>
using namespace std;

class Solution {
public:
    /**
     * Проверка корректности последовательности операций со стеком.
     * 
     * @param pushed - последовательность чисел, которые последовательно помещаются в стек
     * @param popped - предполагаемая последовательность извлечения из стека
     * @return true, если popped можно получить из pushed с помощью корректных операций стека (LIFO)
     * 
     * Алгоритм:
     * 1. Проходим по массиву pushed и кладём элементы в стек.
     * 2. Каждый раз, когда верхушка стека совпадает с текущим элементом popped,
     *    выталкиваем её и двигаем указатель по popped.
     * 3. Если в конце удалось обработать все элементы popped — последовательность корректна.
     * 
     * Временная сложность: O(n), каждый элемент помещается и извлекается максимум 1 раз.
     * Память: O(n) для вспомогательного стека.
     */
    bool validateStackSequences(vector<int>& pushed, vector<int>& popped) {
        stack<int> st;
        int j = 0;
        for (int x : pushed) {
            st.push(x);
            while (!st.empty() && st.top() == popped[j]) {
                st.pop();
                j++;
            }
        }
        return j == popped.size();
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