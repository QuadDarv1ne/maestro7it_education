/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
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

/**
 * @brief Решение задачи "XOR After Range Multiplication Queries II"
 * 
 * @details
 * Метод: декомпозиция на квадратный корень (sqrt decomposition)
 * 
 * @param nums Исходный массив целых чисел
 * @param queries Список запросов в формате [l, r, k, v]
 * @return int Побитовый XOR всех элементов после обработки
 * 
 * @algorithm
 * 1. Порог B = √n разделяет запросы на "малые" и "большие" по k
 * 2. k > B: прямое применение умножения по индексам
 * 3. k ≤ B: группировка по (k, l%k) + разностный массив
 * 4. Мультипликативные обновления через модульную инверсию
 * 
 * @complexity
 * Время: O(q·√n + n·√n)
 * Память: O(n + q)
 * 
 * @author Дуплей М.И.
 * @source https://github.com/QuadDarv1ne/
 */

#include <vector>
#include <unordered_map>
#include <cmath>
using namespace std;

class Solution {
private:
    static const long long MOD = 1e9 + 7;
    
    // Быстрое возведение в степень по модулю
    long long modPow(long long base, long long exp, long long mod) {
        long long result = 1;
        base %= mod;
        while (exp > 0) {
            if (exp & 1) result = (result * base) % mod;
            base = (base * base) % mod;
            exp >>= 1;
        }
        return result;
    }
    
    // Модульная инверсия (теорема Ферма)
    long long modInv(long long a, long long mod) {
        return modPow(a, mod - 2, mod);
    }
    
public:
    int xorAfterQueries(vector<int>& nums, vector<vector<int>>& queries) {
        int n = nums.size();
        if (n == 0) return 0;
        
        int B = static_cast<int>(sqrt(n)) + 1;
        vector<long long> arr(nums.begin(), nums.end());
        
        // Ключ: (k << 20) | mod для хеширования пары
        unordered_map<long long, vector<tuple<int, int, int>>> smallQueries;
        
        for (const auto& q : queries) {
            int l = q[0], r = q[1], k = q[2], v = q[3];
            
            if (k > B) {
                // Прямое применение для больших k
                for (int idx = l; idx <= r; idx += k) {
                    arr[idx] = (arr[idx] * v) % MOD;
                }
            } else {
                // Группировка малых запросов
                int mod = l % k;
                int posL = (l - mod) / k;
                int posR = (r - mod) / k;
                long long key = (static_cast<long long>(k) << 20) | mod;
                smallQueries[key].emplace_back(posL, posR, v);
            }
        }
        
        // Обработка малых запросов
        for (auto& [key, qList] : smallQueries) {
            int k = static_cast<int>(key >> 20);
            int mod = static_cast<int>(key & ((1 << 20) - 1));
            
            int size = (n - mod + k - 1) / k;
            vector<long long> diff(size + 2, 1);
            
            // Мультипликативные обновления
            for (auto& [posL, posR, v] : qList) {
                diff[posL] = (diff[posL] * v) % MOD;
                diff[posR + 1] = (diff[posR + 1] * modInv(v, MOD)) % MOD;
            }
            
            // Применение через префиксное произведение
            long long mult = 1;
            for (int pos = 0; pos < size; ++pos) {
                mult = (mult * diff[pos]) % MOD;
                int idx = mod + pos * k;
                if (idx < n) {
                    arr[idx] = (arr[idx] * mult) % MOD;
                }
            }
        }
        
        // Финальный XOR
        int result = 0;
        for (long long val : arr) {
            result ^= static_cast<int>(val);
        }
        return result;
    }
};