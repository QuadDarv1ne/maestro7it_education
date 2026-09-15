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
#include <cmath>

using namespace std;

class Solution {
public:
    /*
     * Возвращает минимальное количество операций, чтобы все элементы сетки стали равны.
     * За одну операцию можно прибавить x или вычесть x из любого элемента.
     * Если это невозможно, возвращает -1.
     *
     * https://leetcode.com/problems/minimum-operations-to-make-a-uni-value-grid/description/?envType=daily-question&envId=2026-04-28
     * 
     * @param grid двумерный вектор целых чисел
     * @param x    целое число, шаг изменения
     * @return     минимальное число операций или -1
     */
    int minOperations(vector<vector<int>>& grid, int x) {
        // Разворачиваем в одномерный массив
        vector<int> flat;
        for (auto& row : grid)
            for (int val : row)
                flat.push_back(val);
        
        // Проверяем, что у всех элементов одинаковый остаток от деления на x
        int remainder = flat[0] % x;
        for (int val : flat) {
            if (val % x != remainder)
                return -1;
        }
        
        // Сортируем и находим медиану
        sort(flat.begin(), flat.end());
        int median = flat[flat.size() / 2];
        
        // Считаем общее количество операций
        long long ops = 0;   // на случай большого ответа
        for (int val : flat)
            ops += abs(val - median) / x;
        
        return (int)ops;
    }
};