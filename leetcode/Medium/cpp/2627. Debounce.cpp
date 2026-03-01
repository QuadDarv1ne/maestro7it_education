/**
 * https://leetcode.com/problems/house-robber-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "2627. Debounce"
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

#include <thread>
#include <chrono>
#include <atomic>
#include <functional>
#include <memory>

template <typename Func>
class Debouncer {
public:
    Debouncer(Func&& fn, int delay_ms)
        : fn_(std::forward<Func>(fn)), delay_ms_(delay_ms), stop_flag_(false) {}

    // Оператор вызова — debounced-функция
    void operator()() {
        // Если уже запущен поток ожидания, останавливаем его
        if (thread_.joinable()) {
            stop_flag_ = true;        // сигнал остановки
            thread_.join();           // ждём завершения старого потока
        }
        stop_flag_ = false;
        // Запускаем новый поток, который подождёт delay_ms и выполнит fn_
        thread_ = std::thread([this]() {
            std::this_thread::sleep_for(std::chrono::milliseconds(delay_ms_));
            if (!stop_flag_.load()) {  // если не было нового вызова
                fn_();
            }
        });
    }

    // Деструктор — обязательно дожидаемся завершения потока
    ~Debouncer() {
        if (thread_.joinable()) {
            stop_flag_ = true;
            thread_.join();
        }
    }

private:
    Func fn_;
    int delay_ms_;
    std::thread thread_;
    std::atomic<bool> stop_flag_;
};

// Вспомогательная функция для создания Debouncer с автоматическим выводом типа
template <typename Func>
auto debounce(Func&& fn, int delay_ms) {
    return Debouncer<Func>(std::forward<Func>(fn), delay_ms);
}

/*
Пример использования:

#include <iostream>
#include <chrono>

void log(int x) {
    std::cout << "Вызвана с аргументом: " << x << std::endl;
}

int main() {
    auto debounced_log = debounce([]() { log(42); }, 50);

    // Имитация вызовов с малым интервалом
    debounced_log();
    std::this_thread::sleep_for(std::chrono::milliseconds(30));
    debounced_log();  // этот отменит предыдущий
    std::this_thread::sleep_for(std::chrono::milliseconds(100)); // ждём выполнения

    return 0;
}
*/