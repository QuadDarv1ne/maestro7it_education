public class Solution {
    public int SingleNumber(int[] nums) {
        /**
         * Находит единственный элемент, который встречается один раз.
         * 
         * Алгоритм:
         * 1. Используем операцию XOR для всех элементов
         * 2. Все парные элементы аннулируют друг друга
         * 3. Оставшийся результат - искомый элемент
         * 
         * Сложность: O(n) время, O(1) память
         */
        
        int result = 0;
        foreach (int num in nums) {
            result ^= num;
        }
        return result;
    }
}