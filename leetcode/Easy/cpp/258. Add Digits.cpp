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

class Solution {
public:
    /**
     * Вычисляет цифровой корень числа (рекурсивную сумму цифр до одной цифры).
     * 
     * Алгоритм 1 (математический):
     * Цифровой корень числа num можно вычислить по формуле:
     * - Если num == 0: возвращаем 0
     * - Иначе: 1 + (num - 1) % 9
     * 
     * Алгоритм 2 (итеративный):
     * 1. Пока число имеет более одной цифры:
     *    - Складываем все его цифры
     *    - Заменяем число на сумму цифр
     * 2. Возвращаем полученную одну цифру
     * 
     * Сложность:
     * Математический: O(1) по времени, O(1) по памяти
     * Итеративный: O(log n) по времени, O(1) по памяти
     * 
     * @param num Исходное число
     * @return Цифровой корень числа (одна цифра)
     * 
     * Примеры:
     * addDigits(38) → 2
     * addDigits(0) → 0
     * addDigits(123) → 6
     */
    int addDigits(int num) {
        // Математический подход (цифровой корень)
        if (num == 0) {
            return 0;
        }
        return 1 + (num - 1) % 9;
    }
    
    /**
     * Итеративное решение.
     * 
     * @param num Исходное число
     * @return Цифровой корень
     */
    int addDigitsIterative(int num) {
        while (num >= 10) {
            int digitSum = 0;
            int temp = num;
            
            // Суммируем цифры текущего числа
            while (temp > 0) {
                digitSum += temp % 10;  // Добавляем последнюю цифру
                temp /= 10;             // Удаляем последнюю цифру
            }
            
            num = digitSum;
        }
        
        return num;
    }
    
    /**
     * Рекурсивное решение.
     * 
     * @param num Исходное число
     * @return Цифровой корень
     */
    int addDigitsRecursive(int num) {
        if (num < 10) {
            return num;
        }
        
        int digitSum = 0;
        int temp = num;
        
        // Суммируем цифры
        while (temp > 0) {
            digitSum += temp % 10;
            temp /= 10;
        }
        
        // Рекурсивно вызываем для суммы
        return addDigitsRecursive(digitSum);
    }
};