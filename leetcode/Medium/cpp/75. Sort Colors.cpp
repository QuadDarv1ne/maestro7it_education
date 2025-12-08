#include <vector>
#include <iostream>
using namespace std;

class Solution {
public:
    /**
     * Сортировка цветов (Dutch National Flag алгоритм)
     * 
     * Алгоритм: Three-way partition
     * Сложность: O(n) по времени, O(1) по памяти
     * 
     * @param nums вектор целых чисел (0, 1, 2)
     */
    void sortColors(vector<int>& nums) {
        int low = 0;      // Конец нулей
        int mid = 0;      // Текущий элемент
        int high = nums.size() - 1;  // Начало двоек
        
        while (mid <= high) {
            switch (nums[mid]) {
                case 0:
                    // Обмен и сдвиг для нулей
                    swap(nums[low], nums[mid]);
                    low++;
                    mid++;
                    break;
                case 1:
                    // Единицы остаются на месте
                    mid++;
                    break;
                case 2:
                    // Обмен и сдвиг для двоек
                    swap(nums[mid], nums[high]);
                    high--;
                    break;
            }
        }
    }
    
    /**
     * Альтернативное решение: counting sort
     */
    void sortColorsCounting(vector<int>& nums) {
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
     * Расширенная версия для k цветов
     */
    void sortColorsK(vector<int>& nums, int k) {
        vector<int> count(k + 1, 0);
        
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
};