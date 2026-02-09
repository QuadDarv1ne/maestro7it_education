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
    vector<int> singleNumber(vector<int>& nums) {
        // Шаг 1: XOR всех чисел
        long long xor_all = 0;
        for (int num : nums) {
            xor_all ^= num;
        }
        
        // Шаг 2: Находим правый единичный бит
        int diff = xor_all & -xor_all;
        
        // Шаг 3: Разделяем и находим два числа
        int a = 0, b = 0;
        for (int num : nums) {
            if (num & diff) {
                a ^= num;
            } else {
                b ^= num;
            }
        }
        
        return {a, b};
    }
};