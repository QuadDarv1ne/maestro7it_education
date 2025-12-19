/*
https://leetcode.com/problems/find-all-people-with-secret/?envType=daily-question&envId=2025-12-19

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

var findAllPeople = function(n, meetings, firstPerson) {
    meetings.sort((a, b) => a[2] - b[2]);

    const knows = Array(n).fill(false);
    knows[0] = true;
    knows[firstPerson] = true;

    let i = 0;
    while (i < meetings.length) {
        const t = meetings[i][2];
        const adj = new Map();
        const participants = new Set();

        while (i < meetings.length && meetings[i][2] === t) {
            const [x, y] = meetings[i];
            if (!adj.has(x)) adj.set(x, []);
            if (!adj.has(y)) adj.set(y, []);
            adj.get(x).push(y);
            adj.get(y).push(x);
            participants.add(x);
            participants.add(y);
            i++;
        }

        const queue = [];
        const visited = new Set();
        for (const p of participants) {
            if (knows[p]) {
                queue.push(p);
                visited.add(p);
            }
        }

        while (queue.length) {
            const cur = queue.shift();
            if (!adj.has(cur)) continue;
            for (const nxt of adj.get(cur)) {
                if (!visited.has(nxt)) {
                    visited.add(nxt);
                    queue.push(nxt);
                }
            }
        }

        for (const p of visited) {
            knows[p] = true;
        }
    }

    return knows.map((v, idx) => v ? idx : -1).filter(x => x !== -1);
};
