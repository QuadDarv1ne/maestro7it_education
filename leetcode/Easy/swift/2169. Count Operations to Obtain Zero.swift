/*
https://leetcode.com/problems/count-operations-to-obtain-zero/description/?envType=daily-question&envId=2025-11-09
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

/// Подсчитывает количество операций, необходимых для получения нуля из двух неотрицательных целых чисел.
/// Этот метод вычисляет количество операций, необходимых для того, чтобы сделать либо num1, либо num2 равным нулю.
/// В одной операции, если num1 >= num2, вычитаем num2 из num1, иначе вычитаем num1 из num2.
///
/// - Parameter num1: Первое неотрицательное целое число.
/// - Parameter num2: Второе неотрицательное целое число.
/// - Returns: Количество операций, необходимых для того, чтобы сделать либо num1, либо num2 равным нулю.
class Solution {
    func countOperations(_ num1: Int, _ num2: Int) -> Int {
        var operations = 0
        var n1 = num1
        var n2 = num2
        while n1 != 0 && n2 != 0 {
            if n1 >= n2 {
                operations += n1 / n2
                n1 %= n2
            } else {
                operations += n2 / n1
                n2 %= n1
            }
        }
        return operations
    }
}

/*
Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
8. Ник в телеграм: @quadd4rv1n7
9. Ник в ВК: https://vk.com/dupley_maxim_1999
*/
