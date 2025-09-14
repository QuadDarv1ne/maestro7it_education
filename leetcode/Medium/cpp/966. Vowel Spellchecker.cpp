/**
 * https://leetcode.com/problems/vowel-spellchecker/description/?envType=daily-question&envId=2025-09-14
 */

#include <vector>
#include <string>
#include <unordered_set>
#include <unordered_map>
#include <cctype>
#include <algorithm>
using namespace std;

class Solution {
public:
    /**
     * Решение задачи Vowel Spellchecker.
     * 
     * Для каждого запроса из queries ищем слово в wordlist по следующим правилам:
     * 1. Точное совпадение.
     * 2. Совпадение без учета регистра (первое найденное).
     * 3. Совпадение с заменой всех гласных на '*' (первое найденное).
     * 4. Если ничего не найдено, возвращаем пустую строку.
     */
    vector<string> spellchecker(vector<string>& wordlist, vector<string>& queries) {
        // Создаем множество для точных совпадений
        unordered_set<string> exact(wordlist.begin(), wordlist.end());
        // Словарь для регистра-независимого поиска: ключ — слово в нижнем регистре, значение — первое слово из wordlist
        unordered_map<string, string> caseInsensitive;
        // Словарь для поиска с заменой гласных на '*': ключ — строка с замененными гласными, значение — первое слово
        unordered_map<string, string> vowelInsensitive;
        
        for (const string& word : wordlist) {
            string lower = word;
            // Преобразуем в нижний регистр
            transform(lower.begin(), lower.end(), lower.begin(), ::tolower);
            // Если в caseInsensitive еще нет этого ключа, добавляем
            if (caseInsensitive.find(lower) == caseInsensitive.end()) {
                caseInsensitive[lower] = word;
            }
            // Заменяем гласные на * в lower
            for (char& c : lower) {
                if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
                    c = '*';
                }
            }
            string vowelKey = lower;
            if (vowelInsensitive.find(vowelKey) == vowelInsensitive.end()) {
                vowelInsensitive[vowelKey] = word;
            }
        }
        
        vector<string> result;
        for (const string& query : queries) {
            // Проверяем точное совпадение
            if (exact.find(query) != exact.end()) {
                result.push_back(query);
                continue;
            }
            string lowerQuery = query;
            transform(lowerQuery.begin(), lowerQuery.end(), lowerQuery.begin(), ::tolower);
            // Проверяем регистра-независимое совпадение
            if (caseInsensitive.find(lowerQuery) != caseInsensitive.end()) {
                result.push_back(caseInsensitive[lowerQuery]);
                continue;
            }
            // Заменяем гласные на * в lowerQuery
            for (char& c : lowerQuery) {
                if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
                    c = '*';
                }
            }
            string vowelQuery = lowerQuery;
            if (vowelInsensitive.find(vowelQuery) != vowelInsensitive.end()) {
                result.push_back(vowelInsensitive[vowelQuery]);
            } else {
                result.push_back("");
            }
        }
        return result;
    }
};

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