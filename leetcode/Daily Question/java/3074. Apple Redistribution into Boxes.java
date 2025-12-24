/**
 * Задача: Минимальное количество коробок для перераспределения яблок (LeetCode #3074)
 * 
 * Описание:
 * Даны два массива:
 * 1. apple - где apple[i] представляет количество яблок в i-й корзине
 * 2. capacity - где capacity[j] представляет вместимость j-й коробки
 * 
 * Необходимо найти минимальное количество коробок, достаточное для упаковки всех яблок.
 * 
 * Автор: Дуплей Максим Игоревич
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
 * 
 * Сложность:
 * - Время: O(n log n) из-за сортировки
 * - Память: O(1) (не считая входных данных)
 */

import java.util.Arrays;
import java.util.Collections;

class Solution {
    public int minimumBoxes(int[] apple, int[] capacity) {
        // Считаем общее количество яблок
        int totalApples = 0;
        for (int apples : apple) {
            totalApples += apples;
        }
        
        // Сортируем коробки по убыванию вместимости
        // Для примитивного типа int нужно отсортировать, затем перевернуть
        Arrays.sort(capacity);
        reverseArray(capacity);
        
        // Жадный алгоритм: берем самые вместительные коробки
        int currentCapacity = 0;
        int boxesUsed = 0;
        
        for (int boxCapacity : capacity) {
            boxesUsed++;
            currentCapacity += boxCapacity;
            
            // Если набрали достаточную вместимость
            if (currentCapacity >= totalApples) {
                return boxesUsed;
            }
        }
        
        return boxesUsed; // Теоретически недостижимо
    }
    
    // Вспомогательный метод для переворота массива
    private void reverseArray(int[] arr) {
        int left = 0;
        int right = arr.length - 1;
        while (left < right) {
            int temp = arr[left];
            arr[left] = arr[right];
            arr[right] = temp;
            left++;
            right--;
        }
    }
}

// Альтернативная Java реализация с использованием Integer[]
class Solution2 {
    public int minimumBoxes(int[] apple, int[] capacity) {
        // Считаем общее количество яблок
        int totalApples = Arrays.stream(apple).sum();
        
        // Преобразуем int[] в Integer[] для сортировки с компаратором
        Integer[] capacityBoxed = Arrays.stream(capacity)
                                      .boxed()
                                      .toArray(Integer[]::new);
        
        // Сортируем по убыванию
        Arrays.sort(capacityBoxed, Collections.reverseOrder());
        
        // Жадный алгоритм
        int currentCapacity = 0;
        int boxesUsed = 0;
        
        for (int boxCapacity : capacityBoxed) {
            boxesUsed++;
            currentCapacity += boxCapacity;
            
            if (currentCapacity >= totalApples) {
                return boxesUsed;
            }
        }
        
        return boxesUsed;
    }
}