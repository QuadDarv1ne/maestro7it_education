/*
https://leetcode.com/problems/count-mentions-per-user/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
public:
    vector<int> countMentions(int numberOfUsers, vector<vector<string>>& events) {
        vector<int> mentions(numberOfUsers, 0);
        vector<int> offlineUntil(numberOfUsers, 0);

        // Сортировка: OFFLINE перед MESSAGE при одинаковом времени
        sort(events.begin(), events.end(), [](auto &a, auto &b) {
            int ta = stoi(a[1]), tb = stoi(b[1]);
            if (ta == tb) return a[0] == "OFFLINE" && b[0] == "MESSAGE";
            return ta < tb;
        });

        for (auto &ev : events) {
            int t = stoi(ev[1]);
            // Обновляем онлайн/оффлайн
            for (int i = 0; i < numberOfUsers; i++) {
                if (offlineUntil[i] <= t) offlineUntil[i] = 0;
            }
            if (ev[0] == "OFFLINE") {
                int uid = stoi(ev[2]);
                offlineUntil[uid] = t + 60;
            } else {
                string data = ev[2];
                if (data == "ALL") {
                    for (int i = 0; i < numberOfUsers; i++)
                        mentions[i]++;
                } else if (data == "HERE") {
                    for (int i = 0; i < numberOfUsers; i++)
                        if (offlineUntil[i] == 0)
                            mentions[i]++;
                } else {
                    // Разбор id-списка
                    stringstream ss(data);
                    string token;
                    while (ss >> token) {
                        if (token.rfind("id", 0) == 0) {
                            int uid = stoi(token.substr(2));
                            mentions[uid]++;
                        }
                    }
                }
            }
        }
        return mentions;
    }
};
