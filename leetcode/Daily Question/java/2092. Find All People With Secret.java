/*
https://leetcode.com/problems/find-all-people-with-secret/?envType=daily-question&envId=2025-12-19

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Find All People With Secret"

Условие:
- Есть n человек (0 ... n-1)
- meetings[i] = [x, y, time]
- Человек 0 знает секрет и сообщает его firstPerson в момент 0
- Секрет распространяется мгновенно в рамках одного и того же времени

Идея решения:
1. Отсортировать встречи по времени
2. Обрабатывать встречи группами с одинаковым временем
3. Для каждой группы строить временный граф
4. Если хотя бы один участник компоненты знает секрет — он распространяется
5. Обновлять глобальный массив knows

Сложность:
- Время: O(m log m)
- Память: O(n + m)
*/

import java.util.*;

class Solution {
    public List<Integer> findAllPeople(int n, int[][] meetings, int firstPerson) {

        // Сортируем встречи по времени
        Arrays.sort(meetings, (a, b) -> Integer.compare(a[2], b[2]));

        // knows[i] = знает ли человек i секрет
        boolean[] knows = new boolean[n];
        knows[0] = true;
        knows[firstPerson] = true;

        int i = 0;
        int m = meetings.length;

        while (i < m) {
            int currentTime = meetings[i][2];

            // Временный граф для текущего времени
            Map<Integer, List<Integer>> graph = new HashMap<>();
            Set<Integer> participants = new HashSet<>();

            // Собираем все встречи с одинаковым временем
            while (i < m && meetings[i][2] == currentTime) {
                int x = meetings[i][0];
                int y = meetings[i][1];

                graph.computeIfAbsent(x, k -> new ArrayList<>()).add(y);
                graph.computeIfAbsent(y, k -> new ArrayList<>()).add(x);

                participants.add(x);
                participants.add(y);
                i++;
            }

            // BFS начинается только от тех, кто уже знает секрет
            Queue<Integer> queue = new ArrayDeque<>();
            Set<Integer> visited = new HashSet<>();

            for (int p : participants) {
                if (knows[p]) {
                    queue.offer(p);
                    visited.add(p);
                }
            }

            // Распространяем секрет внутри текущей временной группы
            while (!queue.isEmpty()) {
                int cur = queue.poll();
                if (!graph.containsKey(cur)) continue;

                for (int next : graph.get(cur)) {
                    if (!visited.contains(next)) {
                        visited.add(next);
                        queue.offer(next);
                    }
                }
            }

            // Все достигнутые участники теперь знают секрет
            for (int p : visited) {
                knows[p] = true;
            }
        }

        // Формируем ответ
        List<Integer> result = new ArrayList<>();
        for (int p = 0; p < n; p++) {
            if (knows[p]) {
                result.add(p);
            }
        }

        return result;
    }
}
