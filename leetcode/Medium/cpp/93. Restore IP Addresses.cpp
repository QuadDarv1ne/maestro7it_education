/*
https://leetcode.com/problems/restore-ip-addresses/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
public:
    vector<string> restoreIpAddresses(string s) {
        /*
        Решение задачи "Restore IP Addresses" (LeetCode 93).

        Идея:
        - Строим IP‑адрес через backtracking на 4 части.
        - Каждой части длина 1–3, без ведущих нулей,
          значение ≤ 255.
        */
        vector<string> res;
        vector<string> parts;

        function<void(int)> backtrack = [&](int start) {
            if (parts.size() == 4) {
                if (start == s.size()) {
                    string ip = parts[0];
                    for (int i = 1; i < 4; i++)
                        ip += "." + parts[i];
                    res.push_back(ip);
                }
                return;
            }
            if (start >= s.size())
                return;

            for (int len = 1; len <= 3 && start + len <= s.size(); len++) {
                string seg = s.substr(start, len);
                if (seg.size() > 1 && seg[0] == '0') continue;
                if (stoi(seg) <= 255) {
                    parts.push_back(seg);
                    backtrack(start + len);
                    parts.pop_back();
                }
            }
        };

        backtrack(0);
        return res;
    }
};
