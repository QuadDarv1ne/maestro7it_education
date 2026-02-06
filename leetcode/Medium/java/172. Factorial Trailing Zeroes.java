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
     * Подсчитывает количество нулей в конце n!.
     * Нули образуются от пар множителей 2 и 5.
     * Поскольку двоек всегда больше, чем пятерок, считаем только пятерки.
     * 
     * Сложность по времени: O(log₅ n)
     * Сложность по памяти: O(1)
     */
    public int trailingZeroes(int n) {
        int count = 0;
        
        while (n >= 5) {
            n /= 5;
            count += n;
        }
        
        return count;
    }
}