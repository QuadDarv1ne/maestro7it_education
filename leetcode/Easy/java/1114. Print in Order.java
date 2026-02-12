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

import java.util.concurrent.CountDownLatch;

class Foo {
    /**
     * Счётчики для синхронизации порядка выполнения.
     * latch1 открывается после first(), latch2 — после second().
     */
    private final CountDownLatch latch1;
    private final CountDownLatch latch2;

    /**
     * Конструктор. Инициализирует счётчики с начальным значением 1.
     */
    public Foo() {
        latch1 = new CountDownLatch(1);
        latch2 = new CountDownLatch(1);
    }

    /**
     * Первый метод. Выполняет печать и уменьшает счётчик latch1 до 0,
     * разрешая тем самым выполнение метода second().
     *
     * @param printFirst функция, выводящая "first"
     * @throws InterruptedException если поток будет прерван во время ожидания
     */
    public void first(Runnable printFirst) throws InterruptedException {
        printFirst.run();
        latch1.countDown();
    }

    /**
     * Второй метод. Ожидает обнуления latch1, затем печатает "second"
     * и уменьшает latch2, разрешая выполнение third().
     *
     * @param printSecond функция, выводящая "second"
     * @throws InterruptedException если поток будет прерван во время ожидания
     */
    public void second(Runnable printSecond) throws InterruptedException {
        latch1.await();
        printSecond.run();
        latch2.countDown();
    }

    /**
     * Третий метод. Ожидает обнуления latch2, затем печатает "third".
     *
     * @param printThird функция, выводящая "third"
     * @throws InterruptedException если поток будет прерван во время ожидания
     */
    public void third(Runnable printThird) throws InterruptedException {
        latch2.await();
        printThird.run();
    }
}