/**
 * https://leetcode.com/problems/sort-vowels-in-a-string/description/?envType=daily-question&envId=2025-09-11
 */

import java.util.*;

class Solution {
    /**
     * Метод sortVowels принимает строку и сортирует все гласные буквы
     * в порядке возрастания (по Unicode), оставляя остальные символы
     * без изменений.
     *
     * Алгоритм:
     * 1. Извлекаем гласные из строки.
     * 2. Сортируем их.
     * 3. Вставляем обратно на места гласных.
     *
     * Временная сложность: O(n log n).
     */
    private boolean isVowel(char c) {
        c = Character.toLowerCase(c);
        return c=='a'||c=='e'||c=='i'||c=='o'||c=='u';
    }
    
    public String sortVowels(String s) {
        List<Character> vowels = new ArrayList<>();
        for (char c : s.toCharArray()) {
            if (isVowel(c)) {
                vowels.add(c);
            }
        }
        Collections.sort(vowels);
        StringBuilder sb = new StringBuilder();
        int vi = 0;
        for (char c : s.toCharArray()) {
            if (isVowel(c)) {
                sb.append(vowels.get(vi++));
            } else {
                sb.append(c);
            }
        }
        return sb.toString();
    }
}

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/