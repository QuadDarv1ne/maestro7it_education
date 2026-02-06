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

/**
 * @param {string} s
 * @param {string} t
 * @return {boolean}
 */
var isIsomorphic = function(s, t) {
    if (s.length !== t.length) return false;
    
    const sToT = new Map();
    const tToS = new Map();
    
    for (let i = 0; i < s.length; i++) {
        const sChar = s[i];
        const tChar = t[i];
        
        // Проверяем s -> t
        if (sToT.has(sChar)) {
            if (sToT.get(sChar) !== tChar) return false;
        } else {
            sToT.set(sChar, tChar);
        }
        
        // Проверяем t -> s
        if (tToS.has(tChar)) {
            if (tToS.get(tChar) !== sChar) return false;
        } else {
            tToS.set(tChar, sChar);
        }
    }
    
    return true;
};