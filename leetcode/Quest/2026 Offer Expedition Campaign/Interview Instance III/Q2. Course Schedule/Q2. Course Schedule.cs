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

public class Solution {
    public bool CanFinish(int numCourses, int[][] prerequisites) {
        List<int>[] graph = new List<int>[numCourses];
        for (int i = 0; i < numCourses; i++) {
            graph[i] = new List<int>();
        }
        foreach (int[] pre in prerequisites) {
            graph[pre[1]].Add(pre[0]); // prereq -> course
        }
        
        int[] state = new int[numCourses]; // 0 unvisited, 1 visiting, 2 visited
        
        for (int i = 0; i < numCourses; i++) {
            if (HasCycle(i, graph, state)) {
                return false;
            }
        }
        return true;
    }
    
    private bool HasCycle(int node, List<int>[] graph, int[] state) {
        if (state[node] == 1) return true;
        if (state[node] == 2) return false;
        
        state[node] = 1;
        foreach (int neighbor in graph[node]) {
            if (HasCycle(neighbor, graph, state)) {
                return true;
            }
        }
        state[node] = 2;
        return false;
    }
}