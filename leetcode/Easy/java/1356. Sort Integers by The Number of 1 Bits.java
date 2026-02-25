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
     * Сортирует массив по количеству единичных битов,
     * а затем по значению числа.
     *
     * @param arr входной массив
     * @return отсортированный массив
     */
    public int[] sortByBits(int[] arr) {
        // Преобразуем в Integer[] для использования Comparator
        Integer[] boxed = Arrays.stream(arr).boxed().toArray(Integer[]::new);
        Arrays.sort(boxed, (a, b) -> {
            int bitsA = Integer.bitCount(a);
            int bitsB = Integer.bitCount(b);
            if (bitsA == bitsB) return Integer.compare(a, b);
            return Integer.compare(bitsA, bitsB);
        });
        // Обратно в int[]
        return Arrays.stream(boxed).mapToInt(Integer::intValue).toArray();
    }
}