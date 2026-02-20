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

#include <string>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    /**
     * Преобразует специальную двоичную строку в лексикографически наибольшую.
     * 
     * @param s исходная специальная строка (например, "11011000")
     * @return максимально возможная строка после перестановок (например, "11100100")
     */
    string makeLargestSpecial(string s) {
        return dfs(s);
    }
    
private:
    string dfs(const string& s) {
        // Базовый случай: пустая строка
        if (s.empty()) return "";
        
        vector<string> groups;   // Группы текущего уровня
        int balance = 0;          // Баланс единиц и нулей
        int left = 0;             // Начало текущей группы
        
        for (int i = 0; i < s.size(); ++i) {
            balance += (s[i] == '1') ? 1 : -1;
            if (balance == 0) {
                // Обрабатываем внутренность без первого и последнего символа
                string inner = dfs(s.substr(left + 1, i - left - 1));
                groups.push_back("1" + inner + "0");
                left = i + 1;     // Переходим к следующей группе
            }
        }
        
        // Сортируем группы по убыванию (лексикографически)
        sort(groups.begin(), groups.end(), greater<string>());
        
        // Объединяем группы в одну строку
        string result;
        for (const string& g : groups) {
            result += g;
        }
        return result;
    }
};