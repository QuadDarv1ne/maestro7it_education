/*
https://leetcode.com/problems/restore-ip-addresses/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

var restoreIpAddresses = function(s) {
    /*
    Решение задачи "Restore IP Addresses" (LeetCode 93).

    Идея:
    - Backtracking: строим 4 сегмента.
    - Каждый сегмент длиной 1–3, не начинается с ведущих нулей
      (если длина > 1).
    - Значение сегмента должно быть ≤ 255.
    */
    const res = [];
    const parts = [];

    const backtrack = (start) => {
        if (parts.length === 4) {
            if (start === s.length)
                res.push(parts.join('.'));
            return;
        }
        if (start >= s.length) return;

        for (let len = 1; len <= 3 && start + len <= s.length; len++) {
            const seg = s.substring(start, start + len);
            if (seg.length > 1 && seg[0] === '0') continue;
            if (parseInt(seg) <= 255) {
                parts.push(seg);
                backtrack(start + len);
                parts.pop();
            }
        }
    };

    backtrack(0);
    return res;
};
