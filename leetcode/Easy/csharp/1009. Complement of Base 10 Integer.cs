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

public class Solution {
    /// <summary>
    /// Находит дополнение целого числа (инверсия всех битов).
    /// </summary>
    /// <remarks>
    /// <para><b>Алгоритм:</b> Битовая инверсия с маской.</para>
    /// 
    /// <para><b>Шаги:</b>
    /// <list type="number">
    ///   <item>Обработать крайний случай: <c>n == 0</c> → вернуть <c>1</c></item>
    ///   <item>Найти количество значимых бит: <c>bit_length</c></item>
    ///   <item>Создать маску: <c>mask = (1 << bit_length) - 1</c></item>
    ///   <item>Инвертировать: <c>result = n ^ mask</c></item>
    /// </list>
    /// </para>
    /// 
    /// <para><b>Пример:</b>
    /// <code>
    ///   n = 5 (бинарно: 101)
    ///   bit_length = 3
    ///   mask = (1 << 3) - 1 = 7 (бинарно: 111)
    ///   result = 5 ^ 7 = 2 (бинарно: 010) ✓
    /// </code>
    /// </para>
    /// 
    /// <para><b>Сложность:</b> Время: O(1), Память: O(1)</para>
    /// </remarks>
    /// <param name="n">Входное неотрицательное целое число</param>
    /// <returns>Дополнение числа n</returns>
    public int BitwiseComplement(int n) {
        // Крайний случай: дополнение 0 равно 1
        if (n == 0) return 1;
        
        // Находим количество значимых бит
        int bit_length = Convert.ToString(n, 2).Length;
        
        // Создаём маску из единиц: 111...1 (bit_length раз)
        int mask = (1 << bit_length) - 1;
        
        // XOR инвертирует все биты в пределах маски
        return n ^ mask;
    }
}