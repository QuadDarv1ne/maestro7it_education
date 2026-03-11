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
     * Находит дополнение целого числа (инверсия всех битов).
     * 
     * <p><b>Алгоритм:</b> Битовая инверсия с использованием маски.</p>
     * 
     * <p><b>Шаги:</b>
     * <ol>
     *   <li>Обработать крайний случай: {@code n == 0} → вернуть {@code 1}</li>
     *   <li>Найти количество значимых бит: {@code bit_length}</li>
     *   <li>Создать маску: {@code mask = (1 << bit_length) - 1}</li>
     *   <li>Инвертировать: {@code result = n ^ mask}</li>
     * </ol>
     * 
     * <p><b>Пример:</b>
     * <pre>
     *   n = 5 (бинарно: 101)
     *   bit_length = 3
     *   mask = (1 << 3) - 1 = 7 (бинарно: 111)
     *   result = 5 ^ 7 = 2 (бинарно: 010) ✓
     * </pre>
     * 
     * <p><b>Сложность:</b> Время: O(1), Память: O(1)</p>
     * 
     * @param n входное неотрицательное целое число (0 <= n < 10^9)
     * @return дополнение числа n
     */
    public int bitwiseComplement(int n) {
        // Крайний случай: дополнение 0 равно 1
        if (n == 0) return 1;
        
        // Находим количество значимых бит
        int bit_length = Integer.toBinaryString(n).length();
        
        // Создаём маску из единиц нужной длины
        int mask = (1 << bit_length) - 1;
        
        // XOR инвертирует все биты
        return n ^ mask;
    }
}