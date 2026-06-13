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
    public String mapWordWeights(String[] words, int[] weights) {
        StringBuilder result = new StringBuilder();
        
        // Проходим по каждому слову
        for (String word : words) {
            int sum = 0;
            
            // Вычисляем вес слова
            for (int i = 0; i < word.length(); i++) {
                char c = word.charAt(i);
                // 'a' имеет индекс 0, 'b' - 1 и т.д.
                sum += weights[c - 'a'];
            }
            
            // Берем остаток от деления на 26
            int rem = sum % 26;
            
            // Отображаем в букву: 0 -> 'z', 1 -> 'y', ..., 25 -> 'a'
            // Формула: 'z' - rem
            char mappedChar = (char) ('z' - rem);
            
            result.append(mappedChar);
        }
        
        return result.toString();
    }
}