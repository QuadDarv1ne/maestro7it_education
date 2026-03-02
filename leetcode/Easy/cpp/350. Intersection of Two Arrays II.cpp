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
    /**
     * Возвращает пересечение двух массивов с учётом кратности.
     *
     * @param nums1 первый вектор целых чисел
     * @param nums2 второй вектор целых чисел
     * @return вектор, содержащий общие элементы с повторениями
     */
    vector<int> intersect(vector<int>& nums1, vector<int>& nums2) {
        // Для экономии памяти работаем с меньшим массивом
        if (nums1.size() > nums2.size()) {
            return intersect(nums2, nums1);
        }
        
        unordered_map<int, int> freq;
        for (int num : nums1) {
            freq[num]++;
        }
        
        vector<int> result;
        for (int num : nums2) {
            auto it = freq.find(num);
            if (it != freq.end() && it->second > 0) {
                result.push_back(num);
                it->second--;
            }
        }
        
        return result;
    }
};