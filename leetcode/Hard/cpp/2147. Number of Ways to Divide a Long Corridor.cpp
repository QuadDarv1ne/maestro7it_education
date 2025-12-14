/*
https://leetcode.com/problems/number-of-ways-to-divide-a-long-corridor/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
public:
    int numberOfWays(string corridor) {
        const long long MOD = 1e9 + 7;
        vector<int> seats;

        for (int i = 0; i < corridor.size(); i++) {
            if (corridor[i] == 'S')
                seats.push_back(i);
        }

        if (seats.size() < 2 || seats.size() % 2 != 0)
            return 0;

        long long ways = 1;
        for (int i = 1; i < seats.size() - 1; i += 2) {
            long long gap = seats[i + 1] - seats[i];
            ways = (ways * gap) % MOD;
        }

        return ways;
    }
};
