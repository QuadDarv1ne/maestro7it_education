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
#include <set>
#include <algorithm>
#include <climits>

using namespace std;

class Solution {
public:
    vector<vector<int>> minAbsDiff(vector<vector<int>>& grid, int k) {
        int m = grid.size();
        int n = grid[0].size();
        int rows = m - k + 1;
        int cols = n - k + 1;
        
        vector<vector<int>> result(rows, vector<int>(cols, 0));
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                // Используем set для хранения уникальных значений
                set<int> uniqueVals;
                for (int x = i; x < i + k; x++) {
                    for (int y = j; y < j + k; y++) {
                        uniqueVals.insert(grid[x][y]);
                    }
                }
                
                // Если все значения одинаковы
                if (uniqueVals.size() == 1) {
                    result[i][j] = 0;
                    continue;
                }
                
                // set уже хранит значения в отсортированном порядке
                // Ищем минимальную разность между соседними элементами
                int minDiff = INT_MAX;
                auto prev = uniqueVals.begin();
                for (auto curr = next(prev); curr != uniqueVals.end(); ++curr) {
                    int diff = *curr - *prev;
                    if (diff < minDiff) {
                        minDiff = diff;
                    }
                    prev = curr;
                }
                
                result[i][j] = minDiff;
            }
        }
        
        return result;
    }
};