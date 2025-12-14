/*
https://leetcode.com/problems/count-mentions-per-user/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

var countMentions = function(numberOfUsers, events) {
    events.sort((a,b) => {
        let ta = parseInt(a[1]), tb = parseInt(b[1]);
        if (ta === tb) {
            if (a[0] === "OFFLINE" && b[0] === "MESSAGE") return -1;
            if (a[0] === "MESSAGE" && b[0] === "OFFLINE") return 1;
        }
        return ta - tb;
    });

    const mentions = new Array(numberOfUsers).fill(0);
    const offlineUntil = new Array(numberOfUsers).fill(0);
    const online = new Set();
    for (let i = 0; i < numberOfUsers; i++) online.add(i);

    for (let ev of events) {
        const t = parseInt(ev[1]);

        // Обновляем статус онлайн
        for (let i = 0; i < numberOfUsers; i++) {
            if (offlineUntil[i] <= t) online.add(i);
        }

        if (ev[0] === "OFFLINE") {
            const uid = parseInt(ev[2]);
            offlineUntil[uid] = t + 60;
            online.delete(uid);
        } else { // MESSAGE
            const data = ev[2];
            if (data === "ALL") {
                for (let i = 0; i < numberOfUsers; i++) mentions[i]++;
            } else if (data === "HERE") {
                for (let uid of online) mentions[uid]++;
            } else {
                for (let token of data.split(" ")) {
                    if (token.startsWith("id")) {
                        const uid = parseInt(token.slice(2));
                        mentions[uid]++;
                    }
                }
            }
        }
    }

    return mentions;
};
