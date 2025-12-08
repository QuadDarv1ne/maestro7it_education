class Solution {
    /**
     * Сортировка цветов (Dutch National Flag алгоритм)
     * 
     * Алгоритм: Three-way partition
     * Сложность: O(n) по времени, O(1) по памяти
     * 
     * @param nums массив целых чисел (0, 1, 2)
     */
    public void sortColors(int[] nums) {
        int low = 0;          // Конец нулей
        int mid = 0;          // Текущий элемент
        int high = nums.length - 1;  // Начало двоек
        
        while (mid <= high) {
            if (nums[mid] == 0) {
                // Обмен и сдвиг для нулей
                swap(nums, low, mid);
                low++;
                mid++;
            } else if (nums[mid] == 1) {
                // Единицы остаются на месте
                mid++;
            } else { // nums[mid] == 2
                // Обмен и сдвиг для двоек
                swap(nums, mid, high);
                high--;
                // Не увеличиваем mid, нужно проверить новый элемент
            }
        }
    }
    
    /**
     * Альтернативное решение: counting sort
     */
    public void sortColorsCounting(int[] nums) {
        int count0 = 0, count1 = 0, count2 = 0;
        
        // Подсчет элементов
        for (int num : nums) {
            if (num == 0) count0++;
            else if (num == 1) count1++;
            else count2++;
        }
        
        // Заполнение массива
        int index = 0;
        for (int i = 0; i < count0; i++) nums[index++] = 0;
        for (int i = 0; i < count1; i++) nums[index++] = 1;
        for (int i = 0; i < count2; i++) nums[index++] = 2;
    }
    
    /**
     * Вспомогательная функция для обмена элементов
     */
    private void swap(int[] nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
    
    /**
     * Расширенная версия для k цветов
     */
    public void sortColorsK(int[] nums, int k) {
        int[] count = new int[k + 1];
        
        // Подсчет каждого цвета
        for (int num : nums) {
            count[num]++;
        }
        
        // Заполнение массива
        int index = 0;
        for (int color = 0; color <= k; color++) {
            for (int i = 0; i < count[color]; i++) {
                nums[index++] = color;
            }
        }
    }
    
    // Пример использования
    public static void main(String[] args) {
        Solution solution = new Solution();
        
        // Тестовые случаи
        int[][] testCases = {
            {2,0,2,1,1,0},
            {2,0,1},
            {0},
            {1,0},
            {2,2,2,2},
            {1,1,1,1},
            {0,0,0,0},
            {2,1,0}
        };
        
        int[][] expected = {
            {0,0,1,1,2,2},
            {0,1,2},
            {0},
            {0,1},
            {2,2,2,2},
            {1,1,1,1},
            {0,0,0,0},
            {0,1,2}
        };
        
        System.out.println("Тестирование Dutch National Flag алгоритма:");
        for (int i = 0; i < testCases.length; i++) {
            int[] nums = testCases[i].clone();
            solution.sortColors(nums);
            
            boolean passed = java.util.Arrays.equals(nums, expected[i]);
            System.out.print(passed ? "✓ " : "✗ ");
            System.out.print("Тест " + (i + 1) + ": Вход: ");
            printArray(testCases[i]);
            System.out.print(" -> Результат: ");
            printArray(nums);
            System.out.println();
        }
    }
    
    private static void printArray(int[] arr) {
        for (int num : arr) {
            System.out.print(num + " ");
        }
    }
}