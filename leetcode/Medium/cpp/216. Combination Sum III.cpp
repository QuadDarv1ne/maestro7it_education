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

class Solution {
public:
    vector<vector<int>> combinationSum3(int k, int n) {
        vector<vector<int>> result;
        vector<int> current;
        backtrack(1, k, n, current, result);
        return result;
    }
    
private:
    void backtrack(int start, int k, int remaining, 
                   vector<int>& current, vector<vector<int>>& result) {
        // Если комбинация достигла нужной длины
        if (current.size() == k) {
            // Если остаток суммы равен 0 - нашли решение
            if (remaining == 0) {
                result.push_back(current);
            }
            return;
        }
        
        // Если осталось слишком мало чисел или сумма слишком мала/велика
        int remaining_numbers = k - current.size();
        
        // Раннее отсечение: проверка возможности достичь remaining
        if (remaining < start * remaining_numbers + 
                       remaining_numbers * (remaining_numbers - 1) / 2 ||
            remaining > 9 * remaining_numbers - 
                       remaining_numbers * (remaining_numbers - 1) / 2) {
            return;
        }
        
        // Перебираем возможные числа
        for (int num = start; num <= 9; num++) {
            // Если число слишком большое для оставшейся суммы
            if (num > remaining) break;
            
            current.push_back(num);
            backtrack(num + 1, k, remaining - num, current, result);
            current.pop_back();
        }
    }
};