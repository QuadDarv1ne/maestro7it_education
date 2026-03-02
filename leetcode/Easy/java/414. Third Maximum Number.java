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

class Solution {
    /**
     * Возвращает третий уникальный максимум или максимум, если уникальных меньше трёх.
     *
     * @param nums массив целых чисел
     * @return третье уникальное максимальное число или максимальное
     */
    public int thirdMax(int[] nums) {
        // Используем Long.MIN_VALUE для обозначения "не установлено",
        // чтобы корректно работать с отрицательными числами
        long first = Long.MIN_VALUE;
        long second = Long.MIN_VALUE;
        long third = Long.MIN_VALUE;

        for (int num : nums) {
            // Пропускаем, если число уже является одним из текущих максимумов
            if (num == first || num == second || num == third) continue;

            if (num > first) {
                third = second;
                second = first;
                first = num;
            } else if (num > second) {
                third = second;
                second = num;
            } else if (num > third) {
                third = num;
            }
        }

        // Если третий максимум был обновлён (не равен Long.MIN_VALUE), возвращаем его
        return third != Long.MIN_VALUE ? (int)third : (int)first;
    }
}