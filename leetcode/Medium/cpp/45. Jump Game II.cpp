/**
 * https://leetcode.com/problems/jump-game-ii/description/?envType=study-plan-v2&envId=top-interview-150
 */

class Solution {
public:
    /**
     * Определяет минимальное количество прыжков, чтобы дойти до конца массива.
     *
     * @param nums Вектор целых чисел, где nums[i] — максимальная длина прыжка из позиции i.
     * @return Минимальное количество прыжков до последнего индекса.
     *
     * Описание алгоритма:
     * Используется жадный подход:
     * - farthest хранит наибольший индекс, который можно достичь в рамках текущего количества прыжков.
     * - current_end — граница текущего диапазона прыжков.
     * - При достижении i == current_end увеличиваем счётчик прыжков и обновляем границу.
     *
     * Сложность:
     * - Время: O(n), где n — размер массива nums.
     * - Память: O(1).
     *
     * Пример:
     * nums = [2, 3, 1, 1, 4]
     * Минимум прыжков: 2 (0->1, 1->4).
     */
    int jump(vector<int>& nums) {
        int jumps = 0, current_end = 0, farthest = 0;
        for (int i = 0; i < (int)nums.size() - 1; i++) {
            farthest = max(farthest, i + nums[i]);
            if (i == current_end) {
                jumps++;
                current_end = farthest;
            }
        }
        return jumps;
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