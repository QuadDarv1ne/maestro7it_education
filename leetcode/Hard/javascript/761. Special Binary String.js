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
 * Преобразует специальную двоичную строку в лексикографически наибольшую.
 * @param {string} s - исходная специальная строка (например, "11011000")
 * @return {string} - максимально возможная строка после перестановок (например, "11100100")
 */
var makeLargestSpecial = function(s) {
    const dfs = (str) => {
        if (str.length === 0) return "";
        
        const groups = [];
        let balance = 0;
        let left = 0;
        
        for (let i = 0; i < str.length; i++) {
            balance += str[i] === '1' ? 1 : -1;
            if (balance === 0) {
                // Обрабатываем внутренность без первого и последнего символа
                const inner = dfs(str.substring(left + 1, i));
                groups.push("1" + inner + "0");
                left = i + 1;
            }
        }
        
        // Сортируем группы по убыванию (лексикографически)
        groups.sort((a, b) => b.localeCompare(a));
        return groups.join('');
    };
    
    return dfs(s);
};