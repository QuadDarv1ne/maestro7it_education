/**
 * Находит минимальное количество удалений пар элементов, чтобы оставшийся массив был отсортирован в неубывающем порядке.
 * 
 * Алгоритм:
 * 1. Используем динамическое программирование для поиска самой длинной неубывающей подпоследовательности.
 * 2. Подпоследовательность должна иметь ту же четность длины, что и исходный массив.
 * 3. Удаление происходит парами, поэтому количество удаленных элементов должно быть четным.
 * 
 * @param nums Входной массив целых чисел
 * @return Минимальное количество удалений пар
 * 
 * Сложность по времени: O(n²)
 * Сложность по памяти: O(n)
 *
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
// ==================== C++ ====================

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    /**
     * Возвращает минимальное количество операций для сортировки массива.
     * 
     * Операция: выбрать соседнюю пару с минимальной суммой (самую левую при равенстве),
     * заменить пару на их сумму.
     */
    int minimumPairRemoval(vector<int>& nums) {
        vector<int> arr = nums;
        int operations = 0;
        
        while (!isNonDecreasing(arr)) {
            int minSum = arr[0] + arr[1];
            int minIndex = 0;
            
            for (int i = 1; i < arr.size() - 1; i++) {
                int currentSum = arr[i] + arr[i + 1];
                if (currentSum < minSum) {
                    minSum = currentSum;
                    minIndex = i;
                }
            }
            
            arr[minIndex] = minSum;
            arr.erase(arr.begin() + minIndex + 1);
            operations++;
        }
        
        return operations;
    }
    
private:
    bool isNonDecreasing(const vector<int>& a) {
        for (int i = 1; i < a.size(); i++) {
            if (a[i] < a[i - 1]) {
                return false;
            }
        }
        return true;
    }
};