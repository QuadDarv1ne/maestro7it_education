/**
 * https://leetcode.com/problems/vowel-spellchecker/description/?envType=daily-question&envId=2025-09-14
 */

import java.util.*;

class Solution {
    /**
     * Решение задачи Vowel Spellchecker.
     * 
     * Для каждого запроса из queries ищем слово в wordlist по следующим правилам:
     * 1. Точное совпадение.
     * 2. Совпадение без учета регистра (первое найденное).
     * 3. Совпадение с заменой всех гласных на '*' (первое найденное).
     * 4. Если ничего не найдено, возвращаем пустую строку.
     */
    public String[] spellchecker(String[] wordlist, String[] queries) {
        // Создаем множество для точных совпадений
        Set<String> exact = new HashSet<>(Arrays.asList(wordlist));
        // Словарь для регистра-независимого поиска: ключ — слово в нижнем регистре, значение — первое слово из wordlist
        Map<String, String> caseInsensitive = new HashMap<>();
        // Словарь для поиска с заменой гласных на '*': ключ — строка с замененными гласными, значение — первое слово
        Map<String, String> vowelInsensitive = new HashMap<>();
        
        for (String word : wordlist) {
            String lower = word.toLowerCase();
            // Если в caseInsensitive еще нет этого нижнего регистра, добавляем
            if (!caseInsensitive.containsKey(lower)) {
                caseInsensitive.put(lower, word);
            }
            // Заменяем гласные на * в lower
            StringBuilder sb = new StringBuilder();
            for (char c : lower.toCharArray()) {
                // Проверяем, является ли символ гласной
                if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
                    sb.append('*');
                } else {
                    sb.append(c);
                }
            }
            String vowelKey = sb.toString();
            // Если в vowelInsensitive еще нет этого ключа, добавляем
            if (!vowelInsensitive.containsKey(vowelKey)) {
                vowelInsensitive.put(vowelKey, word);
            }
        }
        
        String[] result = new String[queries.length];
        for (int i = 0; i < queries.length; i++) {
            String query = queries[i];
            // Проверяем точное совпадение
            if (exact.contains(query)) {
                result[i] = query;
                continue;
            }
            String lowerQuery = query.toLowerCase();
            // Проверяем регистра-независимое совпадение
            if (caseInsensitive.containsKey(lowerQuery)) {
                result[i] = caseInsensitive.get(lowerQuery);
                continue;
            }
            // Заменяем гласные в lowerQuery на '*'
            StringBuilder sb = new StringBuilder();
            for (char c : lowerQuery.toCharArray()) {
                if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
                    sb.append('*');
                } else {
                    sb.append(c);
                }
            }
            String vowelQuery = sb.toString();
            // Проверяем по ключу с замененными гласными
            if (vowelInsensitive.containsKey(vowelQuery)) {
                result[i] = vowelInsensitive.get(vowelQuery);
            } else {
                result[i] = "";
            }
        }
        return result;
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