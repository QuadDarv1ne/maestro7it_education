/**
 * Вычисляет максимальную сумму счастья выбранных детей.
 * 
 * @param {number[]} happiness - массив значений счастья
 * @param {number} k - количество детей для выбора
 * @return {number} - максимальная сумма счастья
 * 
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 */
var maximumHappinessSum = function(happiness, k) {
    // Сортируем по убыванию
    happiness.sort((a, b) => b - a);
    
    // Суммируем первые k элементов с учетом уменьшения
    let total = 0;
    for (let i = 0; i < k; i++) {
        // Текущее счастье после i уменьшений
        const current = Math.max(0, happiness[i] - i);
        total += current;
    }
    
    return total;
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