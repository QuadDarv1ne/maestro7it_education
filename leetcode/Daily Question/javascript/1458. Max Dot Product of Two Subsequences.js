/**
 * Максимальное скалярное произведение двух подпоследовательностей
 * 
 * @param {number[]} nums1 - Первый массив целых чисел
 * @param {number[]} nums2 - Второй массив целых чисел
 * @return {number} Максимальное скалярное произведение
 * 
 * Сложность: Время O(m*n), Память O(m*n)
 * 
 * Автор: Дуплей Максим Игоревич
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
var maxDotProduct = function(nums1, nums2) {
    const m = nums1.length;
    const n = nums2.length;
    
    // Создаем DP таблицу с отрицательной бесконечностью
    const dp = Array(m + 1).fill().map(() => Array(n + 1).fill(-Infinity));
    
    // Заполняем таблицу DP
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            const product = nums1[i - 1] * nums2[j - 1];
            
            // 4 варианта выбора:
            // 1. Только текущее произведение
            // 2. Добавить к предыдущей подпоследовательности
            // 3. Пропустить элемент nums1
            // 4. Пропустить элемент nums2
            dp[i][j] = Math.max(
                product,
                dp[i - 1][j - 1] + product,
                dp[i - 1][j],
                dp[i][j - 1]
            );
        }
    }
    
    return dp[m][n];
};