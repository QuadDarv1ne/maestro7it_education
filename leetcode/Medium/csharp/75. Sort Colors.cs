public class Solution {
    /**
     * Сортировка цветов (Dutch National Flag алгоритм)
     * 
     * Алгоритм: Three-way partition
     * Сложность: O(n) по времени, O(1) по памяти
     * 
     * @param nums массив целых чисел (0, 1, 2)
     */
    public void SortColors(int[] nums) {
        int low = 0;          // Конец нулей
        int mid = 0;          // Текущий элемент
        int high = nums.Length - 1;  // Начало двоек
        
        while (mid <= high) {
            switch (nums[mid]) {
                case 0:
                    // Обмен и сдвиг для нулей
                    Swap(nums, low, mid);
                    low++;
                    mid++;
                    break;
                case 1:
                    // Единицы остаются на месте
                    mid++;
                    break;
                case 2:
                    // Обмен и сдвиг для двоек
                    Swap(nums, mid, high);
                    high--;
                    break;
            }
        }
    }
    
    /**
     * Альтернативное решение: counting sort
     */
    public void SortColorsCounting(int[] nums) {
        int count0 = 0, count1 = 0, count2 = 0;
        
        // Подсчет элементов
        foreach (int num in nums) {
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
    private void Swap(int[] nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
    
    /**
     * Расширенная версия для k цветов
     */
    public void SortColorsK(int[] nums, int k) {
        int[] count = new int[k + 1];
        
        // Подсчет каждого цвета
        foreach (int num in nums) {
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
}