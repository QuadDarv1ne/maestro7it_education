/**
 * Находит максимальную длину подмножества, в котором существуют три элемента
 * x, y, z (не обязательно различных по индексам, но могут быть равны по значению),
 * таких что x * y == z.
 * 
 * @param {number[]} nums - массив целых чисел
 * @return {number} максимальная длина подмножества
 */
var maximumLength = function(nums) {
    const freq = new Map();
    for (const num of nums) {
        freq.set(num, (freq.get(num) || 0) + 1);
    }
    
    let maxLen = 0;
    const LIMIT = 1e9;
    
    // Обрабатываем единицы
    if (freq.has(1)) {
        const countOnes = freq.get(1);
        maxLen = Math.max(maxLen, countOnes % 2 === 1 ? countOnes : countOnes - 1);
    }
    
    const visited = new Set();
    
    for (const [num, count] of freq) {
        if (num === 1 || visited.has(num)) continue;
        
        let chainLen = 0;
        let current = num;
        
        while (freq.has(current) && current <= LIMIT) {
            visited.add(current);
            
            if (freq.get(current) >= 2) {
                chainLen += 2;
            } else {
                chainLen += 1;
                break;
            }
            
            current = current * current;
        }
        
        maxLen = Math.max(maxLen, chainLen);
    }
    
    return maxLen;
};