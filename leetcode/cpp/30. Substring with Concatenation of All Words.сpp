/**
 * https://leetcode.com/problems/substring-with-concatenation-of-all-words/
 */

#include <vector>
#include <string>
#include <unordered_map>

using namespace std;

/**
 * Находит все начальные индексы подстрок в строке `s`, которые являются конкатенацией 
 * всех слов из списка `words` в любом порядке. Все слова в `words` имеют одинаковую длину.
 *
 * Алгоритм:
 * 1. Проверяет тривиальные случаи: пустая строка `s` или пустой список `words`.
 * 2. Вычисляет общую длину всех слов (`totalLen`) и длину одного слова (`wordLen`).
 * 3. Если длина строки `s` меньше `totalLen`, возвращает пустой результат.
 * 4. Создает частотный словарь `wordCount` для слов из списка `words`.
 * 5. Для каждого возможного начального смещения (0, 1, ..., wordLen-1):
 *    a. Инициализирует текущий частотный словарь `currCount` и указатель `left`.
 *    b. Перемещает указатель `right` с шагом `wordLen` по строке:
 *       - Извлекает текущее слово.
 *       - Если слово есть в `wordCount`:
 *           * Увеличивает счетчик слова в `currCount`.
 *           * Если частота слова превышает значение в `wordCount`, сдвигает `left` до устранения превышения.
 *           * Если количество слов в окне равно размеру списка `words`, добавляет `left` в результат.
 *       - Если слова нет в `wordCount`, сбрасывает окно (очищает `currCount` и перемещает `left` за текущее слово).
 * 6. Возвращает список найденных индексов.
 *
 * Сложность:
 * - Временная: O(n * wordLen), где n — длина строки `s`.
 * - Пространственная: O(m * wordLen), где m — количество слов в списке `words`.
 *
 * Параметры:
 *   s: Строка, в которой выполняется поиск.
 *   words: Список слов одинаковой длины для конкатенации.
 *
 * Возвращает:
 *   Вектор начальных индексов подстрок, удовлетворяющих условию.
 */

class Solution {
public:
    vector<int> findSubstring(string s, vector<string>& words) {
        vector<int> result;
        if (words.empty() || s.empty()) return result;
        int n = s.size();
        int m = words.size();
        int wordLen = words[0].size();
        int totalLen = m * wordLen;

        if (n < totalLen) return result;

        unordered_map<string, int> wordCount;
        for (string& word : words) {
            wordCount[word]++;
        }

        for (int start = 0; start < wordLen; start++) {
            unordered_map<string, int> currCount;
            int left = start;
            int count = 0;

            for (int right = start; right <= n - wordLen; right += wordLen) {
                string word = s.substr(right, wordLen);

                if (wordCount.find(word) != wordCount.end()) {
                    currCount[word]++;
                    count++;

                    while (currCount[word] > wordCount[word]) {
                        string leftWord = s.substr(left, wordLen);
                        currCount[leftWord]--;
                        count--;
                        left += wordLen;
                    }

                    if (count == m) {
                        result.push_back(left);
                        string leftWord = s.substr(left, wordLen);
                        currCount[leftWord]--;
                        count--;
                        left += wordLen;
                    }
                } else {
                    currCount.clear();
                    count = 0;
                    left = right + wordLen;
                }
            }
        }

        return result;
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