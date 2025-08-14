/**
 * https://leetcode.com/problems/move-zeroes/description/
 */

/// <summary>
/// Перемещает все нули в конец массива, сохраняя порядок ненулевых элементов.
/// 
/// Алгоритм:
/// - Два указателя: i (позиция для следующего ненулевого элемента) и j (текущий индекс)
/// - Если nums[j] != 0, меняем местами nums[i] и nums[j], увеличиваем i
/// 
/// Время: O(n), Память: O(1)
/// </summary>
public class Solution {
    public void MoveZeroes(int[] nums) {
        int i = 0;
        for (int j = 0; j < nums.Length; j++) {
            if (nums[j] != 0) {
                int temp = nums[i];
                nums[i] = nums[j];
                nums[j] = temp;
                i++;
            }
        }
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