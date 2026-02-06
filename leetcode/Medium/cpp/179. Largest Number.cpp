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

#include <vector>
#include <string>
#include <algorithm>

using namespace std;

class Solution {
public:
    string largestNumber(vector<int>& nums) {
        // Преобразуем в строки
        vector<string> strNums;
        for (int num : nums) {
            strNums.push_back(to_string(num));
        }
        
        // Сортируем с лямбда-компаратором
        sort(strNums.begin(), strNums.end(), [](const string& a, const string& b) {
            return a + b > b + a;  // Сравниваем конкатенации
        });
        
        // Если самый большой элемент "0", возвращаем "0"
        if (strNums[0] == "0") {
            return "0";
        }
        
        // Собираем результат
        string result;
        for (const string& s : strNums) {
            result += s;
        }
        
        return result;
    }
};