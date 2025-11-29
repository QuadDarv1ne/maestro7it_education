/**
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * LeetCode 34: Find First and Last Position of Element in Sorted Array
 * 
 * Алгоритм: Бинарный поиск для нахождения начальной и конечной позиции
 * Сложность: O(log n) по времени, O(1) по памяти
 */

class Solution {
    /**
     * Находит первую и последнюю позицию target в отсортированном массиве
     * @param nums отсортированный массив целых чисел
     * @param target искомое значение
     * @return массив [первая позиция, последняя позиция] или [-1, -1]
     */
    public int[] searchRange(int[] nums, int target) {
        int first = findFirst(nums, target);
        int last = findLast(nums, target);
        
        return new int[]{first, last};
    }
    
    /**
     * Находит первое вхождение target в массиве
     * Используем модифицированный бинарный поиск:
     * Когда находим target, продолжаем искать слева
     */
    private int findFirst(int[] nums, int target) {
        int left = 0;
        int right = nums.length - 1;
        int first = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (nums[mid] >= target) {
                if (nums[mid] == target) {
                    first = mid;
                }
                right = mid - 1; // Продолжаем искать слева
            } else {
                left = mid + 1;
            }
        }
        
        return first;
    }
    
    /**
     * Находит последнее вхождение target в массиве
     * Используем модифицированный бинарный поиск:
     * Когда находим target, продолжаем искать справа
     */
    private int findLast(int[] nums, int target) {
        int left = 0;
        int right = nums.length - 1;
        int last = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (nums[mid] <= target) {
                if (nums[mid] == target) {
                    last = mid;
                }
                left = mid + 1; // Продолжаем искать справа
            } else {
                right = mid - 1;
            }
        }
        
        return last;
    }
    
    // ============================================
    // АЛЬТЕРНАТИВНОЕ РЕШЕНИЕ
    // ============================================
    
    /**
     * Альтернативная реализация с единым методом поиска границ
     */
    public int[] searchRangeAlt(int[] nums, int target) {
        int first = findBound(nums, target, true);
        int last = findBound(nums, target, false);
        return new int[]{first, last};
    }
    
    /**
     * Универсальный метод поиска границы
     * @param isFirst true - ищем первое вхождение, false - последнее
     */
    private int findBound(int[] nums, int target, boolean isFirst) {
        int left = 0;
        int right = nums.length - 1;
        int result = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (nums[mid] == target) {
                result = mid;
                if (isFirst) {
                    right = mid - 1; // Ищем первое слева
                } else {
                    left = mid + 1;  // Ищем последнее справа
                }
            } else if (nums[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return result;
    }
}

/*
 * КЛЮЧЕВЫЕ МОМЕНТЫ РЕАЛИЗАЦИИ:
 * 
 * 1. Math.floor() для целочисленного деления
 *    В JavaScript нужно явно округлять результат деления
 * 
 * 2. const вместо let где возможно
 *    Делает код более предсказуемым и безопасным
 * 
 * 3. Два отдельных прохода
 *    Первый ищет левую границу, второй - правую
 * 
 * 4. Условия >= и <= вместо ==
 *    Позволяет продолжать поиск в нужном направлении
 * 
 * ОТЛИЧИЯ ОТ JAVA-ВЕРСИИ:
 * 
 * - Используем const/let вместо типизированных переменных
 * - Math.floor() вместо автоматического целочисленного деления
 * - Стрелочные функции как опция
 * - JSDoc комментарии вместо JavaDoc
 * 
 * Полезные ссылки автора:
 * Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * Telegram: @quadd4rv1n7, @dupley_maxim_1999
 * Rutube: https://rutube.ru/channel/4218729/
 * Plvideo: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * YouTube: https://www.youtube.com/@it-coders
 * VK: https://vk.com/science_geeks
 */