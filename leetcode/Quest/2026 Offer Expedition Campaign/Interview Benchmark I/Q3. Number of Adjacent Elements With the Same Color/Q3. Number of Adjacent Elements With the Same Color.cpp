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
    vector<int> colorTheArray(int n, vector<vector<int>>& queries) {
        vector<int> colors(n, 0);
        vector<int> result;
        int count = 0;
        
        for (auto& q : queries) {
            int i = q[0], color = q[1];
            int old = colors[i];
            
            if (old != color) {
                // Remove old
                if (i > 0 && colors[i-1] != 0 && colors[i-1] == old) count--;
                if (i < n-1 && colors[i+1] != 0 && colors[i+1] == old) count--;
                
                colors[i] = color;
                
                // Add new
                if (i > 0 && colors[i-1] != 0 && colors[i-1] == color) count++;
                if (i < n-1 && colors[i+1] != 0 && colors[i+1] == color) count++;
            }
            result.push_back(count);
        }
        return result;
    }
};