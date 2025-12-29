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

#include <unordered_map>
#include <string>
#include <vector>
#include <functional>
#include <memory>

using namespace std;

class Solution {
public:
    bool pyramidTransition(string bottom, vector<string>& allowed) {
        /**
         * Определяет, можно ли построить пирамиду из заданного основания.
         * 
         * @param bottom строка основания пирамиды
         * @param allowed список разрешенных троек вида "XYZ", где XY - основание, Z - вершина
         * @return true если пирамиду можно построить, иначе false
         */
        
        // Создаем хеш-таблицу для быстрого поиска разрешенных вершин
        unordered_map<string, vector<char>> allowedMap;
        for (const string& triple : allowed) {
            string base = triple.substr(0, 2);
            char top = triple[2];
            allowedMap[base].push_back(top);
        }
        
        // Мемоизация с использованием хеш-таблицы
        unordered_map<string, bool> memo;
        
        // Вспомогательная функция для рекурсивного поиска
        function<bool(const string&)> dfs = [&](const string& current) -> bool {
            // Если уже вычисляли для этого уровня - возвращаем результат
            if (memo.find(current) != memo.end()) {
                return memo[current];
            }
            
            // Базовый случай: достигли вершины пирамиды
            if (current.length() == 1) {
                memo[current] = true;
                return true;
            }
            
            // Генерируем все возможные следующие уровни
            vector<string> nextLevels;
            generateNextLevels(current, "", 0, allowedMap, nextLevels);
            
            // Если не удалось сгенерировать следующий уровень
            if (nextLevels.empty()) {
                memo[current] = false;
                return false;
            }
            
            // Проверяем каждый возможный следующий уровень
            for (const string& next : nextLevels) {
                if (dfs(next)) {
                    memo[current] = true;
                    return true;
                }
            }
            
            memo[current] = false;
            return false;
        };
        
        return dfs(bottom);
    }
    
private:
    /**
     * Генерирует все возможные следующие уровни пирамиды.
     */
    void generateNextLevels(const string& current, string next, int idx,
                           const unordered_map<string, vector<char>>& allowedMap,
                           vector<string>& result) {
        // Если следующий уровень полностью построен
        if (next.length() == current.length() - 1) {
            result.push_back(next);
            return;
        }
        
        // Текущая пара символов
        string pair = current.substr(idx, 2);
        
        // Если для этой пары нет разрешенных вершин - прерываем генерацию
        auto it = allowedMap.find(pair);
        if (it == allowedMap.end()) {
            return;
        }
        
        // Перебираем все возможные вершины для текущей пары
        for (char top : it->second) {
            generateNextLevels(current, next + top, idx + 1, allowedMap, result);
        }
    }
};