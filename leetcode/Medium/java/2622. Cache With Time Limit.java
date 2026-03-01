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

import java.util.concurrent.ConcurrentHashMap;

public class TimeLimitedCache {
    private class Entry {
        int value;
        long expirationTime; // абсолютное время истечения (мс)
        Entry(int value, long expirationTime) {
            this.value = value;
            this.expirationTime = expirationTime;
        }
    }

    private ConcurrentHashMap<Integer, Entry> cache;

    public TimeLimitedCache() {
        cache = new ConcurrentHashMap<>();
    }

    /**
     * Сохраняет значение с временем жизни.
     * @return true, если ключ уже существовал и не истёк
     */
    public boolean set(int key, int value, int duration) {
        long now = System.currentTimeMillis();
        long expiration = now + duration;
        Entry old = cache.get(key);
        boolean existed = false;
        if (old != null && old.expirationTime > now) {
            existed = true;
        }
        // Если старая запись истекла, удаляем её (необязательно, но аккуратно)
        if (old != null && old.expirationTime <= now) {
            cache.remove(key);
        }
        cache.put(key, new Entry(value, expiration));
        return existed;
    }

    /**
     * Возвращает значение или -1, если ключ отсутствует или истёк.
     */
    public int get(int key) {
        long now = System.currentTimeMillis();
        Entry entry = cache.get(key);
        if (entry != null && entry.expirationTime > now) {
            return entry.value;
        }
        // Удаляем истекший ключ
        if (entry != null) {
            cache.remove(key);
        }
        return -1;
    }

    /**
     * Возвращает количество неистекших ключей.
     */
    public int count() {
        long now = System.currentTimeMillis();
        // Удаляем истекшие ключи
        cache.entrySet().removeIf(e -> e.getValue().expirationTime <= now);
        return cache.size();
    }
}