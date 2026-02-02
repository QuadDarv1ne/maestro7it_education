/**
 * Решение задачи LeetCode № 3013: "Divide an Array Into Subarrays With Minimum Cost II"
 * https://leetcode.com/problems/divide-an-array-into-subarrays-with-minimum-cost-ii/description/
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
    long long minimumCost(vector<int>& nums, int k, int dist) {
        int n = nums.size();
        if (k == 1) return nums[0];
        
        multiset<int> selected;    // k-1 наименьших элементов
        multiset<int> candidates;  // остальные элементы
        long long selected_sum = 0;
        
        // Инициализация первого окна [1, dist+1]
        vector<int> window;
        for (int i = 1; i < min(n, dist + 2); i++) {
            window.push_back(nums[i]);
        }
        sort(window.begin(), window.end());
        
        for (int i = 0; i < min((int)window.size(), k - 1); i++) {
            selected.insert(window[i]);
            selected_sum += window[i];
        }
        for (int i = k - 1; i < window.size(); i++) {
            candidates.insert(window[i]);
        }
        
        long long min_cost = nums[0] + selected_sum;
        
        // Скользим окном
        for (int right = dist + 2; right < n; right++) {
            int left = right - dist - 1;
            int out_val = nums[left];
            int in_val = nums[right];
            
            // Удаляем выходящий элемент
            auto it = selected.find(out_val);
            if (it != selected.end()) {
                selected.erase(it);
                selected_sum -= out_val;
                
                // Пополняем из candidates
                if (!candidates.empty()) {
                    int val = *candidates.begin();
                    candidates.erase(candidates.begin());
                    selected.insert(val);
                    selected_sum += val;
                }
            } else {
                it = candidates.find(out_val);
                if (it != candidates.end()) {
                    candidates.erase(it);
                }
            }
            
            // Добавляем входящий элемент
            if (selected.size() < k - 1) {
                selected.insert(in_val);
                selected_sum += in_val;
            } else if (in_val < *selected.rbegin()) {
                // Новый элемент меньше максимального в selected
                int max_val = *selected.rbegin();
                selected.erase(selected.find(max_val));
                selected_sum -= max_val;
                candidates.insert(max_val);
                
                selected.insert(in_val);
                selected_sum += in_val;
            } else {
                candidates.insert(in_val);
            }
            
            min_cost = min(min_cost, (long long)nums[0] + selected_sum);
        }
        
        return min_cost;
    }
};