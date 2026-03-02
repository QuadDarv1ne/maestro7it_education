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
    /// Переворачивает гласные буквы в строке.
    /// </summary>
    /// <param name="s">Входная строка.</param>
    /// <returns>Строка с перевёрнутыми гласными.</returns>
    public string ReverseVowels(string s) {
        // Создаём множество гласных
        HashSet<char> vowels = new HashSet<char>("aeiouAEIOU");
        char[] chars = s.ToCharArray();
        int left = 0;
        int right = chars.Length - 1;
        
        while (left < right) {
            // Ищем гласную слева
            while (left < right && !vowels.Contains(chars[left])) {
                left++;
            }
            // Ищем гласную справа
            while (left < right && !vowels.Contains(chars[right])) {
                right--;
            }
            // Меняем местами
            if (left < right) {
                char temp = chars[left];
                chars[left] = chars[right];
                chars[right] = temp;
                left++;
                right--;
            }
        }
        
        return new string(chars);
    }
}