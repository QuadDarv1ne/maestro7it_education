/**
 * https://leetcode.com/problems/jump-game/description/?envType=study-plan-v2&envId=top-interview-150
 */

public class Solution {
    /**
     * Метод canJump:
     * @param nums — массив неотрицательных чисел, nums[i] — максимальный прыжок с позиции i
     * @return true, если можно добраться до последнего индекса, иначе false
     *
     * Жадный подход:
     * - Переменная maxReach — максимально достижимый индекс
     * - Пробегаем массив до тех пор, пока i ≤ maxReach
     * - Обновляем maxReach = max(maxReach, i + nums[i])
     * - Если maxReach ≥ последний индекс, возвращаем true
     * Сложность: O(n) по времени, O(1) по памяти
     */
    public boolean canJump(int[] nums) {
        int maxReach = 0;
        int last = nums.length - 1;
        for (int i = 0; i <= maxReach && i < nums.length; i++) {
            maxReach = Math.max(maxReach, i + nums[i]);
            if (maxReach >= last) {
                return true;
            }
        }
        return false;
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