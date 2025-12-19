/*
https://leetcode.com/problems/count-covered-buildings/?envType=daily-question&envId=2025-12-11

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Count Covered Buildings"
*/

var countCoveredBuildings = function(n, buildings) {
    let rowMin = new Map(), rowMax = new Map();
    let colMin = new Map(), colMax = new Map();

    for (let [x, y] of buildings) {
        rowMin.set(x, rowMin.has(x) ? Math.min(rowMin.get(x), y) : y);
        rowMax.set(x, rowMax.has(x) ? Math.max(rowMax.get(x), y) : y);
        colMin.set(y, colMin.has(y) ? Math.min(colMin.get(y), x) : x);
        colMax.set(y, colMax.has(y) ? Math.max(colMax.get(y), x) : x);
    }

    let ans = 0;
    for (let [x, y] of buildings) {
        if (rowMin.get(x) < y && y < rowMax.get(x) &&
            colMin.get(y) < x && x < colMax.get(y)) {
            ans++;
        }
    }
    return ans;
};
