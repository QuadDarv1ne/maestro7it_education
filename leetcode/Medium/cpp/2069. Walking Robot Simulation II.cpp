/**
 * https://leetcode.com/problems/walking-robot-simulation-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Walking Robot Simulation II" на C++
 * 
 * Задача: Робот движется по периметру прямоугольника width x height против часовой стрелки.
 *         При шаге, если следующая клетка вне границ, он поворачивает налево (против часовой)
 *         и повторяет попытку. Нужно обрабатывать команды step и возвращать координаты и направление.
 * 
 * Алгоритм:
 * 1. Вычисляем периметр perimeter = 2*(width+height)-4.
 * 2. Предвычисляем для каждой позиции на периметре (0..perimeter-1) координаты и направление.
 *    - Направление: East (0), North (1), West (2), South (3).
 * 3. Храним текущую позицию на периметре (pos) и общее количество пройденных шагов (steps).
 * 4. При step(num): steps += num; pos = steps % perimeter.
 * 5. При getPos/getDir: возвращаем предвычисленные для текущей pos значения.
 * 6. Особый случай: если steps > 0 и pos == 0 (закончили полный круг),
 *    то робот смотрит на South (а не East).
 * 
 * Сложность: O(perimeter) на инициализацию, O(1) на запрос.
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

class Robot {
private:
    int perimeter;
    long long steps; // общее количество шагов
    vector<pair<int,int>> positions; // координаты для каждой позиции на периметре
    vector<int> directions; // направление для каждой позиции на периметре
    
    void buildPerimeter(int width, int height) {
        // Идём по периметру против часовой стрелки
        // East: (0,0) -> (width-1, 0)
        for (int x = 0; x < width; ++x) {
            positions.emplace_back(x, 0);
            directions.push_back(0); // East
        }
        // North: (width-1, 1) -> (width-1, height-1)
        for (int y = 1; y < height; ++y) {
            positions.emplace_back(width - 1, y);
            directions.push_back(1); // North
        }
        // West: (width-2, height-1) -> (0, height-1)
        for (int x = width - 2; x >= 0; --x) {
            positions.emplace_back(x, height - 1);
            directions.push_back(2); // West
        }
        // South: (0, height-2) -> (0, 1)
        for (int y = height - 2; y > 0; --y) {
            positions.emplace_back(0, y);
            directions.push_back(3); // South
        }
    }
    
public:
    Robot(int width, int height) {
        perimeter = 2 * (width + height) - 4;
        steps = 0;
        buildPerimeter(width, height);
    }
    
    void step(int num) {
        steps += num;
    }
    
    vector<int> getPos() {
        if (perimeter == 0) return {0, 0};
        int idx = steps % perimeter;
        return {positions[idx].first, positions[idx].second};
    }
    
    string getDir() {
        if (perimeter == 0) return "East";
        int idx = steps % perimeter;
        // Особый случай: если сделали хотя бы один шаг и вернулись в (0,0)
        if (steps > 0 && idx == 0) {
            return "South";
        }
        switch (directions[idx]) {
            case 0: return "East";
            case 1: return "North";
            case 2: return "West";
            default: return "South";
        }
    }
};