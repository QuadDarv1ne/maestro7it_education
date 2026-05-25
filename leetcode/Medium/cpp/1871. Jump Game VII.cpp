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
 */

#include <vector>
#include <string>

class Solution {
public:
    /**
     * @brief Решение задачи Jump Game VII.
     * 
     * Функция проверяет достижимость последнего индекса строки.
     * Используется подход динамического программирования со скользящим окном
     * для оптимизации подсчета доступных предыдущих позиций.
     * 
     * @param s Бинарная строка ('0' и '1').
     * @param minJump Минимальная длина прыжка.
     * @param maxJump Максимальная длина прыжка.
     * @return true Если последний индекс достижим.
     * @return false Иначе.
     */
    bool canReach(std::string s, int minJump, int maxJump) {
        int n = s.length();
        // Используем vector<int> для быстрой работы, 1 = достижимо, 0 = нет
        std::vector<int> dp(n, 0);
        dp[0] = 1;
        
        int count = 0;
        
        for (int i = 1; i < n; ++i) {
            // Добавляем в count новые достижимые позиции, входящие в правую границу окна
            if (i >= minJump) {
                count += dp[i - minJump];
            }
            // Вычитаем позиции, которые выходят за левую границу окна
            if (i > maxJump) {
                count -= dp[i - maxJump - 1];
            }
            
            // Если s[i] == '0' и count > 0, значит мы можем попасть в i
            if (s[i] == '0' && count > 0) {
                dp[i] = 1;
            }
        }
        
        return dp[n - 1];
    }
};