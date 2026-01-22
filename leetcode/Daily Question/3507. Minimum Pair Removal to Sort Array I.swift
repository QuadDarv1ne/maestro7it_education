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

// ==================== Swift ====================

class Solution {
    /**
     * Возвращает минимальное количество операций для сортировки массива.
     * 
     * Операция: выбрать соседнюю пару с минимальной суммой (самую левую при равенстве),
     * заменить пару на их сумму.
     */
    func minimumPairRemoval(_ nums: [Int]) -> Int {
        var arr = nums
        var operations = 0
        
        func isNonDecreasing(_ a: [Int]) -> Bool {
            for i in 1..<a.count {
                if a[i] < a[i - 1] {
                    return false
                }
            }
            return true
        }
        
        while !isNonDecreasing(arr) {
            var minSum = arr[0] + arr[1]
            var minIndex = 0
            
            for i in 1..<(arr.count - 1) {
                let currentSum = arr[i] + arr[i + 1]
                if currentSum < minSum {
                    minSum = currentSum
                    minIndex = i
                }
            }
            
            arr[minIndex] = minSum
            arr.remove(at: minIndex + 1)
            operations += 1
        }
        
        return operations
    }
}