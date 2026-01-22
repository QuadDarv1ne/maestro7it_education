3507. Minimum Pair Removal to Sort Array I/**
 * Максимальное скалярное произведение двух подпоследовательностей
 * 
 * @param nums1 Первый массив целых чисел
 * @param nums2 Второй массив целых чисел
 * @return Максимальное скалярное произведение
 * 
 * Сложность: Время O(m*n), Память O(m*n)
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
 */ 
class Solution {
    func maxDotProduct(_ nums1: [Int], _ nums2: [Int]) -> Int {
        let m = nums1.count
        let n = nums2.count
        
        // Инициализация DP таблицы с минимальным значением
        var dp = Array(repeating: Array(repeating: Int.min / 2, count: n + 1), count: m + 1)
        
        // Заполнение таблицы DP
        for i in 1...m {
            for j in 1...n {
                let product = nums1[i - 1] * nums2[j - 1]
                
                // Выбираем максимум из 4 вариантов
                dp[i][j] = max(
                    product,
                    dp[i - 1][j - 1] + product,
                    dp[i - 1][j],
                    dp[i][j - 1]
                )
            }
        }
        
        return dp[m][n]
    }
}