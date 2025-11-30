/**
 * https://leetcode.com/problems/count-and-say/description/
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Count and Say" на JavaScript
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

var countAndSay = function(n) {
    if (n === 1) return "1";
    
    let result = "1";
    
    for (let i = 2; i <= n; i++) {
        let current = "";
        let count = 1;
        let prevChar = result[0];
        
        for (let j = 1; j < result.length; j++) {
            if (result[j] === prevChar) {
                count++;
            } else {
                current += count + prevChar;
                count = 1;
                prevChar = result[j];
            }
        }
        
        current += count + prevChar;
        result = current;
    }
    
    return result;
};