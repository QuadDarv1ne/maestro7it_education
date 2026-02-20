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

import java.util.*;

class Solution {
    /**
     * Преобразует специальную двоичную строку в лексикографически наибольшую.
     *
     * @param s исходная специальная строка (например, "11011000")
     * @return максимально возможная строка после перестановок (например, "11100100")
     */
    public String makeLargestSpecial(String s) {
        return dfs(s);
    }
    
    private String dfs(String s) {
        if (s.isEmpty()) return "";
        
        List<String> groups = new ArrayList<>();
        int balance = 0;
        int left = 0;
        
        for (int i = 0; i < s.length(); i++) {
            balance += (s.charAt(i) == '1') ? 1 : -1;
            if (balance == 0) {
                // Рекурсивно обрабатываем внутреннюю часть (без первого и последнего символа)
                String inner = dfs(s.substring(left + 1, i));
                groups.add("1" + inner + "0");
                left = i + 1;
            }
        }
        
        // Сортируем группы по убыванию (лексикографически)
        groups.sort(Collections.reverseOrder());
        
        // Объединяем с помощью StringBuilder
        StringBuilder sb = new StringBuilder();
        for (String g : groups) {
            sb.append(g);
        }
        return sb.toString();
    }
}