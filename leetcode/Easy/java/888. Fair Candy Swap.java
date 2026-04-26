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

import java.util.*;

class Solution {
    /**
     * Находит размеры коробок для обмена, чтобы у Алисы и Боба стало поровну конфет.
     * <p>
     * Алгоритм:
     * - Вычисляем общую сумму конфет у Алисы и Боба.
     * - Находим разницу diff = (sumA - sumB) / 2.
     * - Для каждой коробки Алисы a вычисляем необходимую коробку Боба b = a - diff.
     * - Если b есть у Боба (хранится в хеш-множестве), возвращаем [a, b].
     *
     * @param aliceSizes массив коробок Алисы
     * @param bobSizes   массив коробок Боба
     * @return массив из двух чисел [коробка_Алисы, коробка_Боба]
     */
    public int[] fairCandySwap(int[] aliceSizes, int[] bobSizes) {
        int sumA = 0, sumB = 0;
        for (int x : aliceSizes) sumA += x;
        for (int x : bobSizes) sumB += x;
        int diff = (sumA - sumB) / 2;
        Set<Integer> setB = new HashSet<>();
        for (int x : bobSizes) setB.add(x);
        for (int a : aliceSizes) {
            int need = a - diff;
            if (setB.contains(need))
                return new int[]{a, need};
        }
        return new int[]{0, 0};
    }
}