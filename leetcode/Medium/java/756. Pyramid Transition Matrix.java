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

import java.util.*;

class Solution {
    /**
     * Определяет, можно ли построить пирамиду из заданного основания.
     * 
     * @param bottom строка основания пирамиды
     * @param allowed список разрешенных троек вида "XYZ", где XY - основание, Z - вершина
     * @return true если пирамиду можно построить, иначе false
     */
    public boolean pyramidTransition(String bottom, List<String> allowed) {
        // Создаем карту для быстрого поиска разрешенных вершин
        Map<String, List<Character>> allowedMap = new HashMap<>();
        for (String triple : allowed) {
            String base = triple.substring(0, 2);
            char top = triple.charAt(2);
            allowedMap.computeIfAbsent(base, k -> new ArrayList<>()).add(top);
        }
        
        // Мемоизация для оптимизации
        Map<String, Boolean> memo = new HashMap<>();
        
        return dfs(bottom, allowedMap, memo);
    }
    
    private boolean dfs(String current, Map<String, List<Character>> allowedMap, 
                       Map<String, Boolean> memo) {
        // Если уже вычисляли для этого уровня - возвращаем результат
        if (memo.containsKey(current)) {
            return memo.get(current);
        }
        
        // Базовый случай: достигли вершины пирамиды
        if (current.length() == 1) {
            memo.put(current, true);
            return true;
        }
        
        // Генерируем все возможные следующие уровни
        List<String> nextLevels = new ArrayList<>();
        generateNextLevels(current, new StringBuilder(), 0, allowedMap, nextLevels);
        
        // Если не удалось сгенерировать следующий уровень
        if (nextLevels.isEmpty()) {
            memo.put(current, false);
            return false;
        }
        
        // Проверяем каждый возможный следующий уровень
        for (String next : nextLevels) {
            if (dfs(next, allowedMap, memo)) {
                memo.put(current, true);
                return true;
            }
        }
        
        memo.put(current, false);
        return false;
    }
    
    /**
     * Генерирует все возможные следующие уровни пирамиды.
     */
    private void generateNextLevels(String current, StringBuilder next, int idx,
                                   Map<String, List<Character>> allowedMap,
                                   List<String> result) {
        // Если следующий уровень полностью построен
        if (next.length() == current.length() - 1) {
            result.add(next.toString());
            return;
        }
        
        // Текущая пара символов
        String pair = current.substring(idx, idx + 2);
        
        // Если для этой пары нет разрешенных вершин - прерываем генерацию
        List<Character> tops = allowedMap.get(pair);
        if (tops == null) {
            return;
        }
        
        // Перебираем все возможные вершины для текущей пары
        for (char top : tops) {
            next.append(top);
            generateNextLevels(current, next, idx + 1, allowedMap, result);
            next.deleteCharAt(next.length() - 1); // Откат
        }
    }
}