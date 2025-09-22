/**
 * https://leetcode.com/problems/count-elements-with-maximum-frequency/description/?envType=daily-question&envId=2025-09-22
 */

#include <vector>
#include <unordered_map>
using namespace std;

class Solution {
public:
    /**
     * @brief Подсчёт элементов с максимальной частотой встречаемости.
     *
     * Алгоритм:
     * 1. Подсчитать частоты всех элементов массива.
     * 2. Найти максимальное значение частоты.
     * 3. Вернуть количество различных элементов, имеющих эту частоту.
     *
     * @param nums Входной массив целых чисел.
     * @return int Количество элементов с максимальной частотой.
     */
    int maxFrequencyElements(vector<int>& nums) {
        unordered_map<int,int> freq;
        for(int x : nums) freq[x]++;
        int maxFreq = 0;
        for(auto &p : freq) if(p.second > maxFreq) maxFreq = p.second;
        int result = 0;
        for(auto &p : freq) if(p.second == maxFreq) result += p.second;
        return result;
    }
};


/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/