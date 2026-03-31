/**
 * https://leetcode.com/problems/lexicographically-smallest-generated-string/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "3474. Lexicographically Smallest Generated String" на JavaScript
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
 * @param {string} str1
 * @param {string} str2
 * @return {string}
 */
var generateString = function(str1, str2) {
    const n = str1.length, m = str2.length, L = n + m - 1;
    const word = new Array(L).fill(-1); // -1 = символ не определен
    
    // Шаг 1: Фиксируем символы из T-условий
    for (let i = 0; i < n; i++) {
        if (str1[i] === 'T') {
            for (let k = 0; k < m; k++) {
                const pos = i + k;
                if (pos >= L) return "";
                if (word[pos] !== -1 && word[pos] !== str2.charCodeAt(k)) return "";
                word[pos] = str2.charCodeAt(k);
            }
        }
    }
    
    // Лямбда: совпало бы при заполнении пустот 'a'?
    const wouldMatchIfA = (i) => {
        for (let k = 0; k < m; k++) {
            const pos = i + k;
            if (pos >= L) return false;
            if (word[pos] === -1) {
                if (str2[k] !== 'a') return false;
            } else {
                if (word[pos] !== str2.charCodeAt(k)) return false;
            }
        }
        return true;
    };
    
    // Лямбда: крайняя правая пустая позиция в подстроке
    const getRightmostUndef = (i) => {
        let r = -1;
        for (let k = 0; k < m; k++) {
            const pos = i + k;
            if (pos < L && word[pos] === -1) r = pos;
        }
        return r;
    };
    
    // Шаг 2: Ищем скрытые конфликты
    const violated = [];
    for (let i = 0; i < n; i++) {
        if (str1[i] === 'F' && wouldMatchIfA(i)) {
            const r = getRightmostUndef(i);
            if (r === -1) return "";
            violated.push([i, r]);
        }
    }
    
    // Сортируем по правой позиции
    violated.sort((a, b) => a[1] - b[1]);
    
    // Шаг 3: Жадное исправление (массив active хранит отсортированные индексы поставленных 'b')
    const active = [];
    for (const [i, r] of violated) {
        // Бинарный поиск первой 'b' >= i
        let idx = active.findIndex(bPos => bPos >= i);
        
        // Если такой 'b' нет, или она стоит правее текущего F-окна
        if (idx === -1 || active[idx] > i + m - 1) {
            // Вставляем 'b' в sorted массив
            let insIdx = active.findIndex(bPos => bPos >= r);
            if (insIdx === -1) active.push(r);
            else active.splice(insIdx, 0, r);
            
            word[r] = 'b'.charCodeAt(0);
        }
    }
    
    // Шаг 4: Финальная сборка
    return word.map(c => String.fromCharCode(c === -1 ? 'a'.charCodeAt(0) : c)).join('');
};