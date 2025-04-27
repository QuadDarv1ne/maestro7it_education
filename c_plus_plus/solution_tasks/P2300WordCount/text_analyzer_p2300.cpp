// Пример использования пула потоков NVIDIA (P2300 stdexec)
#include <exec/static_thread_pool.hpp> 
#include <fstream>
#include <iostream>
#include <stdexec/execution.hpp>

namespace ex = stdexec;

int main()
{
   // 1. Создаём пул из 3 потоков и получаем планировщик (scheduler)
   exec::static_thread_pool pool{3};
   auto sched = pool.get_scheduler();

   // 2. Фабрика для создания асинхронных задач (sender'ов)
   // Каждая задача будет считать слова в указанном файле
   auto make_count = [&sched](std::string path) {
      return ex::schedule(sched)  // Запускаем задачу в пуле потоков
             // Передаём путь к файлу в следующий шаг
             | ex::then([p = std::move(path)] { return p; })
             | ex::then([](std::string&& p) -> size_t {
                    // Основная логика - чтение файла и подсчёт слов
                    std::ifstream in(p);

                    if (!in)  // Если файл не открылся - бросаем исключение
                        throw std::runtime_error("Не могу открыть: " + p);

                    size_t cnt = 0;
                    std::string word;
                    while (in >> word)
                        ++cnt;
                    
                    std::cout << "Слов в " << p << " = " << cnt << std::endl;
                    return cnt;
                })
             // Обработчик ошибок (если возникло исключение)
             | ex::upon_error([](std::exception_ptr ep) -> size_t {
                    try {
                        if (ep)
                            std::rethrow_exception(ep);
                    }
                    catch (const std::exception& e) {
                        std::cerr << "Ошибка: " << e.what() << std::endl;
                    }
                    return 0;  // При ошибке возвращаем 0
                });
   };

   // 3. Создаём три асинхронные задачи
   auto task1 = make_count("file1.txt");
   auto task2 = make_count("file2.txt");
   auto task3 = make_count("file3.txt");

   // 4. Собираем pipeline:
   // - when_all запускает все задачи параллельно
   // - then объединяет результаты в вектор
   // - then суммирует все элементы вектора
   auto pipeline =
      ex::when_all(std::move(task1), std::move(task2), std::move(task3))
      | ex::then([](size_t a, size_t b, size_t c) {
            return std::vector<size_t>{a, b, c};
        })
      | ex::then([](std::vector<size_t> v) {
            return std::accumulate(v.begin(), v.end(), size_t{0});
        });

   // 5. Запускаем и ждём завершения
   auto result = ex::sync_wait(std::move(pipeline));

   // 6. Выводим общий результат
   if (result) {
      auto [total] = result.value();
      std::cout << "Всего слов: " << total << "\n";
   }
}
