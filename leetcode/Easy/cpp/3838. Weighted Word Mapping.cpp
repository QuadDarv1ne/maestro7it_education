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

class Solution {
public:
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