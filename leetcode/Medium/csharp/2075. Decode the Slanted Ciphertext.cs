/**
 * https://leetcode.com/problems/decode-the-slanted-ciphertext/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Decode the Slanted Ciphertext" на C#
 * 
 * Задача: Расшифровать строку, закодированную наклонной транспозицией.
 * 
 * Алгоритм:
 * 1. Вычисляем количество столбцов: cols = encodedText.Length / rows
 * 2. Проходим по каждой диагонали, начиная с каждого столбца первой строки
 * 3. Собираем символы, прыгая на cols + 1 позицию вперёд
 * 4. Удаляем конечные пробелы
 * 
 * Сложность: O(n) времени, O(n) памяти
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
    public string DecodeCiphertext(string encodedText, int rows) {
        if (string.IsNullOrEmpty(encodedText)) return "";
        
        int n = encodedText.Length;
        int cols = n / rows;
        System.Text.StringBuilder result = new System.Text.StringBuilder();
        
        for (int i = 0; i < cols; i++) {
            for (int j = i; j < n; j += cols + 1) {
                result.Append(encodedText[j]);
            }
        }
        
        return result.ToString().TrimEnd();
    }
}