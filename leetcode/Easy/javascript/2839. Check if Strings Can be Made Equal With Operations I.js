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
 * 
 * @param {string} s1
 * @param {string} s2
 * @return {boolean}
 */

var canBeEqual = function(s1, s2) {
    // Проверяем мультимножества символов на позициях (0,2) и (1,3)
    
    // Для позиций 0 и 2
    const pair1_02 = [s1[0], s1[2]].sort().join('');
    const pair2_02 = [s2[0], s2[2]].sort().join('');
    if (pair1_02 !== pair2_02) {
        return false;
    }
    
    // Для позиций 1 и 3
    const pair1_13 = [s1[1], s1[3]].sort().join('');
    const pair2_13 = [s2[1], s2[3]].sort().join('');
    if (pair1_13 !== pair2_13) {
        return false;
    }
    
    return true;
};