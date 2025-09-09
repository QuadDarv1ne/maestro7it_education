/**
 * https://leetcode.com/problems/number-of-people-aware-of-a-secret/description/?envType=daily-question&envId=2025-09-09
 */

// JavaScript
/**
 * Функция peopleAwareOfSecret вычисляет количество людей,
 * которые знают секрет к n-му дню.
 * Каждый человек начинает делиться секретом через delay дней
 * и забывает его через forget дней.
 * Используется динамическое программирование.
 * Результат возвращается по модулю 1e9+7.
 *
 * @param {number} n - количество дней
 * @param {number} delay - через сколько дней после узнания человек начинает делиться
 * @param {number} forget - через сколько дней человек забывает секрет
 * @return {number} - количество людей, знающих секрет на n-й день
 */
var peopleAwareOfSecret = function(n, delay, forget) {
    const MOD = 1e9 + 7;
    const dp = new Array(n + 1).fill(0);
    dp[1] = 1;
    let sumSharing = 0;
    let result = 0;
    
    for (let day = 2; day <= n; day++) {
        if (day - delay >= 1) sumSharing = (sumSharing + dp[day - delay]) % MOD;
        if (day - forget >= 1) sumSharing = (sumSharing - dp[day - forget] + MOD) % MOD;
        dp[day] = sumSharing;
    }

    for (let day = n - forget + 1; day <= n; day++) {
        if (day >= 1) result = (result + dp[day]) % MOD;
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