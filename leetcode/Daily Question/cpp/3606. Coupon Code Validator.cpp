/*
https://leetcode.com/problems/coupon-code-validator/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
public:
    vector<string> validateCoupons(vector<string>& code, vector<string>& businessLine, vector<bool>& isActive) {
        vector<string> order = {"electronics", "grocery", "pharmacy", "restaurant"};
        unordered_map<string,int> pos;
        for (int i = 0; i < order.size(); i++)
            pos[order[i]] = i;

        vector<pair<int,string>> valid;
        regex pattern("^[A-Za-z0-9_]+$");

        for (int i = 0; i < code.size(); i++) {
            if (isActive[i] && pos.count(businessLine[i]) && !code[i].empty() &&
                regex_match(code[i], pattern)) {
                valid.push_back({pos[businessLine[i]], code[i]});
            }
        }

        sort(valid.begin(), valid.end(), [](auto &a, auto &b) {
            if (a.first == b.first)
                return a.second < b.second;
            return a.first < b.first;
        });

        vector<string> answer;
        for (auto &p : valid) answer.push_back(p.second);
        return answer;
    }
};
