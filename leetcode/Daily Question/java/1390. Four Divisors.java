/**
 * https://leetcode.com/problems/four-divisors/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Four Divisors"
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

import java.util.HashSet;
import java.util.Set;

class Solution {
    public int sumFourDivisors(int[] nums) {
        int totalSum = 0;
        
        for (int num : nums) {
            totalSum += getDivisorsSum(num);
        }
        
        return totalSum;
    }
    
    private int getDivisorsSum(int num) {
        // Всегда есть делители 1 и само число
        Set<Integer> divisors = new HashSet<>();
        divisors.add(1);
        divisors.add(num);
        
        // Перебираем возможные делители до sqrt(num)
        int sqrtNum = (int) Math.sqrt(num);
        for (int i = 2; i <= sqrtNum; i++) {
            if (num % i == 0) {
                divisors.add(i);
                divisors.add(num / i);
                
                // Если уже больше 4 делителей, можно прекратить
                if (divisors.size() > 4) {
                    return 0;
                }
            }
        }
        
        // Проверяем, что делителей ровно 4
        if (divisors.size() == 4) {
            int sum = 0;
            for (int div : divisors) {
                sum += div;
            }
            return sum;
        }
        
        return 0;
    }
}