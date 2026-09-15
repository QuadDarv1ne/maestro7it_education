/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDar1ne/
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

using namespace std;

class Solution {
public:
    /**
     * @brief Преобразует список слов в строку символов на основе весов букв.
     * 
     * Алгоритм работает следующим образом:
     * 1. Для каждого слова вычисляется сумма весов всех его букв.
     *    Индекс веса для буквы определяется как (буква - 'a').
     * 2. Вычисляется остаток от деления полученной суммы на 26.
     * 3. Остаток преобразуется в символ по обратному принципу:
     *    0 -> 'z', 1 -> 'y', ..., 25 -> 'a'.
     * 
     * @param words Ссылка на вектор строк (слова для обработки).
     * @param weights Ссылка на вектор целых чисел (веса для букв от 'a' до 'z').
     * @return Строка, составленная из вычисленных символов для каждого слова.
     */
    string mapWordWeights(vector<string>& words, vector<int>& weights) {
        string result = "";
        
        // Проходим по каждому слову
        for (const string& word : words) {
            int sum = 0;
            
            // Вычисляем вес слова
            for (char c : word) {
                // c - 'a' дает индекс от 0 до 25
                sum += weights[c - 'a'];
            }
            
            // Берем остаток от деления на 26
            int rem = sum % 26;
            
            // Отображаем в букву: 0 -> 'z', 1 -> 'y', ..., 25 -> 'a'
            // 'z' имеет код 122. Если rem=0, то 122-0=122 ('z').
            // Если rem=1, то 122-1=121 ('y').
            result += ('z' - rem);
        }
        
        return result;
    }
};