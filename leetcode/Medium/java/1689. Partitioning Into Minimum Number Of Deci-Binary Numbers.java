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
    public int minPartitions(String n) {
        int maxDigit = 0;
        
        // Проходим по каждому символу строки
        for (int i = 0; i < n.length(); i++) {
            // Получаем числовое значение цифры (код символа - код '0')
            int digit = n.charAt(i) - '0';
            
            // Если нашли цифру больше текущего максимума, обновляем его
            if (digit > maxDigit) {
                maxDigit = digit;
            }
        }
        
        return maxDigit;
    }
}