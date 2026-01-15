/**
 * Максимальная площадь квадратного отверстия в сетке
 * 
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
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