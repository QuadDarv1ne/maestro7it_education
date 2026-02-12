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

#include <functional>
#include <mutex>
#include <condition_variable>

class Foo {
private:
    std::mutex mtx;              // мьютекс для защиты состояния
    std::condition_variable cv;  // условная переменная для ожидания
    int step;                    // 1 — ждём first, 2 — ждём second, 3 — ждём third

public:
    /**
     * Конструктор. Устанавливает начальное состояние step = 1.
     */
    Foo() : step(1) {}

    /**
     * Первый метод. Печатает "first", переводит step в 2 и оповещает все ожидающие потоки.
     *
     * @param printFirst функция для вывода "first"
     */
    void first(std::function<void()> printFirst) {
        printFirst();
        {
            std::lock_guard<std::mutex> lock(mtx);
            step = 2;
        }
        cv.notify_all();
    }

    /**
     * Второй метод. Ожидает, пока step не станет равен 2,
     * затем печатает "second", переводит step в 3 и оповещает.
     *
     * @param printSecond функция для вывода "second"
     */
    void second(std::function<void()> printSecond) {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [this]() { return step == 2; });
        printSecond();
        step = 3;
        cv.notify_all();
    }

    /**
     * Третий метод. Ожидает, пока step не станет равен 3,
     * затем печатает "third".
     *
     * @param printThird функция для вывода "third"
     */
    void third(std::function<void()> printThird) {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [this]() { return step == 3; });
        printThird();
    }
};