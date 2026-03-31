/**
 * https://leetcode.com/problems/lexicographically-smallest-generated-string/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "3474. Lexicographically Smallest Generated String" на C++
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
#include <set>
#include <algorithm>

using namespace std;

class Solution {
public:
    string generateString(string str1, string str2) {
        int n = str1.size(), m = str2.size(), L = n + m - 1;
        vector<int> word(L, -1); // -1 = символ не определен
        
        // Шаг 1: Фиксируем символы из T-условий
        for (int i = 0; i < n; ++i) {
            if (str1[i] == 'T') {
                for (int k = 0; k < m; ++k) {
                    int pos = i + k;
                    if (pos >= L) return "";
                    if (word[pos] != -1 && word[pos] != str2[k]) return "";
                    word[pos] = str2[k];
                }
            }
        }
        
        // Лямбда: совпало бы со str2, если заполнить пустые места 'a'?
        auto wouldMatchIfFilledWithA = [&](int i) {
            for (int k = 0; k < m; ++k) {
                int pos = i + k;
                if (pos >= L) return false;
                if (word[pos] == -1) {
                    if (str2[k] != 'a') return false;
                } else {
                    if (word[pos] != str2[k]) return false;
                }
            }
            return true;
        };
        
        // Лямбда: найти самую правую пустую позицию в подстроке
        auto getRightmostUndef = [&](int i) {
            int r = -1;
            for (int k = 0; k < m; ++k) {
                int pos = i + k;
                if (pos < L && word[pos] == -1) r = pos;
            }
            return r;
        };
        
        // Шаг 2: Собираем F-условия, которые нарушатся при заполнении 'a'
        vector<pair<int, int>> violated;
        for (int i = 0; i < n; ++i) {
            if (str1[i] == 'F' && wouldMatchIfFilledWithA(i)) {
                int r = getRightmostUndef(i);
                if (r == -1) return ""; // Нет пустых мест для исправления
                violated.push_back({i, r});
            }
        }
        
        // Сортируем конфликты по самой правой позиции
        sort(violated.begin(), violated.end(), [](const auto& a, const auto& b) {
            return a.second < b.second;
        });
        
        // Шаг 3: Жадно исправляем конфликты (ставим 'b' как можно правее)
        set<int> active;
        for (auto& p : violated) {
            int i = p.first, r = p.second;
            auto it = active.lower_bound(i);
            // Если уже стоящая 'b' не перекрывает текущее F-условие
            if (it == active.end() || *it > i + m - 1) {
                active.insert(r);
                word[r] = 'b';
            }
        }
        
        // Шаг 4: Заполняем оставшиеся неопределенные позиции 'a'
        string result = "";
        for (int pos = 0; pos < L; ++pos) {
            result += (char)(word[pos] == -1 ? 'a' : word[pos]);
        }
        
        return result;
    }
};