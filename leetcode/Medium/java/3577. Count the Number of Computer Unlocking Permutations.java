/*
LeetCode 3577: Count the Number of Computer Unlocking Permutations
https://leetcode.com/problems/count-the-number-of-computer-unlocking-permutations/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. YouTube канал: https://www.youtube.com/@it-coders
6. ВК группа: https://vk.com/science_geeks
*/

// ========================== JAVA ==========================
class Solution {
    /**
     * Подсчитывает количество валидных перестановок для разблокировки компьютеров.
     * 
     * Time Complexity: O(n)
     * Space Complexity: O(1)
     * 
     * @param complexity массив сложностей паролей компьютеров
     * @return количество валидных перестановок по модулю 10^9 + 7
     */
    public int countPermutations(int[] complexity) {
        final int MOD = 1_000_000_007;
        int n = complexity.length;
        
        // Проверяем, можно ли разблокировать все компьютеры
        for (int i = 1; i < n; i++) {
            if (complexity[i] <= complexity[0]) {
                return 0;
            }
        }
        
        // Вычисляем (n-1)! mod MOD
        long result = 1;
        for (int i = 1; i < n; i++) {
            result = (result * i) % MOD;
        }
        
        return (int) result;
    }
}