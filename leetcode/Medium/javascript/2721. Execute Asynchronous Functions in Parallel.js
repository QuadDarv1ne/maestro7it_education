/**
 * https://leetcode.com/problems/house-robber-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "2721. Execute Asynchronous Functions in Parallel"
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

var promiseAll = function(functions) {
    return new Promise((resolve, reject) => {
        const results = new Array(functions.length); // Массив для результатов
        let completedCount = 0;                       // Счётчик выполненных

        functions.forEach((fn, index) => {
            // Вызываем функцию, получаем промис
            fn()
                .then(result => {
                    results[index] = result;          // Сохраняем результат по индексу
                    completedCount++;                  // Увеличиваем счётчик

                    // Если все промисы выполнены, разрешаем итоговый промис
                    if (completedCount === functions.length) {
                        resolve(results);
                    }
                })
                .catch(error => {
                    reject(error); // При первой ошибке отклоняем итоговый промис
                });
        });

        // Важно: Если массив functions пуст, нужно сразу разрешить промис с пустым массивом
        if (functions.length === 0) {
            resolve([]);
        }
    });
};