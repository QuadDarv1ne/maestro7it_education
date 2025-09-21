/**
 * https://leetcode.com/problems/design-movie-rental-system/
 */

/**
 * Класс MovieRentingSystem — имитация системы аренды фильмов.
 * 
 * Особенности:
 * - Поддерживает поиск доступных фильмов с сортировкой по цене и магазину.
 * - Можно арендовать фильм, возвращать его (drop), получать отчёт о 5 самых дешёвых арендованных фильмах.
 * - Оптимизация: используются кучи (MinHeap) и ленивое удаление через Set для быстрого поиска и аренды.
 * 
 * Методы:
 * - search(movie): возвращает до 5 магазинов с фильмом по цене и id магазина.
 * - rent(shop, movie): арендовать фильм в магазине.
 * - drop(shop, movie): вернуть арендованный фильм.
 * - report(): возвращает до 5 самых дешёвых арендованных фильмов.
 */

/**
 * @param {number} n — количество магазинов
 * @param {number[][]} entries — список [shop, movie, price]
 */
var MovieRentingSystem = function(n, entries) {
    // Внутренний класс MinHeap для реализации приоритетной очереди
    class MinHeap {
        constructor(compare) {
            this.data = [];
            this.compare = compare;
        }
        size() { return this.data.length; }
        peek() { return this.data[0]; }
        push(x) {
            this.data.push(x);
            this._siftUp(this.data.length - 1);
        }
        pop() {
            if (this.size() === 0) return null;
            const top = this.data[0];
            const last = this.data.pop();
            if (this.size() > 0) {
                this.data[0] = last;
                this._siftDown(0);
            }
            return top;
        }
        _siftUp(i) {
            while (i > 0) {
                let p = Math.floor((i - 1) / 2);
                if (this.compare(this.data[i], this.data[p]) < 0) {
                    [this.data[i], this.data[p]] = [this.data[p], this.data[i]];
                    i = p;
                } else break;
            }
        }
        _siftDown(i) {
            let n = this.size();
            while (true) {
                let l = i * 2 + 1, r = i * 2 + 2, smallest = i;
                if (l < n && this.compare(this.data[l], this.data[smallest]) < 0) smallest = l;
                if (r < n && this.compare(this.data[r], this.data[smallest]) < 0) smallest = r;
                if (smallest !== i) {
                    [this.data[i], this.data[smallest]] = [this.data[smallest], this.data[i]];
                    i = smallest;
                } else break;
            }
        }
    }

    // priceMap: хранит цену фильма в конкретном магазине
    this.priceMap = new Map(); // key = shop*1e5+movie -> price

    // availableHeapByMovie: кучи доступных фильмов для быстрого поиска
    this.availableHeapByMovie = new Map(); // movie -> MinHeap [price, shop, movie]

    // rentedHeap: кучи арендованных фильмов для отчёта
    this.rentedHeap = new MinHeap((a, b) =>
        a[0] - b[0] || a[1] - b[1] || a[2] - b[2]
    );

    // Sets для ленивого удаления: проверяем актуальность данных в кучах
    this.availableSet = new Set(); // "shop,movie"
    this.rentedSet = new Set();

    // Инициализация системы
    for (let [shop, movie, price] of entries) {
        let key = shop * 100000 + movie;
        this.priceMap.set(key, price);

        if (!this.availableHeapByMovie.has(movie)) {
            this.availableHeapByMovie.set(movie, new MinHeap((a, b) =>
                a[0] - b[0] || a[1] - b[1]
            ));
        }
        this.availableHeapByMovie.get(movie).push([price, shop, movie]);
        this.availableSet.add(`${shop},${movie}`);
    }
};

/** 
 * Поиск до 5 магазинов, где доступен фильм, отсортированных по цене и ID магазина.
 * @param {number} movie
 * @return {number[]} — список ID магазинов
 */
MovieRentingSystem.prototype.search = function(movie) {
    let res = [];
    if (!this.availableHeapByMovie.has(movie)) return res;
    let heap = this.availableHeapByMovie.get(movie);
    let tmp = [];
    let seen = new Set(); // чтобы исключить дубликаты в результате

    while (heap.size() && res.length < 5) {
        let [price, shop, m] = heap.pop();
        let key = `${shop},${m}`;
        if (this.availableSet.has(key) && !seen.has(key)) {
            res.push(shop);
            seen.add(key);
        }
        if (this.availableSet.has(key)) tmp.push([price, shop, m]);
    }
    for (let e of tmp) heap.push(e); // возвращаем элементы обратно в кучу
    return res;
};

/** 
 * Аренда фильма в конкретном магазине
 * @param {number} shop 
 * @param {number} movie
 * @return {void}
 */
MovieRentingSystem.prototype.rent = function(shop, movie) {
    let keyNum = shop * 100000 + movie;
    let price = this.priceMap.get(keyNum);
    this.availableSet.delete(`${shop},${movie}`);
    this.rentedSet.add(`${shop},${movie}`);
    this.rentedHeap.push([price, shop, movie]);
};

/** 
 * Возврат арендованного фильма
 * @param {number} shop 
 * @param {number} movie
 * @return {void}
 */
MovieRentingSystem.prototype.drop = function(shop, movie) {
    let keyNum = shop * 100000 + movie;
    let price = this.priceMap.get(keyNum);
    this.rentedSet.delete(`${shop},${movie}`);
    this.availableSet.add(`${shop},${movie}`);
    this.availableHeapByMovie.get(movie).push([price, shop, movie]);
};

/**
 * Получение отчёта: до 5 самых дешёвых арендованных фильмов
 * @return {number[][]} — список [shop, movie]
 */
MovieRentingSystem.prototype.report = function() {
    let res = [];
    let tmp = [];
    let seen = new Set(); // исключаем дубли

    while (this.rentedHeap.size() && res.length < 5) {
        let [price, shop, movie] = this.rentedHeap.pop();
        let key = `${shop},${movie}`;
        if (this.rentedSet.has(key) && !seen.has(key)) {
            res.push([shop, movie]);
            seen.add(key);
        }
        if (this.rentedSet.has(key)) tmp.push([price, shop, movie]);
    }
    for (let e of tmp) this.rentedHeap.push(e); // возвращаем обратно в кучу
    return res;
};

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/