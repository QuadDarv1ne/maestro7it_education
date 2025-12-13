/*
https://leetcode.com/problems/gray-code/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

/**
 * @param {number} n
 * @return {number[]}
 */
var grayCode = function(n) {
    /*
    Решение задачи "Gray Code" (LeetCode 89).

    Идея:
    - Используем отражение:
      начальный массив [0], затем на каждом шаге
      добавляем отражённые элементы с установленным битом.
    - Последовательность длиной 2^n, первые — 0.

    Сложность:
    - Время: O(2^n)
    - Память: O(2^n)
    */
    const result = [0];
    for (let i = 0; i < n; i++) {
        let size = result.length;
        for (let j = size - 1; j >= 0; j--) {
            result.push(result[j] | (1 << i));
        }
    }
    return result;
};
