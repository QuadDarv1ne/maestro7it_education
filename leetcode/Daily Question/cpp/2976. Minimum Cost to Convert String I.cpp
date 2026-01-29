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

class Solution {
public:
    long long minimumCost(string source, string target, vector<char>& original, vector<char>& changed, vector<int>& cost) {
        const long long INF = 1e18;
        // Матрица 26x26 для минимальных стоимостей преобразований
        vector<vector<long long>> dist(26, vector<long long>(26, INF));
        
        // Инициализация: преобразование символа в себя стоит 0
        for (int i = 0; i < 26; i++) {
            dist[i][i] = 0;
        }
        
        // Добавляем заданные преобразования
        for (int i = 0; i < original.size(); i++) {
            int u = original[i] - 'a';
            int v = changed[i] - 'a';
            dist[u][v] = min(dist[u][v], (long long)cost[i]);
        }
        
        // Алгоритм Флойда-Уоршелла
        for (int k = 0; k < 26; k++) {
            for (int i = 0; i < 26; i++) {
                if (dist[i][k] == INF) continue;
                for (int j = 0; j < 26; j++) {
                    if (dist[k][j] == INF) continue;
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
                }
            }
        }
        
        // Вычисляем общую стоимость
        long long total = 0;
        for (int i = 0; i < source.length(); i++) {
            int u = source[i] - 'a';
            int v = target[i] - 'a';
            
            if (dist[u][v] == INF) {
                return -1;
            }
            total += dist[u][v];
        }
        
        return total;
    }
};