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

public class RandomizedSet {
    private List<int> values;
    private Dictionary<int, int> indexMap;
    private Random random;

    public RandomizedSet() {
        values = new List<int>();
        indexMap = new Dictionary<int, int>();
        random = new Random();
    }
    
    public bool Insert(int val) {
        if (indexMap.ContainsKey(val)) return false;
        indexMap[val] = values.Count;
        values.Add(val);
        return true;
    }
    
    public bool Remove(int val) {
        if (!indexMap.ContainsKey(val)) return false;
        int idx = indexMap[val];
        int lastVal = values[values.Count - 1];
        values[idx] = lastVal;
        indexMap[lastVal] = idx;
        values.RemoveAt(values.Count - 1);
        indexMap.Remove(val);
        return true;
    }
    
    public int GetRandom() {
        return values[random.Next(values.Count)];
    }
}