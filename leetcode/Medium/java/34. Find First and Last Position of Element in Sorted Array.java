class Solution {
    /**
     * Автор: Дуплей Максим Игоревич
     * ORCID: https://orcid.org/0009-0007-7605-539X
     * GitHub: https://github.com/QuadDarv1ne/
     * 
     * Алгоритм: Бинарный поиск для нахождения начальной и конечной позиции
     * Сложность: O(log n) по времени, O(1) по памяти
     */
    public int[] searchRange(int[] nums, int target) {
        int first = findFirst(nums, target);
        int last = findLast(nums, target);
        
        return new int[]{first, last};
    }
    
    private int findFirst(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        int first = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (nums[mid] >= target) {
                if (nums[mid] == target) {
                    first = mid;
                }
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        }
        
        return first;
    }
    
    private int findLast(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        int last = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (nums[mid] <= target) {
                if (nums[mid] == target) {
                    last = mid;
                }
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return last;
    }
}

/*
 * Полезные ссылки автора:
 * Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * Telegram: @quadd4rv1n7, @dupley_maxim_1999
 * Rutube: https://rutube.ru/channel/4218729/
 * Plvideo: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * YouTube: https://www.youtube.com/@it-coders
 * VK: https://vk.com/science_geeks
 */