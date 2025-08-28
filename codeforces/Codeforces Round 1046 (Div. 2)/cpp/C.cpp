/**
 * https://codeforces.com/contest/2136/problem/C
 */

#include <bits/stdc++.h>
using namespace std;

/**
 * @brief Решение задачи Codeforces 2136C – Against the Difference.
 *
 * Идея:
 *   - Посчитаем количество вхождений каждого числа (cnt_x).
 *   - Для каждого числа x ответ += min(cnt_x, x).
 *   - Это и будет максимальная длина аккуратной (neat) подпоследовательности.
 *
 * Сложность:
 *   - Время: O(n) на тест
 *   - Память: O(n)
 */

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int> a(n);
        for (int i = 0; i < n; i++) cin >> a[i];

        unordered_map<int, int> freq;
        for (int x : a) freq[x]++;

        long long ans = 0;
        for (auto [x, cnt] : freq) {
            ans += min(cnt, x);
        }

        cout << ans << "\n";
    }
    return 0;
}

/** Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
*/