/**
 * https://leetcode.com/problems/jump-game/description/?envType=study-plan-v2&envId=top-interview-150
 */

class Solution {
public:
    /**
     * canJump:
     * @param nums — вектор неотрицательных чисел, nums[i] — максимальный прыжок из i
     * @return true, если можно достичь последнего индекса, иначе false
     *
     * Подход:
     * - Жадный: переменная maxReach — максимальный достижимый индекс
     * - Проходим, пока i ≤ maxReach
     * - Обновляем maxReach = max(maxReach, i + nums[i])
     * - Если maxReach ≥ последний индекс, возвращаем true
     * Сложность: O(n) времени, O(1) памяти
     */
    bool canJump(vector<int>& nums) {
        int maxReach = 0;
        int n = nums.size();
        for (int i = 0; i <= maxReach && i < n; ++i) {
            maxReach = max(maxReach, i + nums[i]);
            if (maxReach >= n - 1) {
                return true;
            }
        }
        return false;
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