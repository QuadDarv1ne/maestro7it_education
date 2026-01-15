/**
 * Максимальная площадь квадратного отверстия в сетке
 * @param {number} n
 * @param {number} m
 * @param {number[]} hBars
 * @param {number[]} vBars
 * @return {number}
 */
var maximizeSquareHoleArea = function(n, m, hBars, vBars) {
    hBars.sort((a, b) => a - b);
    vBars.sort((a, b) => a - b);
    
    const findMaxConsecutive = (arr) => {
        if (arr.length === 0) return 0;
        let maxGap = 1;
        let current = 1;
        for (let i = 1; i < arr.length; i++) {
            if (arr[i] === arr[i-1] + 1) {
                current++;
            } else {
                maxGap = Math.max(maxGap, current);
                current = 1;
            }
        }
        return Math.max(maxGap, current);
    };
    
    const maxH = findMaxConsecutive(hBars);
    const maxV = findMaxConsecutive(vBars);
    
    const side = Math.min(maxH, maxV) + 1;
    return side * side;
};