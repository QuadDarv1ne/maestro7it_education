/**
 * Максимальная площадь квадратного отверстия в сетке
 */
public class Solution {
    public int MaximizeSquareHoleArea(int n, int m, int[] hBars, int[] vBars) {
        Array.Sort(hBars);
        Array.Sort(vBars);
        
        int maxHGap = FindMaxConsecutive(hBars);
        int maxVGap = FindMaxConsecutive(vBars);
        
        int side = Math.Min(maxHGap, maxVGap) + 1;
        return side * side;
    }
    
    private int FindMaxConsecutive(int[] arr) {
        if (arr.Length == 0) return 0;
        int maxGap = 1;
        int current = 1;
        for (int i = 1; i < arr.Length; i++) {
            if (arr[i] == arr[i-1] + 1) {
                current++;
            } else {
                maxGap = Math.Max(maxGap, current);
                current = 1;
            }
        }
        return Math.Max(maxGap, current);
    }
}