/*
https://leetcode.com/problems/gray-code/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

public class Solution {
    public IList<int> GrayCode(int n) {
        /*
        Решение задачи "Gray Code" (LeetCode 89).

        Идея:
        - Начинаем с [0], затем на каждом шаге
          добавляем отражённые элементы с установленным битом.
        - Последовательность длиной 2^n начинается с 0.

        Сложность:
        - Время: O(2^n)
        - Память: O(2^n)
        */
        var result = new List<int> { 0 };
        for (int i = 0; i < n; ++i) {
            int size = result.Count;
            for (int j = size - 1; j >= 0; --j) {
                result.Add(result[j] | (1 << i));
            }
        }
        return result;
    }
}
