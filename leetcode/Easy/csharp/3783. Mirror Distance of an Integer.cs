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

using System;

public class Solution {
    /// <summary>
    /// Вычисляет зеркальное расстояние числа n.
    /// </summary>
    /// <param name="n">Исходное целое число.</param>
    /// <returns>Целое число, представляющее зеркальное расстояние.</returns>
    public int MirrorDistance(int n) {
        // 1. Преобразуем число в строку.
        string s = n.ToString();
        
        // 2. Преобразуем строку в массив символов и переворачиваем его.
        char[] charArray = s.ToCharArray();
        Array.Reverse(charArray);
        string reversedStr = new string(charArray);
        
        // 3. Парсим обратно в число (ведущие нули отбрасываются).
        int reversedN = int.Parse(reversedStr);
        
        // 4. Возвращаем абсолютную разницу.
        return Math.Abs(n - reversedN);
    }
}