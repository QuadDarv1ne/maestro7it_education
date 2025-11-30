/**
 * https://leetcode.com/problems/permutation-sequence/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Permutation Sequence" на Java
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

import java.util.*;

class Solution {
    public String getPermutation(int n, int k) {
        // Вычисляем факториалы
        int[] factorials = new int[n];
        factorials[0] = 1;
        for (int i = 1; i < n; i++) {
            factorials[i] = factorials[i-1] * i;
        }
        
        // Создаем список доступных чисел
        List<Integer> numbers = new ArrayList<>();
        for (int i = 1; i <= n; i++) {
            numbers.add(i);
        }
        
        StringBuilder result = new StringBuilder();
        k--;  // Переход к 0-индексации
        
        for (int i = n - 1; i >= 0; i--) {
            int index = k / factorials[i];
            k %= factorials[i];
            
            result.append(numbers.get(index));
            numbers.remove(index);
        }
        
        return result.toString();
    }
}