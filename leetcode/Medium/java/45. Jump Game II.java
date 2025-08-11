/**
 * https://leetcode.com/problems/jump-game-ii/description/?envType=study-plan-v2&envId=top-interview-150
 */

/**
 * Решение задачи "Jump Game II" — минимальное количество прыжков до конца массива.
 */
public class Solution {
    /**
     * Находит минимальное количество прыжков для достижения последнего индекса.
     *
     * @param nums массив, где nums[i] — максимальный прыжок с позиции i.
     * @return минимальное число прыжков до конца массива.
     *
     * Алгоритм:
     * Жадный подход:
     * - farthest — максимальный индекс, достижимый текущим количеством прыжков.
     * - current_end — граница текущей области прыжков.
     * - Когда индекс достигает current_end, увеличиваем jumps и обновляем current_end.
     *
     * Сложность:
     * - Время: O(n), где n — длина массива nums.
     * - Память: O(1).
     *
     * Пример:
     * nums = [2, 3, 1, 1, 4]
     * Ответ: 2 (прыжки с 0 на 1 и с 1 на 4).
     */
    public int jump(int[] nums) {
        int jumps = 0;
        int current_end = 0;
        int farthest = 0;

        for (int i = 0; i < nums.length - 1; i++) {
            farthest = Math.max(farthest, i + nums[i]);
            if (i == current_end) {
                jumps++;
                current_end = farthest;
            }
        }
        return jumps;
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