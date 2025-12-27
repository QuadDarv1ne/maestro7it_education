/*
https://leetcode.com/problems/minimum-penalty-for-a-shop/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

public class Solution {
    public int BestClosingTime(string customers) {
        int n = customers.Length;
        
        // Считаем общее количество клиентов
        int totalY = 0;
        foreach (char c in customers) {
            if (c == 'Y') totalY++;
        }
        
        // Инициализируем
        int currentPenalty = totalY;  // если закроем в час 0
        int minPenalty = currentPenalty;
        int bestHour = 0;
        
        // Проходим по всем возможным часам закрытия
        for (int hour = 1; hour <= n; hour++) {
            // Обновляем штраф для текущего часа закрытия
            if (customers[hour - 1] == 'N') {
                // Магазин был открыт в этот час без клиентов
                currentPenalty++;
            } else {  // customers[hour - 1] == 'Y'
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
    }
}

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