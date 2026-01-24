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

impl Solution {
    /**
     * Минимизирует максимальную сумму пары в массиве
     * 
     * Сортирует массив и формирует пары из первого с последним,
     * второго с предпоследним и т.д. Возвращает максимальную сумму пар.
     * 
     * Сложность: O(n log n) по времени, O(1) дополнительной памяти
     */
    pub fn min_pair_sum(nums: Vec<i32>) -> i32 {
        let mut nums = nums;
        nums.sort();
        let n = nums.len();
        let mut max_sum = 0;
        
        for i in 0..n/2 {
            let current_sum = nums[i] + nums[n - 1 - i];
            if current_sum > max_sum {
                max_sum = current_sum;
            }
        }
        
        max_sum
    }
}