/**
 * https://leetcode.com/problems/binary-search/description/
 */

class Solution {
    /**
     * Выполняет бинарный поиск элемента target в отсортированном массиве nums.
     *
     * Алгоритм:
     * 1. Инициализируем два указателя: left и right.
     * 2. Пока left <= right:
     *    - Вычисляем mid = left + (right - left) / 2.
     *    - Если nums[mid] == target, возвращаем mid.
     *    - Если nums[mid] < target, сдвигаем left = mid + 1.
     *    - Если nums[mid] > target, сдвигаем right = mid - 1.
     * 3. Если элемент не найден, возвращаем -1.
     *
     * @param nums   Отсортированный массив целых чисел
     * @param target Целое число, которое нужно найти
     * @return Индекс target в массиве nums или -1, если элемент не найден
     */
    public int search(int[] nums, int target) {
        int left = 0;
        int right = nums.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (nums[mid] == target) {
                return mid;
            } else if (nums[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        return -1; // элемент не найден
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