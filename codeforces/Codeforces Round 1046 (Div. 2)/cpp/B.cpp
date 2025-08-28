/**
 * https://codeforces.com/contest/2136/problem/B
 */

/**
 * @brief Решение задачи Codeforces 2136B.
 *
 * Условие:
 * Дана строка s длины n из символов '0' и '1', а также число k.
 * Нужно построить перестановку p из чисел 1..n такую, что:
 *  - для любой подстроки длины k хотя бы одна позиция с s[i] = '0'
 *    имеет значение p[i], строго большее, чем все значения p[j] в позициях,
 *    где s[j] = '1' внутри этого окна.
 *
 * Иначе говоря, ни одна позиция с символом '1' не должна быть максимумом
 * в своём окне длины k.
 *
 * Алгоритм:
 * 1. Проверяем, есть ли в строке подстрока из k подряд идущих '1'.
 *    Если такая есть, ответ "NO" (невозможно построить перестановку).
 * 2. Если нет, то:
 *    - всем позициям с '0' назначаем самые большие числа (n, n-1, ...);
 *    - всем позициям с '1' — оставшиеся меньшие числа.
 *    Тогда в каждом окне длины k найдётся хотя бы один '0' с большим числом,
 *    что гарантирует выполнение условия.
 *
 * Сложность:
 *  - Время: O(n) на один тест.
 *  - Память: O(n).
 *
 * Пример:
 * Вход:
 *  n = 5, k = 3, s = "10101"
 * Выход:
 *  YES
 *  5 2 4 1 3
 */
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    if (!(cin >> t)) return 0;
    while (t--) {
        int n, k;
        string s;
        cin >> n >> k >> s;
        bool bad = false;
        // check any k consecutive '1'
        int cnt = 0;
        for (int i = 0; i < n; ++i) {
            if (s[i] == '1') ++cnt;
            else cnt = 0;
            if (cnt >= k) { bad = true; break; }
        }
        if (bad) {
            cout << "NO\n";
            continue;
        }
        vector<int> p(n, 0);
        int cur = n;
        // assign largest numbers to zeros
        for (int i = 0; i < n; ++i) {
            if (s[i] == '0') {
                p[i] = cur--;
            }
        }
        // assign remaining numbers to ones
        for (int i = 0; i < n; ++i) {
            if (s[i] == '1') {
                p[i] = cur--;
            }
        }
        cout << "YES\n";
        for (int i = 0; i < n; ++i) {
            if (i) cout << ' ';
            cout << p[i];
        }
        cout << '\n';
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