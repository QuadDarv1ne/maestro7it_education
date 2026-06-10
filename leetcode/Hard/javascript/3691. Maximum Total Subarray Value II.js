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

/**
 * Разреженная таблица (Sparse Table) для O(1) запросов
 * минимума и максимума на отрезке.
 * 
 * Предподсчёт: O(n log n)
 * Запрос: O(1)
 * Память: O(n log n)
 * 
 * Автор: Дуплей Максим Игоревич
 */
class SparseTableRMQ {
    constructor(data) {
        this.n = data.length;
        this.maxLog = Math.floor(Math.log2(this.n)) + 2;
        this.fMax = Array.from({ length: this.n }, () => Array(this.maxLog).fill(0));
        this.fMin = Array.from({ length: this.n }, () => Array(this.maxLog).fill(0));
        this.lg = Array(this.n + 1).fill(0);

        for (let i = 2; i <= this.n; i++)
            this.lg[i] = this.lg[i >> 1] + 1;

        for (let i = 0; i < this.n; i++) {
            this.fMax[i][0] = data[i];
            this.fMin[i][0] = data[i];
        }

        for (let j = 1; j < this.maxLog; j++) {
            const step = 1 << (j - 1);
            for (let i = 0; i <= this.n - (1 << j); i++) {
                this.fMax[i][j] = Math.max(
                    this.fMax[i][j - 1],
                    this.fMax[i + step][j - 1]
                );
                this.fMin[i][j] = Math.min(
                    this.fMin[i][j - 1],
                    this.fMin[i + step][j - 1]
                );
            }
        }
    }

    queryMax(l, r) {
        const k = this.lg[r - l + 1];
        return Math.max(
            this.fMax[l][k],
            this.fMax[r - (1 << k) + 1][k]
        );
    }

    queryMin(l, r) {
        const k = this.lg[r - l + 1];
        return Math.min(
            this.fMin[l][k],
            this.fMin[r - (1 << k) + 1][k]
        );
    }
}

/**
 * Находит максимальную суммарную ценность k подмассивов.
 * 
 * Ценность подмассива = max - min. Для каждого левого края l
 * ценность монотонно возрастает с ростом правого края r.
 * 
 * Алгоритм:
 * 1. Строим ST-таблицу для O(1) запросов min/max
 * 2. Для каждого l помещаем в max-кучу подмассив [l, n-1]
 * 3. k раз извлекаем максимум и добавляем в кучу [l, r-1]
 * 
 * @param {number[]} nums - Массив целых чисел
 * @param {number} k - Количество выбираемых подмассивов
 * @return {number} Максимальная суммарная ценность k подмассивов
 * 
 * Сложность:
 * Время: O(n log n + k log n)
 * Память: O(n log n)
 * 
 * Автор: Дуплей Максим Игоревич
 */
var maxTotalValue = function(nums, k) {
    const n = nums.length;
    const st = new SparseTableRMQ(nums);
    
    // Max-куча: [val, l, r], сортировка по val по убыванию
    const pq = [];
    
    function push(val, l, r) {
        pq.push([val, l, r]);
        pq.sort((a, b) => b[0] - a[0]);
    }
    
    function pop() {
        return pq.shift();
    }
    
    for (let l = 0; l < n; l++) {
        const val = st.queryMax(l, n - 1) - st.queryMin(l, n - 1);
        push(val, l, n - 1);
    }
    
    let ans = 0;
    for (let i = 0; i < k; i++) {
        const [val, l, r] = pop();
        ans += val;
        if (r > l) {
            const nextVal = st.queryMax(l, r - 1) - st.queryMin(l, r - 1);
            push(nextVal, l, r - 1);
        }
    }
    
    return ans;
};