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
     * Переворачивает гласные буквы в строке.
     * Использует подход с двумя указателями.
     *
     * @param s исходная строка
     * @return строка с изменённым порядком гласных
     */
    public String reverseVowels(String s) {
        // Строка с гласными для проверки (можно использовать Set, но для простоты - строка)
        String vowels = "aeiouAEIOU";
        char[] chars = s.toCharArray();
        int left = 0;
        int right = chars.length - 1;
        
        while (left < right) {
            // Ищем гласную слева
            while (left < right && vowels.indexOf(chars[left]) == -1) {
                left++;
            }
            // Ищем гласную справа
            while (left < right && vowels.indexOf(chars[right]) == -1) {
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
        
        return new String(chars);
    }
}