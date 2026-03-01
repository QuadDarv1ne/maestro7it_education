/**
 * https://leetcode.com/problems/house-robber-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "2622. Cache With Time Limit"
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

using System;
using System.Collections.Generic;

public class TimeLimitedCache
{
    private class Entry
    {
        public int Value;
        public long ExpirationTime; // абсолютное время истечения (мс)
    }

    private Dictionary<int, Entry> cache = new Dictionary<int, Entry>();

    private long CurrentTimeMillis()
    {
        return DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
    }

    public bool Set(int key, int value, int duration)
    {
        long now = CurrentTimeMillis();
        long expiration = now + duration;
        bool existed = false;
        if (cache.TryGetValue(key, out Entry old))
        {
            if (old.ExpirationTime > now)
                existed = true;
            cache.Remove(key); // удаляем старую запись
        }
        cache[key] = new Entry { Value = value, ExpirationTime = expiration };
        return existed;
    }

    public int Get(int key)
    {
        long now = CurrentTimeMillis();
        if (cache.TryGetValue(key, out Entry entry))
        {
            if (entry.ExpirationTime > now)
                return entry.Value;
            else
                cache.Remove(key);
        }
        return -1;
    }

    public int Count()
    {
        long now = CurrentTimeMillis();
        List<int> expired = new List<int>();
        foreach (var kv in cache)
        {
            if (kv.Value.ExpirationTime <= now)
                expired.Add(kv.Key);
        }
        foreach (int key in expired)
            cache.Remove(key);
        return cache.Count;
    }
}