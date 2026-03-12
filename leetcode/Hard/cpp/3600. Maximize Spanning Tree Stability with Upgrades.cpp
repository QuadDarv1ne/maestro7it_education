/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

#include <vector>
#include <tuple>
#include <algorithm>
#include <functional>
#include <set>
using namespace std;

class Solution {
public:
    int maxStability(int n, vector<vector<int>>& edges, int k) {
        vector<tuple<int, int, int, int>> e;
        for (auto& edge : edges) {
            e.emplace_back(edge[0], edge[1], edge[2], edge[3]);
        }
        
        // Собираем все возможные значения стабильности
        vector<int> strengths;
        for (auto& edge : e) {
            strengths.push_back(get<2>(edge));
            if (get<3>(edge) == 0) {
                strengths.push_back(get<2>(edge) * 2); // Улучшенная прочность
            }
        }
        sort(strengths.begin(), strengths.end());
        strengths.erase(unique(strengths.begin(), strengths.end()), strengths.end());
        
        int left = 0, right = strengths.size() - 1;
        int ans = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            int target = strengths[mid];
            
            if (canAchieve(n, e, k, target)) {
                ans = target;
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return ans;
    }
    
private:
    struct DSU {
        vector<int> parent, rank;
        
        DSU(int n) {
            parent.resize(n);
            rank.resize(n, 0);
            for (int i = 0; i < n; i++) parent[i] = i;
        }
        
        void reset(int n) {
            for (int i = 0; i < n; i++) {
                parent[i] = i;
                rank[i] = 0;
            }
        }
        
        int find(int x) {
            if (parent[x] != x) parent[x] = find(parent[x]);
            return parent[x];
        }
        
        bool unite(int x, int y) {
            x = find(x);
            y = find(y);
            if (x == y) return false;
            if (rank[x] < rank[y]) parent[x] = y;
            else if (rank[x] > rank[y]) parent[y] = x;
            else {
                parent[y] = x;
                rank[x]++;
            }
            return true;
        }
        
        bool isConnected(int n) {
            int root = find(0);
            for (int i = 1; i < n; i++) {
                if (find(i) != root) return false;
            }
            return true;
        }
    };
    
    bool canAchieve(int n, vector<tuple<int, int, int, int>>& edges, int k, int target) {
        DSU dsu(n);
        vector<tuple<int, int, int>> optional; // u, v, s
        int mandatoryUsed = 0;
        int mandatoryCount = 0;
        
        for (auto& edge : edges) {
            int u = get<0>(edge), v = get<1>(edge), s = get<2>(edge), must = get<3>(edge);
            if (must == 1) {
                mandatoryCount++;
                if (s < target) return false;
                if (dsu.unite(u, v)) {
                    mandatoryUsed++;
                }
            } else {
                optional.emplace_back(u, v, s);
            }
        }
        
        // Проверяем, не создали ли обязательные рёбра циклы
        if (mandatoryUsed < mandatoryCount) return false;
        
        // Сортируем опциональные рёбра: сначала те, что не требуют улучшения
        sort(optional.begin(), optional.end(), [target](auto& a, auto& b) {
            int sa = get<2>(a);
            int sb = get<2>(b);
            bool aGood = sa >= target;
            bool bGood = sb >= target;
            
            if (aGood && !bGood) return true;
            if (!aGood && bGood) return false;
            
            // Если оба в одной категории, сортируем по убыванию прочности
            if (aGood) {
                return sa > sb;
            } else {
                // Для требующих улучшения - по убыванию улучшенной прочности
                int valA = sa * 2;
                int valB = sb * 2;
                if (valA != valB) return valA > valB;
                return sa > sb;
            }
        });
        
        int upgradesUsed = 0;
        int totalUsed = mandatoryUsed;
        
        for (auto& edge : optional) {
            if (totalUsed == n - 1) break;
            
            int u = get<0>(edge), v = get<1>(edge), s = get<2>(edge);
            
            if (s >= target) {
                if (dsu.unite(u, v)) {
                    totalUsed++;
                }
            } else if (upgradesUsed < k && s * 2 >= target) {
                if (dsu.unite(u, v)) {
                    upgradesUsed++;
                    totalUsed++;
                }
            }
        }
        
        return totalUsed == n - 1 && dsu.isConnected(n);
    }
};