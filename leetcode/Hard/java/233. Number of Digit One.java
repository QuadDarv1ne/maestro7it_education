/**
 * https://leetcode.com/problems/number-of-digit-one/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "233. Number of Digit One"
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
    /**
     * Подсчитывает количество цифр 1 во всех числах от 1 до n.
     * 
     * Алгоритм:
     * Для каждого разряда вычисляем, сколько раз цифра 1 появляется в этом разряде.
     * 
     * Формула для разряда, соответствующего 10^k:
     * - high = n / (10^(k+1))
     * - low = n % (10^k)
     * - cur = (n / (10^k)) % 10
     * 
     * Количество единиц в разряде:
     * count = high * (10^k) + 
     *         (cur > 1 ? 10^k : (cur == 1 ? low + 1 : 0))
     * 
     * Сложность:
     * Время: O(log10(n))
     * Пространство: O(1)
     * 
     * @param n Верхняя граница диапазона чисел
     * @return Общее количество цифр 1
     * 
     * Примеры:
     * countDigitOne(13) → 6
     * countDigitOne(0) → 0
     * countDigitOne(113) → 40
     */
    public int countDigitOne(int n) {
        if (n <= 0) {
            return 0;
        }
        
        long count = 0;  // Используем long для больших чисел
        long factor = 1;  // Текущий разряд: 1, 10, 100, ...
        
        while (factor <= n) {
            // Вычисляем high, low, cur для текущего разряда
            long high = n / (factor * 10);
            long low = n % factor;
            int cur = (int)((n / factor) % 10);
            
            // Добавляем базовую часть: high * factor
            count += high * factor;
            
            // Добавляем дополнительную часть в зависимости от cur
            if (cur > 1) {
                count += factor;
            } else if (cur == 1) {
                count += low + 1;
            }
            // Если cur == 0, ничего не добавляем
            
            // Переходим к следующему разряду
            factor *= 10;
        }
        
        return (int)count;
    }
    
    /**
     * Наивное решение для проверки (неэффективно для больших n).
     * 
     * @param n Верхняя граница диапазона
     * @return Количество цифр 1
     */
    public int countDigitOneBruteforce(int n) {
        int count = 0;
        for (int i = 1; i <= n; i++) {
            int num = i;
            while (num > 0) {
                if (num % 10 == 1) {
                    count++;
                }
                num /= 10;
            }
        }
        return count;
    }
}