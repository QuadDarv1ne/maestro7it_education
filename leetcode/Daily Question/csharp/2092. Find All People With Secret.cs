/*
https://leetcode.com/problems/find-all-people-with-secret/?envType=daily-question&envId=2025-12-19

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

public class Solution {
    public IList<int> FindAllPeople(int n, int[][] meetings, int firstPerson) {
        Array.Sort(meetings, (a, b) => a[2].CompareTo(b[2]));

        bool[] knows = new bool[n];
        knows[0] = true;
        knows[firstPerson] = true;

        int i = 0, m = meetings.Length;
        while (i < m) {
            int currentTime = meetings[i][2];
            var adj = new Dictionary<int, List<int>>();
            var participants = new HashSet<int>();

            while (i < m && meetings[i][2] == currentTime) {
                int x = meetings[i][0], y = meetings[i][1];
                if (!adj.ContainsKey(x)) adj[x] = new List<int>();
                if (!adj.ContainsKey(y)) adj[y] = new List<int>();
                adj[x].Add(y);
                adj[y].Add(x);
                participants.Add(x);
                participants.Add(y);
                i++;
            }

            var queue = new Queue<int>();
            var visited = new HashSet<int>();
            foreach (int p in participants) {
                if (knows[p]) {
                    queue.Enqueue(p);
                    visited.Add(p);
                }
            }

            while (queue.Count > 0) {
                int cur = queue.Dequeue();
                if (!adj.ContainsKey(cur)) continue;
                foreach (int nxt in adj[cur]) {
                    if (!visited.Contains(nxt)) {
                        visited.Add(nxt);
                        queue.Enqueue(nxt);
                    }
                }
            }

            foreach (int p in visited) knows[p] = true;
        }

        var result = new List<int>();
        for (int x = 0; x < n; x++)
            if (knows[x]) result.Add(x);

        return result;
    }
}
