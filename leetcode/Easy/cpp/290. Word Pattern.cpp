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
#include <unordered_map>
#include <sstream>

class Solution {
public:
    bool wordPattern(std::string pattern, std::string s) {
        // Разбиваем строку s на слова
        std::vector<std::string> words;
        std::istringstream iss(s);
        std::string word;
        while (iss >> word) {
            words.push_back(word);
        }

        if (pattern.size() != words.size()) {
            return false;
        }

        std::unordered_map<char, std::string> charToWord;
        std::unordered_map<std::string, char> wordToChar;

        for (size_t i = 0; i < pattern.size(); ++i) {
            char ch = pattern[i];
            const std::string& w = words[i];

            auto itChar = charToWord.find(ch);
            if (itChar != charToWord.end()) {
                // Символ уже сопоставлен — проверяем слово
                if (itChar->second != w) return false;
            } else {
                auto itWord = wordToChar.find(w);
                // Слово уже сопоставлено другому символу?
                if (itWord != wordToChar.end()) return false;
                // Создаём новые пары
                charToWord[ch] = w;
                wordToChar[w] = ch;
            }
        }
        return true;
    }
};