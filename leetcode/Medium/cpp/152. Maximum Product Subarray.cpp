/**
 * https://leetcode.com/problems/maximum-product-subarray/description/
 * Автор: Дуплей Максим Игоревич
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
    int maxProduct(vector<int>& nums) {
        /*
        Находит максимальное произведение подмассива.
        
        Алгоритм:
        - Поддерживаем два значения: max_prod и min_prod
        - При встрече отрицательного числа меняем их местами
        - На каждом шаге обновляем результат
        */
        
        if (nums.empty()) return 0;
        
        int max_prod = nums[0];
        int min_prod = nums[0];
        int result = nums[0];
        
        for (int i = 1; i < nums.size(); i++) {
            int current = nums[i];
            
            // Если число отрицательное, меняем местами max и min
            if (current < 0) {
                swap(max_prod, min_prod);
            }
            
            // Обновляем максимальное и минимальное произведение
            max_prod = max(current, max_prod * current);
            min_prod = min(current, min_prod * current);
            
            // Обновляем результат
            result = max(result, max_prod);
        }
        
        return result;
    }
};