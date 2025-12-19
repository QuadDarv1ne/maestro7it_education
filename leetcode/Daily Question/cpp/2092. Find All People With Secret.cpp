/*
https://leetcode.com/problems/find-all-people-with-secret/?envType=daily-question&envId=2025-12-19

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
public:
    vector<int> findAllPeople(int n, vector<vector<int>>& meetings, int firstPerson) {
        sort(meetings.begin(), meetings.end(), [](auto &a, auto &b) {
            return a[2] < b[2];
        });
        
        vector<bool> knows(n, false);
        knows[0] = true;
        knows[firstPerson] = true;
        
        int i = 0, m = meetings.size();
        while (i < m) {
            int t = meetings[i][2];
            unordered_map<int, vector<int>> adj;
            unordered_set<int> participants;
            
            // Собираем встречи с одинаковым временем
            int j = i;
            while (j < m && meetings[j][2] == t) {
                int x = meetings[j][0], y = meetings[j][1];
                adj[x].push_back(y);
                adj[y].push_back(x);
                participants.insert(x);
                participants.insert(y);
                ++j;
            }
            
            // Находим из участников тех, кто уже знает секрет
            queue<int> q;
            unordered_set<int> visited;
            for (int p : participants) {
                if (knows[p]) {
                    q.push(p);
                    visited.insert(p);
                }
            }
            
            // BFS для распространения среди этой группы
            while (!q.empty()) {
                int cur = q.front(); q.pop();
                for (int nxt : adj[cur]) {
                    if (!visited.count(nxt)) {
                        visited.insert(nxt);
                        q.push(nxt);
                    }
                }
            }
            
            // Добавляем всех найденных к тем, кто знает секрет
            for (int p : visited) {
                knows[p] = true;
            }
            i = j;
        }
        
        vector<int> result;
        for (int x = 0; x < n; x++) if (knows[x]) result.push_back(x);
        return result;
    }
};
