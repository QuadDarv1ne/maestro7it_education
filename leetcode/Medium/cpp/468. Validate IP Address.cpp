/**
 * https://leetcode.com/problems/validate-ip-address/description/
 */

#include <string>
#include <vector>
#include <sstream>
#include <cctype>
using namespace std;

class Solution {
public:
    string validIPAddress(string queryIP) {
        /**
         * Проверяет, является ли строка queryIP допустимым IPv4 или IPv6 адресом.
         *
         * Алгоритм:
         * 1. Если строка содержит точку ('.'), проверяем как IPv4.
         * 2. Если строка содержит двоеточие (':'), проверяем как IPv6.
         * 3. Если строка не содержит ни того, ни другого, возвращаем 'Neither'.
         *
         * Время: O(n), где n — длина строки queryIP.
         * Память: O(1).
         */
        // Проверка IPv4
        if (count(queryIP.begin(), queryIP.end(), '.') == 3) {
            vector<string> parts;
            string part;
            stringstream ss(queryIP);
            while (getline(ss, part, '.')) {
                parts.push_back(part);
            }
            if (parts.size() != 4) return "Neither";
            for (auto &p : parts) {
                if (p.empty() || p.size() > 3) return "Neither";
                if (!all_of(p.begin(), p.end(), ::isdigit)) return "Neither";
                int num = stoi(p);
                if (num < 0 || num > 255) return "Neither";
                if (p.size() > 1 && p[0] == '0') return "Neither"; // ведущие нули
            }
            return "IPv4";
        }
        // Проверка IPv6
        else if (count(queryIP.begin(), queryIP.end(), ':') == 7) {
            vector<string> parts;
            string part;
            stringstream ss(queryIP);
            while (getline(ss, part, ':')) {
                parts.push_back(part);
            }
            if (parts.size() != 8) return "Neither";
            for (auto &p : parts) {
                if (p.empty() || p.size() > 4) return "Neither";
                for (char c : p) {
                    if (!isxdigit(c)) return "Neither"; // символ не является шестнадцатеричным
                }
            }
            return "IPv6";
        }
        return "Neither";
    }
};

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/