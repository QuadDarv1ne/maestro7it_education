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
using namespace std;

class Solution {
public:
    /**
     * Находит все элементы, которые встречаются более чем ⌊ n/3 ⌋ раз.
     * 
     * Алгоритм (алгоритм Бойера-Мура для k = n/3):
     * 1. Не может быть более 2 элементов, удовлетворяющих условию.
     * 2. Используем двух кандидатов и их счетчики.
     * 3. Первый проход: находим двух кандидатов.
     * 4. Второй проход: проверяем, действительно ли кандидаты встречаются > n/3 раз.
     * 
     * Сложность:
     * Время: O(n), два прохода по массиву
     * Пространство: O(1), используем только фиксированное количество переменных
     * 
     * @param nums Входной массив целых чисел
     * @return Вектор элементов, встречающихся более чем ⌊ n/3 ⌋ раз
     * 
     * Примеры:
     * majorityElement({3,2,3}) → {3}
     * majorityElement({1}) → {1}
     * majorityElement({1,2}) → {1,2}
     * majorityElement({1,1,1,3,3,2,2,2}) → {1,2}
     */
    vector<int> majorityElement(vector<int>& nums) {
        vector<int> result;
        if (nums.empty()) {
            return result;
        }
        
        // Инициализация кандидатов и счетчиков
        int candidate1 = 0, candidate2 = 0;
        int count1 = 0, count2 = 0;
        
        // Первый проход: поиск кандидатов
        for (int num : nums) {
            if (count1 > 0 && num == candidate1) {
                count1++;
            } else if (count2 > 0 && num == candidate2) {
                count2++;
            } else if (count1 == 0) {
                candidate1 = num;
                count1 = 1;
            } else if (count2 == 0) {
                candidate2 = num;
                count2 = 1;
            } else {
                count1--;
                count2--;
            }
        }
        
        // Второй проход: проверка кандидатов
        count1 = 0;
        count2 = 0;
        int n = nums.size();
        
        for (int num : nums) {
            if (num == candidate1) {
                count1++;
            } else if (num == candidate2) {
                count2++;
            }
        }
        
        if (count1 > n / 3) {
            result.push_back(candidate1);
        }
        if (count2 > n / 3) {
            result.push_back(candidate2);
        }
        
        return result;
    }
    
    /**
     * Решение с использованием unordered_map (не соответствует ограничению O(1) памяти).
     * 
     * @param nums Входной массив
     * @return Вектор элементов, встречающихся более чем ⌊ n/3 ⌋ раз
     */
    vector<int> majorityElementHashMap(vector<int>& nums) {
        vector<int> result;
        if (nums.empty()) {
            return result;
        }
        
        unordered_map<int, int> counter;
        int n = nums.size();
        
        for (int num : nums) {
            counter[num]++;
        }
        
        for (auto& [num, count] : counter) {
            if (count > n / 3) {
                result.push_back(num);
            }
        }
        
        return result;
    }
};