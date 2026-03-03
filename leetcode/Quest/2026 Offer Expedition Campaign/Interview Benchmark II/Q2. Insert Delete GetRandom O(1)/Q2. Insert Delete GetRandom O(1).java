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

import java.util.*;

class RandomizedSet {
    private List<Integer> values;
    private Map<Integer, Integer> indexMap;
    private Random random;

    public RandomizedSet() {
        values = new ArrayList<>();
        indexMap = new HashMap<>();
        random = new Random();
    }
    
    public boolean insert(int val) {
        if (indexMap.containsKey(val)) return false;
        indexMap.put(val, values.size());
        values.add(val);
        return true;
    }
    
    public boolean remove(int val) {
        if (!indexMap.containsKey(val)) return false;
        int idx = indexMap.get(val);
        int lastVal = values.get(values.size() - 1);
        values.set(idx, lastVal);
        indexMap.put(lastVal, idx);
        values.remove(values.size() - 1);
        indexMap.remove(val);
        return true;
    }
    
    public int getRandom() {
        return values.get(random.nextInt(values.size()));
    }
}