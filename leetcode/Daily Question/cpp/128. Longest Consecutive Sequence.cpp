class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        /**
         * Находит длину самой длинной последовательности последовательных чисел.
         * 
         * Алгоритм:
         * 1. Преобразуем массив в множество для быстрого поиска
         * 2. Для каждого числа проверяем, является ли оно началом последовательности
         * 3. Если да, то подсчитываем длину последовательности
         * 
         * Сложность: O(n) время, O(n) память
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
        
        if (nums.empty()) {
            return 0;
        }
        
        // Преобразуем вектор в множество
        unordered_set<int> numSet(nums.begin(), nums.end());
        int maxLength = 0;
        
        for (int num : numSet) {
            // Проверяем, является ли число началом последовательности
            if (numSet.find(num - 1) == numSet.end()) {
                int currentNum = num;
                int currentLength = 1;
                
                // Подсчитываем длину последовательности
                while (numSet.find(currentNum + 1) != numSet.end()) {
                    currentNum++;
                    currentLength++;
                }
                
                // Обновляем максимальную длину
                maxLength = max(maxLength, currentLength);
            }
        }
        
        return maxLength;
    }
};