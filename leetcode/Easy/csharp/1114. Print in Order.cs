/**
 * https://leetcode.com/problems/print-in-order/description/
 * Автор: Дуплей Максим Игоревич- AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "1114. Print in Order"
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

using System;
using System.Threading;

public class Foo
{
    private readonly ManualResetEventSlim _event1; // сигнал для second
    private readonly ManualResetEventSlim _event2; // сигнал для third

    /**
     * Конструктор. Создаёт события в несигнальном состоянии.
     */
    public Foo()
    {
        _event1 = new ManualResetEventSlim(false);
        _event2 = new ManualResetEventSlim(false);
    }

    /**
     * Первый метод. Печатает "first" и устанавливает событие _event1.
     *
     * @param printFirst делегат для вывода "first"
     */
    public void First(Action printFirst)
    {
        printFirst();
        _event1.Set();
    }

    /**
     * Второй метод. Ожидает сигнала от _event1, печатает "second"
     * и устанавливает _event2.
     *
     * @param printSecond делегат для вывода "second"
     */
    public void Second(Action printSecond)
    {
        _event1.Wait();
        printSecond();
        _event2.Set();
    }

    /**
     * Третий метод. Ожидает сигнала от _event2, печатает "third".
     *
     * @param printThird делегат для вывода "third"
     */
    public void Third(Action printThird)
    {
        _event2.Wait();
        printThird();
    }
}