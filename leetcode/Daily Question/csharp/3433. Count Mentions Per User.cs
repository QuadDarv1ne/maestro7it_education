/*
https://leetcode.com/problems/count-mentions-per-user/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

public class Solution {
    public int[] CountMentions(int numberOfUsers, string[][] events) {
        Array.Sort(events, (a,b) => {
            int ta = int.Parse(a[1]), tb = int.Parse(b[1]);
            if (ta == tb) {
                // OFFLINE перед MESSAGE
                if (a[0] == "OFFLINE" && b[0] == "MESSAGE") return -1;
                if (a[0] == "MESSAGE" && b[0] == "OFFLINE") return 1;
            }
            return ta.CompareTo(tb);
        });

        int[] mentions = new int[numberOfUsers];
        int[] offlineUntil = new int[numberOfUsers];

        foreach (var ev in events) {
            int t = int.Parse(ev[1]);
            for (int i = 0; i < numberOfUsers; i++)
                if (offlineUntil[i] <= t) offlineUntil[i] = 0;

            if (ev[0] == "OFFLINE") {
                int uid = int.Parse(ev[2]);
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
                    foreach (var token in data.Split(' ')) {
                        if (token.StartsWith("id")) {
                            int uid = int.Parse(token.Substring(2));
                            mentions[uid]++;
                        }
                    }
                }
            }
        }
        return mentions;
    }
}
