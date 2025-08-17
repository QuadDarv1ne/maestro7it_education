/**
 * https://leetcode.com/problems/validate-stack-sequences/description/
 */

using System.Collections.Generic;

public class Solution {
    /// <summary>
    /// Проверка, можно ли получить последовательность popped
    /// из последовательности pushed при работе со стеком.
    ///
    /// Алгоритм:
    /// 1. Идём по pushed и кладём элементы в стек.
    /// 2. Если верхушка совпадает с текущим элементом popped,
    ///    извлекаем и двигаем указатель.
    /// 3. В конце проверяем, обработаны ли все элементы popped.
    ///
    /// Сложность: O(n) по времени и O(n) по памяти.
    /// </summary>
    public bool ValidateStackSequences(int[] pushed, int[] popped) {
        Stack<int> st = new Stack<int>();
        int j = 0;
        foreach (int x in pushed) {
            st.Push(x);
            while (st.Count > 0 && st.Peek() == popped[j]) {
                st.Pop();
                j++;
            }
        }
        return j == popped.Length;
    }
}

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