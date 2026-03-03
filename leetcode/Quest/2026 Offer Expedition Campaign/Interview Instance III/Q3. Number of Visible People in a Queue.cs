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
    public int[] CanSeePersonsCount(int[] heights) {
        int n = heights.Length;
        int[] result = new int[n];
        Stack<int> stack = new Stack<int>(); // stores indices
        
        for (int i = n - 1; i >= 0; i--) {
            int visible = 0;
            while (stack.Count > 0 && heights[i] > heights[stack.Peek()]) {
                stack.Pop();
                visible++;
            }
            if (stack.Count > 0) {
                visible++;
            }
            result[i] = visible;
            stack.Push(i);
        }
        return result;
    }
}