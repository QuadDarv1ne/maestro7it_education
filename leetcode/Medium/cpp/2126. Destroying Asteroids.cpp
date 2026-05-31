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
#include <algorithm>

class Solution {
public:
    /**
     * Определяет, сможет ли планета уничтожить все астероиды.
     * 
     * Планета может уничтожить астероид, если её текущая масса больше или равна
     * массе астероида. После уничтожения масса планеты увеличивается на массу
     * астероида. Астероиды можно уничтожать в любом порядке.
     * 
     * @param mass Начальная масса планеты
     * @param asteroids Вектор масс астероидов
     * @return true если все астероиды могут быть уничтожены, иначе false
     * 
     * Примеры:
     *   asteroidsDestroyed(10, {3, 9, 19, 5, 21}) -> true
     *   asteroidsDestroyed(5, {4, 9, 23, 4}) -> false
     * 
     * Алгоритм:
     *   1. Сортируем астероиды по возрастанию массы
     *   2. Жадно уничтожаем самые маленькие доступные
     *   3. Если текущая масса меньше массы астероида — невозможно уничтожить все
     * 
     * Сложность:
     *   Время: O(n log n) — сортировка
     *   Память: O(1)
     */
    bool asteroidsDestroyed(int mass, std::vector<int>& asteroids) {
        std::sort(asteroids.begin(), asteroids.end());
        long long current_mass = mass;
        
        for (int asteroid : asteroids) {
            if (current_mass >= asteroid) {
                current_mass += asteroid;
            } else {
                return false;
            }
        }
        
        return true;
    }
};