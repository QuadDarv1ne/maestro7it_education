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
     * Преобразует заголовок столбца Excel в номер столбца.
     * Это преобразование из системы по основанию 26 в систему по основанию 10.
     * 
     * Сложность по времени: O(n), где n - длина строки
     * Сложность по памяти: O(1)
     */
    int titleToNumber(string columnTitle) {
        int result = 0;
        
        for (char c : columnTitle) {
            // Переходим к следующему разряду
            result = result * 26;
            
            // Добавляем значение текущего символа (A=1, B=2, ..., Z=26)
            result += c - 'A' + 1;
        }
        
        return result;
    }
};