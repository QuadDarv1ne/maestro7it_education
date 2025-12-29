/**
 * https://leetcode.com/problems/pyramid-transition-matrix/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Pyramid Transition Matrix"
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
    /**
     * Определяет, можно ли построить пирамиду из заданного основания.
     * 
     * @param bottom строка основания пирамиды
     * @param allowed список разрешенных троек вида "XYZ", где XY - основание, Z - вершина
     * @return true если пирамиду можно построить, иначе false
     */
    public bool PyramidTransition(string bottom, IList<string> allowed) {
        // Создаем словарь для быстрого поиска разрешенных вершин
        var allowedMap = new Dictionary<string, List<char>>();
        foreach (var triple in allowed) {
            var baseStr = triple.Substring(0, 2);
            var top = triple[2];
            
            if (!allowedMap.ContainsKey(baseStr)) {
                allowedMap[baseStr] = new List<char>();
            }
            allowedMap[baseStr].Add(top);
        }
        
        // Мемоизация для оптимизации
        var memo = new Dictionary<string, bool>();
        
        return Dfs(bottom, allowedMap, memo);
    }
    
    private bool Dfs(string current, Dictionary<string, List<char>> allowedMap, 
                    Dictionary<string, bool> memo) {
        // Если уже вычисляли для этого уровня - возвращаем результат
        if (memo.ContainsKey(current)) {
            return memo[current];
        }
        
        // Базовый случай: достигли вершины пирамиды
        if (current.Length == 1) {
            memo[current] = true;
            return true;
        }
        
        // Генерируем все возможные следующие уровни
        var nextLevels = new List<string>();
        GenerateNextLevels(current, "", 0, allowedMap, nextLevels);
        
        // Если не удалось сгенерировать следующий уровень
        if (nextLevels.Count == 0) {
            memo[current] = false;
            return false;
        }
        
        // Проверяем каждый возможный следующий уровень
        foreach (var next in nextLevels) {
            if (Dfs(next, allowedMap, memo)) {
                memo[current] = true;
                return true;
            }
        }
        
        memo[current] = false;
        return false;
    }
    
    /**
     * Генерирует все возможные следующие уровни пирамиды.
     */
    private void GenerateNextLevels(string current, string next, int idx,
                                   Dictionary<string, List<char>> allowedMap,
                                   List<string> result) {
        // Если следующий уровень полностью построен
        if (next.Length == current.Length - 1) {
            result.Add(next);
            return;
        }
        
        // Текущая пара символов
        var pair = current.Substring(idx, 2);
        
        // Если для этой пары нет разрешенных вершин - прерываем генерацию
        if (!allowedMap.ContainsKey(pair)) {
            return;
        }
        
        // Перебираем все возможные вершины для текущей пары
        foreach (var top in allowedMap[pair]) {
            GenerateNextLevels(current, next + top, idx + 1, allowedMap, result);
        }
    }
}