/**
 * https://leetcode.com/problems/vowel-spellchecker/description/?envType=daily-question&envId=2025-09-14
 */

/**
 * Решение задачи Vowel Spellchecker.
 * 
 * Для каждого запроса из queries ищем слово в wordlist по следующим правилам:
 * 1. Точное совпадение.
 * 2. Совпадение без учета регистра (первое найденное).
 * 3. Совпадение с заменой всех гласных на '*' (первое найденное).
 * 4. Если ничего не найдено, возвращаем пустую строку.
 */
var spellchecker = function(wordlist, queries) {
    // Создаем множество для точных совпадений
    const exact = new Set(wordlist);
    // Словарь для регистра-независимого поиска: ключ — слово в нижнем регистре, значение — первое слово из wordlist
    const caseInsensitive = new Map();
    // Словарь для поиска с заменой гласных на '*': ключ — строка с замененными гласными, значение — первое слово
    const vowelInsensitive = new Map();
    
    for (const word of wordlist) {
        const lower = word.toLowerCase();
        // Если в caseInsensitive еще нет этого ключа, добавляем
        if (!caseInsensitive.has(lower)) {
            caseInsensitive.set(lower, word);
        }
        // Заменяем гласные на * в lower с помощью регулярного выражения
        const vowelKey = lower.replace(/[aeiou]/g, '*');
        if (!vowelInsensitive.has(vowelKey)) {
            vowelInsensitive.set(vowelKey, word);
        }
    }
    
    const result = [];
    for (const query of queries) {
        // Проверяем точное совпадение
        if (exact.has(query)) {
            result.push(query);
            continue;
        }
        const lowerQuery = query.toLowerCase();
        // Проверяем регистра-независимое совпадение
        if (caseInsensitive.has(lowerQuery)) {
            result.push(caseInsensitive.get(lowerQuery));
            continue;
        }
        // Заменяем гласные на * в lowerQuery
        const vowelQuery = lowerQuery.replace(/[aeiou]/g, '*');
        if (vowelInsensitive.has(vowelQuery)) {
            result.push(vowelInsensitive.get(vowelQuery));
        } else {
            result.push('');
        }
    }
    return result;
};

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/