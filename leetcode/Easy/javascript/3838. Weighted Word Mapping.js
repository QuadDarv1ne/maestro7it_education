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
 * @param {string[]} words
 * @param {number[]} weights
 * @return {string}
 */
var mapWordWeights = function(words, weights) {
    let result = "";
    
    for (const word of words) {
        let sum = 0;
        
        // Вычисляем вес слова
        for (const c of word) {
            const index = c.charCodeAt(0) - 'a'.charCodeAt(0);
            sum += weights[index];
        }
        
        // Остаток от деления
        const rem = sum % 26;
        
        // Маппинг: 0 -> 'z', 25 -> 'a'
        // Код 'z' равен 122. 122 - rem даст нужный символ.
        const mappedChar = String.fromCharCode('z'.charCodeAt(0) - rem);
        
        result += mappedChar;
    }
    
    return result;
};