/**
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

class NumArray {
private:
    // Вектор префиксных сумм
    std::vector<int> prefix;
    
public:
    /**
     * Конструктор, инициализирующий объект массивом nums.
     * Вычисляет массив префиксных сумм.
     * @param nums исходный вектор целых чисел
     */
    NumArray(vector<int>& nums) {
        int n = nums.size();
        prefix.resize(n + 1, 0);
        for (int i = 0; i < n; ++i) {
            prefix[i + 1] = prefix[i] + nums[i];
        }
    }
    
    /**
     * Возвращает сумму элементов с индекса left по right включительно.
     * @param left начальный индекс
     * @param right конечный индекс
     * @return сумма на отрезке [left, right]
     */
    int sumRange(int left, int right) {
        return prefix[right + 1] - prefix[left];
    }
};