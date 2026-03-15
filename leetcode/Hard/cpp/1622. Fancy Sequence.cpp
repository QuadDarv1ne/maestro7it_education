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

class Fancy {
private:
    vector<long long> seq;          // Хранит "сырые" значения (raw)
    long long mul, add;              // Глобальный множитель и добавка
    const long long MOD = 1e9 + 7;

    // Быстрое возведение в степень по модулю (для обратного элемента)
    long long modPow(long long a, long long b) {
        long long res = 1;
        while (b) {
            if (b & 1) res = res * a % MOD;
            a = a * a % MOD;
            b >>= 1;
        }
        return res;
    }

    // Обратный элемент по модулю (теорема Ферма: a^(MOD-2) ≡ a^(-1) mod MOD)
    long long modInv(long long a) {
        return modPow(a, MOD - 2);
    }

public:
    /**
     * Конструктор. Инициализирует пустую последовательность.
     * Устанавливает начальные значения: mul = 1, add = 0.
     */
    Fancy() : mul(1), add(0) {}

    /**
     * Добавляет число val в конец последовательности.
     * Сохраняет "сырое" значение, скорректированное с учётом текущих mul и add.
     * @param val целое число для добавления
     */
    void append(int val) {
        // Корректируем val: находим raw = (val - add) / mul (mod MOD)
        long long raw = (val - add + MOD) % MOD;
        raw = raw * modInv(mul) % MOD;
        seq.push_back(raw);
    }

    /**
     * Увеличивает все существующие значения в последовательности на inc.
     * Обновляет только глобальную переменную add.
     * @param inc число, на которое увеличиваются все элементы
     */
    void addAll(int inc) {
        add = (add + inc) % MOD;
    }

    /**
     * Умножает все существующие значения в последовательности на m.
     * Обновляет глобальные переменные mul и add.
     * @param m множитель для всех элементов
     */
    void multAll(int m) {
        mul = mul * m % MOD;
        add = add * m % MOD;
    }

    /**
     * Возвращает текущее значение элемента по индексу idx (0-базовый).
     * Вычисляется как seq[idx] * mul + add по модулю MOD.
     * Если индекс вне диапазона, возвращает -1.
     * @param idx индекс запрашиваемого элемента
     * @return значение элемента или -1
     */
    int getIndex(int idx) {
        if (idx >= seq.size()) return -1;
        // Возвращаем seq[idx] * mul + add (mod MOD)
        return (seq[idx] * mul % MOD + add) % MOD;
    }
};