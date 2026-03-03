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

class RandomizedSet {
private:
    vector<int> values;
    unordered_map<int, int> indexMap;
public:
    RandomizedSet() {}
    
    bool insert(int val) {
        if (indexMap.count(val)) return false;
        indexMap[val] = values.size();
        values.push_back(val);
        return true;
    }
    
    bool remove(int val) {
        if (!indexMap.count(val)) return false;
        int idx = indexMap[val];
        int lastVal = values.back();
        values[idx] = lastVal;
        indexMap[lastVal] = idx;
        values.pop_back();
        indexMap.erase(val);
        return true;
    }
    
    int getRandom() {
        return values[rand() % values.size()];
    }
};