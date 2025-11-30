/**
 * https://leetcode.com/problems/n-queens-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "N-Queens II" на C++
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

#include <unordered_set>
using namespace std;

class Solution {
public:
    int totalNQueens(int n) {
        unordered_set<int> cols, diagonals, anti_diagonals;
        return backtrack(0, cols, diagonals, anti_diagonals, n);
    }
    
private:
    int backtrack(int row, unordered_set<int>& cols, unordered_set<int>& diagonals, 
                  unordered_set<int>& anti_diagonals, int n) {
        if (row == n) {
            return 1;
        }
        
        int count = 0;
        for (int col = 0; col < n; col++) {
            int curr_diagonal = row - col;
            int curr_anti_diagonal = row + col;
            
            if (cols.count(col) || diagonals.count(curr_diagonal) || 
                anti_diagonals.count(curr_anti_diagonal)) {
                continue;
            }
            
            cols.insert(col);
            diagonals.insert(curr_diagonal);
            anti_diagonals.insert(curr_anti_diagonal);
            
            count += backtrack(row + 1, cols, diagonals, anti_diagonals, n);
            
            cols.erase(col);
            diagonals.erase(curr_diagonal);
            anti_diagonals.erase(curr_anti_diagonal);
        }
        
        return count;
    }
};