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
 * 
 * Проверяет, можно ли сделать две строки длины 4 равными,
 * меняя местами символы на позициях, разница между которыми равна 2.
 */

class Solution {
    public boolean canBeEqual(String s1, String s2) {
        // Проверяем мультимножества символов на позициях (0,2) и (1,3)
        
        // Для позиций 0 и 2
        char[] pair1 = {s1.charAt(0), s1.charAt(2)};
        char[] pair2 = {s2.charAt(0), s2.charAt(2)};
        java.util.Arrays.sort(pair1);
        java.util.Arrays.sort(pair2);
        if (pair1[0] != pair2[0] || pair1[1] != pair2[1]) {
            return false;
        }
        
        // Для позиций 1 и 3
        pair1[0] = s1.charAt(1);
        pair1[1] = s1.charAt(3);
        pair2[0] = s2.charAt(1);
        pair2[1] = s2.charAt(3);
        java.util.Arrays.sort(pair1);
        java.util.Arrays.sort(pair2);
        if (pair1[0] != pair2[0] || pair1[1] != pair2[1]) {
            return false;
        }
        
        return true;
    }
}