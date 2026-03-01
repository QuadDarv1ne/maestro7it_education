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

using System.Threading;

public class FooBar {
    private int n;
    private readonly object _lock = new object();
    private bool fooTurn = true;

    public FooBar(int n) {
        this.n = n;
    }

    public void Foo(Action printFoo) {
        for (int i = 0; i < n; i++) {
            lock (_lock) {
                while (!fooTurn) {
                    Monitor.Wait(_lock);
                }
                printFoo();
                fooTurn = false;
                Monitor.Pulse(_lock);
            }
        }
    }

    public void Bar(Action printBar) {
        for (int i = 0; i < n; i++) {
            lock (_lock) {
                while (fooTurn) {
                    Monitor.Wait(_lock);
                }
                printBar();
                fooTurn = true;
                Monitor.Pulse(_lock);
            }
        }
    }
}