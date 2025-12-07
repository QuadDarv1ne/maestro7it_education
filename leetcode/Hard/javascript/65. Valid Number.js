/**
 * @param {string} s
 * @return {boolean}
 */
var isNumber = function(s) {
    /**
     * Автор: Дуплей Максим Игоревич
     * ORCID: https://orcid.org/0009-0007-7605-539X
     * GitHub: https://github.com/QuadDarv1ne/
     * 
     * Задача: Valid Number (LeetCode)
     * Алгоритм: Валидация числа через конечный автомат (флаги)
     * Сложность: O(n) по времени, O(1) по памяти
     * 
     * Идея решения:
     * 1. Используем флаги для отслеживания: цифр, точки, экспоненты
     * 2. Проверяем каждый символ согласно правилам валидного числа
     * 3. Знак может быть только в начале или после 'e'/'E'
     * 4. Точка не может быть после 'e'/'E' или повторяться
     * 5. 'e'/'E' требует хотя бы одну цифру до себя
     */
    
    let hasDigit = false;    // Есть ли цифры
    let hasPoint = false;    // Есть ли точка
    let hasE = false;        // Есть ли экспонента
    
    for (let i = 0; i < s.length; i++) {
        const c = s[i];
        
        if (c >= '0' && c <= '9') {
            hasDigit = true;
        }
        else if (c === '.') {
            // Точка не может быть после 'e' или повторяться
            if (hasE || hasPoint) {
                return false;
            }
            hasPoint = true;
        }
        else if (c === 'e' || c === 'E') {
            // 'e' требует цифру до себя и не может повторяться
            if (hasE || !hasDigit) {
                return false;
            }
            hasE = true;
            hasDigit = false; // После 'e' должна быть хотя бы одна цифра
        }
        else if (c === '+' || c === '-') {
            // Знак только в начале или сразу после 'e'
            if (i > 0 && s[i-1] !== 'e' && s[i-1] !== 'E') {
                return false;
            }
        }
        else {
            // Недопустимый символ
            return false;
        }
    }
    
    return hasDigit;
};

/*
 * Полезные ссылки автора:
 * Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * Telegram: @quadd4rv1n7, @dupley_maxim_1999
 * Rutube: https://rutube.ru/channel/4218729/
 * Plvideo: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * YouTube: https://www.youtube.com/@it-coders
 * VK: https://vk.com/science_geeks
 */