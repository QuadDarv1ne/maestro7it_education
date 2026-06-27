class Solution {
    /**
     * Находит максимальную длину подмножества, в котором существуют три элемента
     * x, y, z (не обязательно различных по индексам, но могут быть равны по значению),
     * таких что x * y == z.
     * 
     * @param nums массив целых чисел
     * @return максимальная длина подмножества
     */
    public int maximumLength(int[] nums) {
        Map<Integer, Integer> freq = new HashMap<>();
        for (int num : nums) {
            freq.put(num, freq.getOrDefault(num, 0) + 1);
        }
        
        int maxLen = 0;
        final long LIMIT = 1_000_000_000;
        
        // Обрабатываем единицы
        if (freq.containsKey(1)) {
            int countOnes = freq.get(1);
            maxLen = Math.max(maxLen, countOnes % 2 == 1 ? countOnes : countOnes - 1);
        }
        
        Set<Integer> visited = new HashSet<>();
        
        for (Map.Entry<Integer, Integer> entry : freq.entrySet()) {
            int num = entry.getKey();
            if (num == 1 || visited.contains(num)) continue;
            
            int chainLen = 0;
            long current = num;
            
            while (freq.containsKey((int)current) && current <= LIMIT) {
                visited.add((int)current);
                
                if (freq.get((int)current) >= 2) {
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
    }
}