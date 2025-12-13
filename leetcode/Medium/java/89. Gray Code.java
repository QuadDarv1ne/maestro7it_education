/*
https://leetcode.com/problems/gray-code/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
    public List<Integer> grayCode(int n) {
        /*
        Решение задачи "Gray Code" (LeetCode 89).

        Идея:
        - Построение методом зеркального отражения:
          начинаем с [0], затем на каждом уровне
          дополняем последовательность отражёнными значениями
          с установленным битом.
        - Возвращаем любую валидную последовательность.

        Сложность:
        - Время: O(2^n)
        - Память: O(2^n)
        */
        List<Integer> result = new ArrayList<>();
        result.add(0);
        for (int i = 0; i < n; i++) {
            int size = result.size();
            for (int j = size - 1; j >= 0; j--) {
                result.add(result.get(j) | (1 << i));
            }
        }
        return result;
    }
}
