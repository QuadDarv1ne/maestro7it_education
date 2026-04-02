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
 * 
 * Строит лексикографически наименьшую строку, удовлетворяющую условиям.
 */

class Solution {
    public String generateString(String str1, String str2) {
        int n = str1.length();
        int m = str2.length();
        int len = n + m - 1;
        
        char[] s = new char[len];
        
        // Фиксируем все 'T' позиции
        for (int i = 0; i < n; ++i) {
            if (str1.charAt(i) == 'T') {
                for (int j = 0; j < m; ++j) {
                    int idx = i + j;
                    if (s[idx] == '\0') {
                        s[idx] = str2.charAt(j);
                    } else if (s[idx] != str2.charAt(j)) {
                        return "";
                    }
                }
            }
        }
        
        // Проверяем 'F' позиции на конфликты
        for (int i = 0; i < n; ++i) {
            if (str1.charAt(i) == 'F') {
                boolean match = true;
                for (int j = 0; j < m; ++j) {
                    int idx = i + j;
                    if (s[idx] == '\0') {
                        match = false;
                        break;
                    }
                    if (s[idx] != str2.charAt(j)) {
                        match = false;
                        break;
                    }
                }
                if (match) {
                    return "";
                }
            }
        }
        
        // Заполняем пустые позиции 'a'
        for (int i = 0; i < len; ++i) {
            if (s[i] == '\0') {
                s[i] = 'a';
            }
        }
        
        // Обрабатываем 'F' позиции, где подстрока стала равна str2
        for (int i = 0; i < n; ++i) {
            if (str1.charAt(i) == 'F') {
                boolean equal = true;
                for (int j = 0; j < m; ++j) {
                    if (s[i + j] != str2.charAt(j)) {
                        equal = false;
                        break;
                    }
                }
                if (equal) {
                    boolean changed = false;
                    for (int j = m - 1; j >= 0; --j) {
                        int idx = i + j;
                        if (s[idx] < 'z') {
                            s[idx]++;
                            changed = true;
                            break;
                        }
                    }
                    if (!changed) {
                        return "";
                    }
                }
            }
        }
        
        // Финальная проверка
        String result = new String(s);
        for (int i = 0; i < n; ++i) {
            String sub = result.substring(i, i + m);
            if (str1.charAt(i) == 'T' && !sub.equals(str2)) {
                return "";
            }
            if (str1.charAt(i) == 'F' && sub.equals(str2)) {
                return "";
            }
        }
        
        return result;
    }
}