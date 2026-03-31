/**
 * https://leetcode.com/problems/lexicographically-smallest-generated-string/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "3474. Lexicographically Smallest Generated String" на Java
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
    public String generateString(String str1, String str2) {
        int n = str1.length(), m = str2.length(), L = n + m - 1;
        int[] word = new int[L];
        Arrays.fill(word, -1); // -1 = символ не определен
        
        // Шаг 1: Фиксируем символы из T-условий
        for (int i = 0; i < n; i++) {
            if (str1.charAt(i) == 'T') {
                for (int k = 0; k < m; k++) {
                    int pos = i + k;
                    if (pos >= L) return "";
                    if (word[pos] != -1 && word[pos] != str2.charAt(k)) return "";
                    word[pos] = str2.charAt(k);
                }
            }
        }
        
        // Шаг 2: Находим F-условия, которые нарушатся, если заполнить пустоты 'a'
        List<int[]> violated = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if (str1.charAt(i) == 'F' && wouldMatchIfA(word, str2, i, m, L)) {
                int r = getRightmostUndef(word, i, m, L);
                if (r == -1) return ""; // Невозможно исправить
                violated.add(new int[]{i, r});
            }
        }
        
        // Шаг 3: Жадное исправление (ставим 'b' как можно правее)
        violated.sort((a, b) -> Integer.compare(a[1], b[1]));
        TreeSet<Integer> active = new TreeSet<>();
        
        for (int[] v : violated) {
            int i = v[0], r = v[1];
            Integer next = active.ceiling(i);
            // Если уже стоящая 'b' не ломает текущее F-условие
            if (next == null || next > i + m - 1) {
                active.add(r);
                word[r] = 'b';
            }
        }
        
        // Шаг 4: Заполняем оставшиеся неопределенные позиции 'a'
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < L; i++) {
            sb.append((char) (word[i] == -1 ? 'a' : word[i]));
        }
        
        return sb.toString();
    }
    
    private boolean wouldMatchIfA(int[] word, String str2, int i, int m, int L) {
        for (int k = 0; k < m; k++) {
            int pos = i + k;
            if (pos >= L) return false;
            if (word[pos] == -1) {
                if (str2.charAt(k) != 'a') return false;
            } else {
                if (word[pos] != str2.charAt(k)) return false;
            }
        }
        return true;
    }
    
    private int getRightmostUndef(int[] word, int i, int m, int L) {
        int r = -1;
        for (int k = 0; k < m; k++) {
            int pos = i + k;
            if (pos < L && word[pos] == -1) r = pos;
        }
        return r;
    }
}