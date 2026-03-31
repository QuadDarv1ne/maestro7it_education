/**
 * https://leetcode.com/problems/lexicographically-smallest-generated-string/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "3474. Lexicographically Smallest Generated String" на CSharp
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

using System;
using System.Collections.Generic;

public class Solution {
    public string GenerateString(string str1, string str2) {
        int n = str1.Length, m = str2.Length, L = n + m - 1;
        int[] word = new int[L];
        for (int i = 0; i < L; i++) word[i] = -1; // -1 = не определено
        
        // Шаг 1: Фиксируем символы из T-условий
        for (int i = 0; i < n; i++) {
            if (str1[i] == 'T') {
                for (int k = 0; k < m; k++) {
                    int pos = i + k;
                    if (pos >= L) return "";
                    if (word[pos] != -1 && word[pos] != str2[k]) return "";
                    word[pos] = str2[k];
                }
            }
        }
        
        // Локальная функция проверки конфликта
        bool WouldMatchIfA(int i) {
            for (int k = 0; k < m; k++) {
                int pos = i + k;
                if (pos >= L) return false;
                if (word[pos] == -1) {
                    if (str2[k] != 'a') return false;
                } else {
                    if (word[pos] != str2[k]) return false;
                }
            }
            return true;
        }
        
        // Локальная функция поиска крайней правой пустой позиции
        int GetRightmostUndef(int i) {
            int r = -1;
            for (int k = 0; k < m; k++) {
                int pos = i + k;
                if (pos < L && word[pos] == -1) r = pos;
            }
            return r;
        }
        
        // Шаг 2: Собираем нарушенные F-условия
        List<(int i, int r)> violated = new List<(int, int)>();
        for (int i = 0; i < n; i++) {
            if (str1[i] == 'F' && WouldMatchIfA(i)) {
                int r = GetRightmostUndef(i);
                if (r == -1) return "";
                violated.Add((i, r));
            }
        }
        
        // Сортируем по правой позиции
        violated.Sort((a, b) => a.r.CompareTo(b.r));
        
        // Шаг 3: Жадное исправление через SortedSet
        SortedSet<int> active = new SortedSet<int>();
        foreach (var v in violated) {
            // Проверяем, есть ли уже 'b' в диапазоне [v.i, v.i + m - 1]
            var view = active.GetViewBetween(v.i, v.i + m - 1);
            if (view.Count == 0) {
                active.Add(v.r);
                word[v.r] = 'b';
            }
        }
        
        // Шаг 4: Сборка финальной строки
        char[] res = new char[L];
        for (int i = 0; i < L; i++) {
            res[i] = (char)(word[i] == -1 ? 'a' : word[i]);
        }
        
        return new string(res);
    }
}