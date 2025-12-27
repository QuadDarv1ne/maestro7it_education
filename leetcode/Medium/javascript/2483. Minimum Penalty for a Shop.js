/*
https://leetcode.com/problems/minimum-penalty-for-a-shop/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

/**
 * Находит оптимальный час закрытия магазина для минимизации штрафа.
 * 
 * @param {string} customers - строка из 'Y' и 'N'
 * @return {number} - час закрытия с минимальным штрафом
 */
var bestClosingTime = function(customers) {
    const n = customers.length;
    
    // Считаем общее количество клиентов
    let totalY = 0;
    for (let i = 0; i < n; i++) {
        if (customers[i] === 'Y') totalY++;
    }
    
    // Инициализируем
    let currentPenalty = totalY;  // если закроем в час 0
    let minPenalty = currentPenalty;
    let bestHour = 0;
    
    // Проходим по всем возможным часам закрытия
    for (let hour = 1; hour <= n; hour++) {
        // Обновляем штраф для текущего часа закрытия
        if (customers[hour - 1] === 'N') {
            // Магазин был открыт в этот час без клиентов
            currentPenalty++;
        } else {  // customers[hour - 1] === 'Y'
            // Больше не считаем этого клиента в закрытое время
            currentPenalty--;
        }
        
        // Проверяем, не нашли ли лучший час
        if (currentPenalty < minPenalty) {
            minPenalty = currentPenalty;
            bestHour = hour;
        }
    }
    
    return bestHour;
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