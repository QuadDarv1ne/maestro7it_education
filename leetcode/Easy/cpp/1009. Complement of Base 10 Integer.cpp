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
     * @brief Находит дополнение целого числа (инверсия битов)
     * 
     * @param n Входное неотрицательное целое число
     * @return int Дополнение числа n
     * 
     * Алгоритм: Битовая инверсия с маской
     * 
     * Шаги:
     * 1. Обработать крайний случай: n == 0 → вернуть 1
     * 2. Найти количество значимых бит: bit_length
     * 3. Создать маску: mask = (1 << bit_length) - 1
     * 4. Инвертировать: result = n ^ mask
     * 
     * Пример:
     *   n = 5 (бинарно: 101)
     *   bit_length = 3
     *   mask = (1 << 3) - 1 = 7 (бинарно: 111)
     *   result = 5 ^ 7 = 2 (бинарно: 010) ✓
     * 
     * Сложность:
     *   Время: O(1) — максимум 30 итераций для n < 10^9
     *   Память: O(1)
     */
    int bitwiseComplement(int n) {
        // Крайний случай: дополнение 0 равно 1
        if (n == 0) return 1;
        
        // Находим количество значимых бит в числе
        int bit_length = 0;
        int temp = n;
        while (temp > 0) {
            bit_length++;
            temp >>= 1;
        }
        
        // Создаём маску из единиц: 111...1 (bit_length раз)
        // (1 << bit_length) даёт 1000...0, вычитаем 1 → 0111...1
        int mask = (1 << bit_length) - 1;
        
        // XOR инвертирует все биты в пределах маски
        return n ^ mask;
    }
};