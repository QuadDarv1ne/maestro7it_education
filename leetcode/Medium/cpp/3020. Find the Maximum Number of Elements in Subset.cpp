#include <vector>
#include <unordered_map>
#include <algorithm>
#include <cmath>

class Solution {
public:
    /**
     * Находит максимальную длину подмножества, в котором существуют три элемента
     * x, y, z (не обязательно различных по индексам, но могут быть равны по значению),
     * таких что x * y == z.
     * 
     * @param nums вектор целых чисел
     * @return int максимальная длина подмножества
     */
    int maximumLength(vector<int>& nums) {
        unordered_map<int, int> freq;
        for (int num : nums) {
            freq[num]++;
        }
        
        int maxLen = 0;
        
        // Обрабатываем единицы
        if (freq.count(1)) {
            int countOnes = freq[1];
            maxLen = max(maxLen, countOnes % 2 == 1 ? countOnes : countOnes - 1);
        }
        
        unordered_map<int, bool> visited;
        const long long LIMIT = 1e9;
        
        for (auto& [num, count] : freq) {
            if (num == 1 || visited[num]) continue;
            
            int chainLen = 0;
            long long current = num;
            
            while (freq.count(current) && current <= LIMIT) {
                visited[current] = true;
                
                if (freq[current] >= 2) {
                    chainLen += 2;
                } else {
                    chainLen += 1;
                    break;
                }
                
                current = current * current;
            }
            
            maxLen = max(maxLen, chainLen);
        }
        
        return maxLen;
    }
};