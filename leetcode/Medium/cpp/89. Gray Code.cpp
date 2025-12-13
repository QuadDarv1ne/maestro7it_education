/*
https://leetcode.com/problems/gray-code/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
public:
    vector<int> grayCode(int n) {
        /*
        Решение задачи "Gray Code" (LeetCode 89).

        Идея:
        - Строим последовательность методом зеркального отражения:
          для каждого бита отражаем текущий список и добавляем бит.
        - Последовательность всегда начинается с 0.

        Сложность:
        - Время: O(2^n)
        - Память: O(2^n)
        */
        vector<int> result{0};
        for (int i = 0; i < n; ++i) {
            int size = result.size();
            for (int j = size - 1; j >= 0; --j) {
                result.push_back(result[j] | (1 << i));
            }
        }
        return result;
    }
};
