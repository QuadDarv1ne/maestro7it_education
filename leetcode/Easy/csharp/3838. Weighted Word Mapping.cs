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
using System.Text;

public class Solution
{
    /// <summary>
    /// Преобразует массив слов в строку символов на основе весов букв.
    /// 
    /// Алгоритм работы:
    /// 1. Вычисляет вес каждого слова как сумму весов составляющих его букв.
    ///    Буква 'a' соответствует индексу 0 в массиве weights, 'b' - 1 и т.д.
    /// 2. Вычисляет остаток от деления веса слова на 26.
    /// 3. Преобразует остаток в символ: 0 -> 'z', 1 -> 'y', ..., 25 -> 'a'.
    /// </summary>
    /// <param name="words">Массив строк для обработки.</param>
    /// <param name="weights">Массив целых чисел, представляющих веса букв от 'a' до 'z'.</param>
    /// <returns>Строка, состоящая из вычисленных символов для каждого входного слова.</returns>
    public string MapWordWeights(string[] words, int[] weights)
    {
        StringBuilder result = new StringBuilder();
        
        foreach (string word in words)
        {
            int sum = 0;
            
            // Вычисляем вес слова
            foreach (char c in word)
            {
                int index = c - 'a';
                sum += weights[index];
            }
            
            // Остаток от деления
            int rem = sum % 26;
            
            // Маппинг: 0 -> 'z', 25 -> 'a'
            // 'z' - rem вычисляет код нужного символа
            char mappedChar = (char)('z' - rem);
            
            result.Append(mappedChar);
        }
        
        return result.ToString();
    }
}