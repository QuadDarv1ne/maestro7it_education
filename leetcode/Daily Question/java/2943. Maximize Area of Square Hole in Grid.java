/**
 * Максимальная площадь квадратного отверстия в сетке
 */
class Solution {
    public int maximizeSquareHoleArea(int n, int m, int[] hBars, int[] vBars) {
        Arrays.sort(hBars);
        Arrays.sort(vBars);
        
        int maxHGap = findMaxConsecutive(hBars);
        int maxVGap = findMaxConsecutive(vBars);
        
        int side = Math.min(maxHGap, maxVGap) + 1;
        return side * side;
    }
    
    private int findMaxConsecutive(int[] arr) {
        if (arr.length == 0) return 0;
        int maxGap = 1;
        int current = 1;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] == arr[i-1] + 1) {
                current++;
            } else {
                maxGap = Math.max(maxGap, current);
                current = 1;
            }
        }
        return Math.max(maxGap, current);
    }
}