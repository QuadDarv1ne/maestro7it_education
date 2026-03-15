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

public class Fancy {
    private List<long> seq;
    private long mul, add;
    private const long MOD = 1_000_000_007L;

    /**
     * Конструктор. Инициализирует пустую последовательность.
     * Устанавливает начальные значения: mul = 1, add = 0.
     */
    public Fancy() {
        seq = new List<long>();
        mul = 1;
        add = 0;
    }

    // Вспомогательный метод: быстрое возведение в степень по модулю
    private long ModPow(long a, long b) {
        long res = 1;
        while (b > 0) {
            if ((b & 1) == 1) res = res * a % MOD;
            a = a * a % MOD;
            b >>= 1;
        }
        return res;
    }

    // Вспомогательный метод: обратный элемент по модулю (теорема Ферма)
    private long ModInv(long a) {
        return ModPow(a, MOD - 2);
    }

    /**
     * Добавляет число val в конец последовательности.
     * Сохраняет "сырое" значение, скорректированное с учётом текущих mul и add.
     * @param val целое число для добавления
     */
    public void Append(int val) {
        long raw = (val - add + MOD) % MOD;
        raw = raw * ModInv(mul) % MOD;
        seq.Add(raw);
    }

    /**
     * Увеличивает все существующие значения в последовательности на inc.
     * Обновляет только глобальную переменную add.
     * @param inc число, на которое увеличиваются все элементы
     */
    public void AddAll(int inc) {
        add = (add + inc) % MOD;
    }

    /**
     * Умножает все существующие значения в последовательности на m.
     * Обновляет глобальные переменные mul и add.
     * @param m множитель для всех элементов
     */
    public void MultAll(int m) {
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
    public int GetIndex(int idx) {
        if (idx >= seq.Count) return -1;
        return (int)((seq[idx] * mul % MOD + add) % MOD);
    }
}