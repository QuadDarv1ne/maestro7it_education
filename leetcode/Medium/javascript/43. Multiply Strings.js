/**
 * https://leetcode.com/problems/multiply-strings/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Multiply Strings" на JavaScript
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

var multiply = function(num1, num2) {
    if (num1 === "0" || num2 === "0") return "0";
    
    const m = num1.length, n = num2.length;
    const res = new Array(m + n).fill(0);
    
    for (let i = m - 1; i >= 0; i--) {
        for (let j = n - 1; j >= 0; j--) {
            const mul = (num1.charAt(i) - '0') * (num2.charAt(j) - '0');
            const p1 = i + j, p2 = i + j + 1;
            const sum = mul + res[p2];
            
            res[p2] = sum % 10;
            res[p1] += Math.floor(sum / 10);
        }
    }
    
    let result = '';
    for (let num of res) {
        if (!(result === '' && num === 0)) {
            result += num.toString();
        }
    }
    
    return result === '' ? "0" : result;
};