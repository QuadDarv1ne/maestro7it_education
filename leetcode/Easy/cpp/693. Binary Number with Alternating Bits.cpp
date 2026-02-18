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
public:
    /**
     * Определяет, чередуются ли биты в двоичном представлении числа.
     *
     * Используется свойство: для числа с чередующимися битами выражение
     * n ^ (n >> 1) даёт число, состоящее только из единиц (вида 2^k - 1).
     * Затем проверяется, является ли это число + 1 степенью двойки.
     *
     * @param n Положительное целое число (1 <= n <= 2^31 - 1)
     * @return true, если биты чередуются, иначе false
     *
     * Примеры:
     *   hasAlternatingBits(5)  // 101 -> true
     *   hasAlternatingBits(7)  // 111 -> false
     *   hasAlternatingBits(11) // 1011 -> false
     *
     * Сложность:
     *   Время: O(1) — константное число битовых операций.
     *   Память: O(1) — используются только несколько переменных.
     *
     * Примечание: используем long long для предотвращения переполнения
     * signed int при n = 2^31 - 1 (см. крайний случай).
     */
    bool hasAlternatingBits(int n) {
        long long xorResult = n ^ (n >> 1);  // используем 64-битный тип для безопасности
        return (xorResult & (xorResult + 1)) == 0;
    }
};