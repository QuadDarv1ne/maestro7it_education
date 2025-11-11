/*
https://leetcode.com/problems/power-grid-maintenance/description/?envType=daily-question&envId=2025-11-06
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X  
GitHub: https://github.com/QuadDarv1ne/  
*/

class Solution {
private:
    vector<int> parent;
    vector<int> rank;
    
    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]); // Path compression
        }
        return parent[x];
    }
    
    bool unionSet(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return false;
        
        // Union by rank
        if (rank[px] < rank[py]) {
            parent[px] = py;
        } else if (rank[px] > rank[py]) {
            parent[py] = px;
        } else {
            parent[py] = px;
            rank[px]++;
        }
        return true;
    }
    
    bool isConnected(int x, int y) {
        return find(x) == find(y);
    }
    
public:
    vector<int> processQueries(int c, vector<vector<int>>& connections, vector<vector<int>>& queries) {
        int n = c; // количество городов/узлов
        vector<int> result;
        
        // Инициализация Union-Find
        parent.resize(n);
        rank.resize(n, 0);
        for (int i = 0; i < n; i++) {
            parent[i] = i;
        }
        
        // Создаём граф из активных соединений
        set<pair<int, int>> activeConnections;
        for (const auto& conn : connections) {
            int u = conn[0], v = conn[1];
            if (u > v) swap(u, v); // нормализуем порядок
            activeConnections.insert({u, v});
            unionSet(u, v);
        }
        
        // Обрабатываем запросы
        for (const auto& query : queries) {
            int type = query[0];
            
            if (type == 1) {
                // Запрос типа 1: отключить соединение [1, u, v]
                int u = query[1], v = query[2];
                if (u > v) swap(u, v);
                activeConnections.erase({u, v});
                
                // Перестраиваем Union-Find без этого соединения
                parent.assign(n, 0);
                rank.assign(n, 0);
                for (int i = 0; i < n; i++) {
                    parent[i] = i;
                }
                
                for (const auto& [a, b] : activeConnections) {
                    unionSet(a, b);
                }
                
            } else if (type == 2) {
                // Запрос типа 2: включить соединение [2, u, v]
                int u = query[1], v = query[2];
                if (u > v) swap(u, v);
                activeConnections.insert({u, v});
                unionSet(u, v);
                
            } else if (type == 3) {
                // Запрос типа 3: проверить связность [3, u, v]
                int u = query[1], v = query[2];
                result.push_back(isConnected(u, v) ? 1 : 0);
            }
        }
        
        return result;
    }
};

/* 
Объяснение типов запросов:
- Тип 1 [1, u, v]: отключить соединение между городами u и v
- Тип 2 [2, u, v]: включить соединение между городами u и v
- Тип 3 [3, u, v]: проверить, связаны ли города u и v (вернуть 1 или 0)

Алгоритм:
1. Используем Union-Find для отслеживания компонент связности
2. Храним активные соединения в set для быстрого добавления/удаления
3. При отключении соединения перестраиваем Union-Find
4. При включении просто добавляем соединение
5. При проверке связности используем find()

Сложность:
- Время: O(Q * (E + N)) где Q - запросы, E - рёбра, N - узлы
- Память: O(N + E)
*/

/* Полезные ссылки: */
// 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
// 2. Telegram №1 @quadd4rv1n7
// 3. Telegram №2 @dupley_maxim_1999
// 4. Rutube канал: https://rutube.ru/channel/4218729/
// 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
// 6. YouTube канал: https://www.youtube.com/@it-coders
// 7. ВК группа: https://vk.com/science_geeks