public class Solution {
    /// <summary>
    /// Находит максимальную длину подмножества, в котором существуют три элемента
    /// x, y, z (не обязательно различных по индексам, но могут быть равны по значению),
    /// таких что x * y == z.
    /// </summary>
    /// <param name="nums">Массив целых чисел</param>
    /// <returns>Максимальная длина подмножества</returns>
    public int MaximumLength(int[] nums) {
        Dictionary<int, int> freq = new Dictionary<int, int>();
        foreach (int num in nums) {
            if (freq.ContainsKey(num))
                freq[num]++;
            else
                freq[num] = 1;
        }
        
        int maxLen = 0;
        const long LIMIT = 1000000000;
        
        // Обрабатываем единицы
        if (freq.ContainsKey(1)) {
            int countOnes = freq[1];
            maxLen = Math.Max(maxLen, countOnes % 2 == 1 ? countOnes : countOnes - 1);
        }
        
        HashSet<int> visited = new HashSet<int>();
        
        foreach (var pair in freq) {
            int num = pair.Key;
            if (num == 1 || visited.Contains(num)) continue;
            
            int chainLen = 0;
            long current = num;
            
            while (freq.ContainsKey((int)current) && current <= LIMIT) {
                visited.Add((int)current);
                
                if (freq[(int)current] >= 2) {
                    chainLen += 2;
                } else {
                    chainLen += 1;
                    break;
                }
                
                current = current * current;
            }
            
            maxLen = Math.Max(maxLen, chainLen);
        }
        
        return maxLen;
    }
}