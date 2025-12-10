/* ========================== C++ ========================== */

/*
 * LeetCode 77: Combinations
 * https://leetcode.com/problems/combinations/
 * 
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. YouTube канал: https://www.youtube.com/@it-coders
 * 6. ВК группа: https://vk.com/science_geeks
 */

#include <vector>
using namespace std;

class Solution {
public:
    /**
     * Генерирует все комбинации из k чисел в диапазоне [1, n].
     * 
     * Time Complexity: O(C(n,k) * k)
     * Space Complexity: O(k)
     */
    vector<vector<int>> combine(int n, int k) {
        vector<vector<int>> result;
        vector<int> path;
        backtrack(n, k, 1, path, result);
        return result;
    }
    
private:
    void backtrack(int n, int k, int start, 
                   vector<int>& path, vector<vector<int>>& result) {
        // Базовый случай: комбинация готова
        if (path.size() == k) {
            result.push_back(path);
            return;
        }
        
        // Оптимизация: i <= n - (k - path.size()) + 1
        for (int i = start; i <= n - (k - static_cast<int>(path.size())) + 1; i++) {
            // Выбираем число i
            path.push_back(i);
            
            // Рекурсивно строим остальную часть
            backtrack(n, k, i + 1, path, result);
            
            // Откатываем выбор (backtracking)
            path.pop_back();
        }
    }
};