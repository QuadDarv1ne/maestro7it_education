/**
 * https://leetcode.com/problems/insert-delete-getrandom-o1/description/?envType=study-plan-v2&envId=top-interview-150
 */

using System;
using System.Collections.Generic;

public class RandomizedSet {
    private List<int> list;
    private Dictionary<int, int> map;

    public RandomizedSet() {
        list = new List<int>();
        map = new Dictionary<int, int>();
    }

    public bool Insert(int val) {
        if (map.ContainsKey(val)) return false;
        map[val] = list.Count;
        list.Add(val);
        return true;
    }

    public bool Remove(int val) {
        if (!map.ContainsKey(val)) return false;
        int index = map[val];
        int lastElement = list[list.Count - 1];
        list[index] = lastElement;
        map[lastElement] = index;
        list.RemoveAt(list.Count - 1);
        map.Remove(val);
        return true;
    }

    public int GetRandom() {
        Random rand = new Random();
        int index = rand.Next(list.Count);
        return list[index];
    }
}

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