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

#include <unordered_map>
#include <chrono>

class TimeLimitedCache {
private:
    struct Entry {
        int value;
        long long expirationTime; // абсолютное время истечения (мс)
    };
    std::unordered_map<int, Entry> cache;

    long long currentTimeMillis() {
        return std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::steady_clock::now().time_since_epoch()
        ).count();
    }

public:
    TimeLimitedCache() {}

    bool set(int key, int value, int duration) {
        long long now = currentTimeMillis();
        long long expiration = now + duration;
        auto it = cache.find(key);
        bool existed = false;
        if (it != cache.end()) {
            if (it->second.expirationTime > now) {
                existed = true;
            }
            cache.erase(it); // удаляем старую запись
        }
        cache[key] = {value, expiration};
        return existed;
    }

    int get(int key) {
        long long now = currentTimeMillis();
        auto it = cache.find(key);
        if (it != cache.end()) {
            if (it->second.expirationTime > now) {
                return it->second.value;
            } else {
                cache.erase(it);
            }
        }
        return -1;
    }

    int count() {
        long long now = currentTimeMillis();
        for (auto it = cache.begin(); it != cache.end(); ) {
            if (it->second.expirationTime <= now) {
                it = cache.erase(it);
            } else {
                ++it;
            }
        }
        return cache.size();
    }
};