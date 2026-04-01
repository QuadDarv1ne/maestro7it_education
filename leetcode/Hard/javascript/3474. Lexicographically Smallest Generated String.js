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
 * Строит лексикографически наименьшую строку, удовлетворяющую условиям.
 * 
 * @param {string} str1
 * @param {string} str2
 * @return {string}
 */

var generateString = function(str1, str2) {
    const n = str1.length;
    const m = str2.length;
    const len = n + m - 1;
    
    const s = new Array(len).fill('');
    
    // Фиксируем все 'T' позиции
    for (let i = 0; i < n; i++) {
        if (str1[i] === 'T') {
            for (let j = 0; j < m; j++) {
                const idx = i + j;
                if (s[idx] === '') {
                    s[idx] = str2[j];
                } else if (s[idx] !== str2[j]) {
                    return "";
                }
            }
        }
    }
    
    // Проверяем 'F' позиции на конфликты
    for (let i = 0; i < n; i++) {
        if (str1[i] === 'F') {
            let match = true;
            for (let j = 0; j < m; j++) {
                const idx = i + j;
                if (s[idx] === '') {
                    match = false;
                    break;
                }
                if (s[idx] !== str2[j]) {
                    match = false;
                    break;
                }
            }
            if (match) {
                return "";
            }
        }
    }
    
    // Заполняем пустые позиции 'a'
    for (let i = 0; i < len; i++) {
        if (s[i] === '') {
            s[i] = 'a';
        }
    }
    
    // Обрабатываем 'F' позиции, где подстрока стала равна str2
    for (let i = 0; i < n; i++) {
        if (str1[i] === 'F') {
            let equal = true;
            for (let j = 0; j < m; j++) {
                if (s[i + j] !== str2[j]) {
                    equal = false;
                    break;
                }
            }
            if (equal) {
                let changed = false;
                for (let j = m - 1; j >= 0; j--) {
                    const idx = i + j;
                    if (s[idx] < 'z') {
                        s[idx] = String.fromCharCode(s[idx].charCodeAt(0) + 1);
                        changed = true;
                        break;
                    }
                }
                if (!changed) {
                    return "";
                }
            }
        }
    }
    
    // Финальная проверка
    const result = s.join('');
    for (let i = 0; i < n; i++) {
        const sub = result.substring(i, i + m);
        if (str1[i] === 'T' && sub !== str2) {
            return "";
        }
        if (str1[i] === 'F' && sub === str2) {
            return "";
        }
    }
    
    return result;
};