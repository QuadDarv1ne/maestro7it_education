#include <exec/static_thread_pool.hpp>
#include <fstream>
#include <iostream>
#include <filesystem>
#include <algorithm>
#include <stdexec/execution.hpp>

namespace ex = stdexec;
namespace fs = std::filesystem;

// 1. Вынесем обработку файла в отдельную функцию для чистоты кода
size_t count_words_in_file(const fs::path& file_path) {
    std::ifstream in(file_path);
    if (!in) {
        throw std::runtime_error("Cannot open file: " + file_path.string());
    }

    return std::distance(
        std::istream_iterator<std::string>(in),
        std::istream_iterator<std::string>()
    );
}

int main() {
    // 2. Конфигурация через константы
    constexpr size_t thread_count = 3;
    const std::vector<fs::path> files_to_process = {
        "file1.txt",
        "file2.txt",
        "file3.txt",
        "file4.txt"  // Добавим ещё один файл для демонстрации
    };

    try {
        // 3. Создаём пул потоков
        exec::static_thread_pool pool{thread_count};
        auto sched = pool.get_scheduler();

        // 4. Фабрика задач с улучшенной обработкой ошибок
        auto make_file_task = [&sched](const fs::path& file_path) {
            return ex::schedule(sched)
                | ex::then([file_path] {
                      auto count = count_words_in_file(file_path);
                      std::cout << "File: " << file_path.filename() 
                                << ", words: " << count << "\n";
                      return count;
                  })
                | ex::upon_error([](std::exception_ptr ep) {
                      try {
                          if (ep) std::rethrow_exception(ep);
                      }
                      catch (const std::exception& e) {
                          std::cerr << "Error: " << e.what() << "\n";
                      }
                      return static_cast<size_t>(0);
                  });
        };

        // 5. Создаём задачи для всех файлов
        std::vector<decltype(make_file_task(files_to_process.front()))> tasks;
        for (const auto& file : files_to_process) {
            tasks.emplace_back(make_file_task(file));
        }

        // 6. Параллельная обработка с динамическим количеством файлов
        auto pipeline = ex::when_all_vector(std::move(tasks))
            | ex::then([](std::vector<size_t>&& results) {
                  const auto total = std::accumulate(
                      results.begin(), 
                      results.end(), 
                      size_t{0}
                  );
                  
                  const auto valid_files = std::count_if(
                      results.begin(), 
                      results.end(), 
                      [](size_t count) { return count > 0; }
                  );
                  
                  std::cout << "\nProcessing complete:\n"
                            << "Total files processed: " << results.size() << "\n"
                            << "Successfully processed: " << valid_files << "\n"
                            << "Failed: " << results.size() - valid_files << "\n"
                            << "Total words count: " << total << "\n";
                  
                  return total;
              });

        // 7. Запуск и обработка результата
        if (auto result = ex::sync_wait(std::move(pipeline))) {
            const auto [total_words] = *result;
            std::cout << "\nFinal result: " << total_words << " words in total\n";
        }

    } catch (const std::exception& e) {
        std::cerr << "Fatal error: " << e.what() << "\n";
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
