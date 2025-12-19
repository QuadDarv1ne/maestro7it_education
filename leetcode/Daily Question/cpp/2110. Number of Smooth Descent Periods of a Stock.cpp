/*
https://leetcode.com/problems/number-of-smooth-descent-periods-of-a-stock/description/?envType=daily-question&envId=2025-12-15

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Задача:
Подсчитать количество "smooth descent periods" — отрезков,
где каждый следующий элемент ровно на 1 меньше предыдущего.
Одиночный элемент всегда считается валидным периодом.

Идея:
dp — длина текущего гладкого убывания, заканчивающегося в текущем дне.
Если prices[i-1] - prices[i] == 1 → dp++
Иначе dp = 1
Каждый dp добавляется к ответу.

Сложность:
Время: O(n)
Память: O(1)
*/

class Solution {
public:
    long long getDescentPeriods(vector<int>& prices) {
        long long ans = 0;
        long long dp = 1;  // длина текущего smooth descent

        ans += dp;
        for (int i = 1; i < prices.size(); i++) {
            if (prices[i - 1] - prices[i] == 1) {
                dp++;
            } else {
                dp = 1;
            }
            ans += dp;
        }
        return ans;
    }
};
