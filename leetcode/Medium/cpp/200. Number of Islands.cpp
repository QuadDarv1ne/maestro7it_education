/**
 * https://leetcode.com/problems/number-of-islands/description/
 */

#include <vector>
using namespace std;

class Solution {
public:
    /**
     * Считает количество островов на карте.
     *
     * Алгоритм:
     * 1. Пробегаем все клетки grid.
     * 2. Если встречаем '1' (земля), увеличиваем счетчик островов.
     * 3. Запускаем DFS, чтобы пометить все смежные клетки как посещённые ('0').
     * 4. DFS рекурсивно проходит вверх, вниз, влево и вправо.
     *
     * @param grid Двумерный массив символов '1' и '0'
     * @return количество островов
     */
    int numIslands(vector<vector<char>>& grid) {
        if (grid.empty()) return 0;
        int count = 0;
        int rows = grid.size(), cols = grid[0].size();
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (grid[i][j] == '1') {
                    count++;
                    dfs(grid, i, j, rows, cols);
                }
            }
        }
        return count;
    }
    
private:
    void dfs(vector<vector<char>>& grid, int i, int j, int rows, int cols) {
        if (i < 0 || i >= rows || j < 0 || j >= cols || grid[i][j] == '0') return;
        grid[i][j] = '0'; // помечаем клетку как посещённую
        dfs(grid, i+1, j, rows, cols);
        dfs(grid, i-1, j, rows, cols);
        dfs(grid, i, j+1, rows, cols);
        dfs(grid, i, j-1, rows, cols);
    }
};

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/