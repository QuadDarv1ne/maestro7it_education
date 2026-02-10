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
    /**
     * Находит длину самого длинного сбалансированного подмассива.
     * Подмассив сбалансирован, если количество уникальных четных чисел
     * равно количеству уникальных нечетных чисел.
     *
     * @param nums Входной массив целых чисел
     * @return Длина самого длинного сбалансированного подмассива
     * @example
     *   longestBalanced(new int[]{2,5,4,3}) → 4
     *   longestBalanced(new int[]{3,2,2,5,4}) → 5
     *   longestBalanced(new int[]{1,2,3,2}) → 3
     */
    public int longestBalanced(int[] nums) {
        int n = nums.length;
        int max_len = 0;
        
        for (int i = 0; i < n; i++) {
            Set<Integer> evenSet = new HashSet<>();
            Set<Integer> oddSet = new HashSet<>();
            
            for (int j = i; j < n; j++) {
                if (nums[j] % 2 == 0) {
                    evenSet.add(nums[j]);
                } else {
                    oddSet.add(nums[j]);
                }
                
                if (evenSet.size() == oddSet.size()) {
                    max_len = Math.max(max_len, j - i + 1);
                }
            }
        }
        
        return max_len;
    }
}