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

class FooBar {
    constructor(n) {
        this.n = n;
        // Изначально разрешаем выполнение foo
        this.fooPromise = Promise.resolve();
        // bar будет ждать, пока его не разрешат из foo
        this.barPromise = new Promise(resolve => {
            this.barResolve = resolve;
        });
    }

    async foo(printFoo) {
        for (let i = 0; i < this.n; i++) {
            await this.fooPromise;          // ждём, пока можно печатать foo
            printFoo();                      // выводим "foo"
            // Создаём новый промис для следующего foo
            this.fooPromise = new Promise(resolve => {
                this.fooResolve = resolve;
            });
            // Разрешаем bar, чтобы он мог печатать
            if (this.barResolve) {
                this.barResolve();
                this.barResolve = null;
            }
        }
    }

    async bar(printBar) {
        for (let i = 0; i < this.n; i++) {
            await this.barPromise;           // ждём, пока можно печатать bar
            printBar();                      // выводим "bar"
            // Создаём новый промис для следующего bar
            this.barPromise = new Promise(resolve => {
                this.barResolve = resolve;
            });
            // Разрешаем foo для следующей итерации
            if (this.fooResolve) {
                this.fooResolve();
                this.fooResolve = null;
            }
        }
    }
}