/*
https://leetcode.com/problems/count-mentions-per-user/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

import java.util.*;

class Solution {
    public int[] countMentions(int numberOfUsers, String[][] events) {
        Arrays.sort(events, (a, b) -> {
            int ta = Integer.parseInt(a[1]), tb = Integer.parseInt(b[1]);
            if (ta == tb) {
                if (a[0].equals("OFFLINE") && b[0].equals("MESSAGE")) return -1;
                if (a[0].equals("MESSAGE") && b[0].equals("OFFLINE")) return 1;
            }
            return ta - tb;
        });

        int[] mentions = new int[numberOfUsers];
        int[] offlineUntil = new int[numberOfUsers];
        Set<Integer> online = new HashSet<>();
        for (int i = 0; i < numberOfUsers; i++) online.add(i);

        for (String[] ev : events) {
            int t = Integer.parseInt(ev[1]);

            // Обновляем статус онлайн
            for (int uid = 0; uid < numberOfUsers; uid++) {
                if (offlineUntil[uid] <= t) online.add(uid);
            }

            if (ev[0].equals("OFFLINE")) {
                int uid = Integer.parseInt(ev[2]);
                offlineUntil[uid] = t + 60;
                online.remove(uid);
            } else { // MESSAGE
                String data = ev[2];
                if (data.equals("ALL")) {
                    for (int i = 0; i < numberOfUsers; i++) mentions[i]++;
                } else if (data.equals("HERE")) {
                    for (int uid : online) mentions[uid]++;
                } else {
                    for (String token : data.split(" ")) {
                        if (token.startsWith("id")) {
                            int uid = Integer.parseInt(token.substring(2));
                            mentions[uid]++;
                        }
                    }
                }
            }
        }

        return mentions;
    }
}
