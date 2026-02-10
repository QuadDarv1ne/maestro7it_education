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
     * Находит пропущенное число в диапазоне [0, n] в массиве длины n.
     * 
     * @param nums Вектор длиной n, содержащий n различных чисел из [0, n]
     * @return Единственное пропущенное число
     * 
     * @example missingNumber({3,0,1}) → 2
     * @example missingNumber({0,1}) → 2
     * @example missingNumber({9,6,4,2,3,5,7,0,1}) → 8
     * 
     * Сложность:
     *   Время: O(n)
     *   Память: O(1)
     */
    int missingNumber(vector<int>& nums) {
        int n = nums.size();
        // Способ 1: Формула суммы
        int expectedSum = n * (n + 1) / 2;
        int actualSum = 0;
        for (int num : nums) {
            actualSum += num;
        }
        return expectedSum - actualSum;
        
        // Способ 2: XOR
        // int result = nums.size();
        // for (int i = 0; i < nums.size(); i++) {
        //     result ^= i ^ nums[i];
        // }
        // return result;
    }
};