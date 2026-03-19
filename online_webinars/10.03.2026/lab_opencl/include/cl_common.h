/**
 * @file cl_common.h
 * @brief Общие утилиты и функции для работы с OpenCL
 * 
 * Этот заголовочный файл содержит:
 * - Макросы для обработки ошибок
 * - Структуры для управления контекстом OpenCL
 * - Вспомогательные функции для работы с устройствами
 * - Утилиты для загрузки kernel'ов
 */

#ifndef CL_COMMON_H
#define CL_COMMON_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

// Определение версии OpenCL перед включением заголовков
#ifndef CL_TARGET_OPENCL_VERSION
#define CL_TARGET_OPENCL_VERSION 300
#endif

#ifdef __APPLE__
#include <OpenCL/opencl.h>
#else
#include <CL/cl.h>
#endif

// ============================================================
// МАКРОСЫ ДЛЯ ОБРАБОТКИ ОШИБОК
// ============================================================

/**
 * @brief Макрос для безопасного освобождения памяти
 */
#define SAFE_FREE(ptr) do { if (ptr) { free(ptr); ptr = NULL; } } while(0)

/**
 * @brief Макрос для проверки ошибок OpenCL с возвратом значения
 * @param err Код ошибки
 * @param msg Сообщение об ошибке
 * @param ret Значение для возврата при ошибке
 */
#define CHECK_CL_ERROR_RET(err, msg, ret) \
    do { \
        if (err != CL_SUCCESS) { \
            fprintf(stderr, "OpenCL Error %d: %s\n", err, msg); \
            return ret; \
        } \
    } while(0)

/**
 * @brief Макрос для проверки ошибок OpenCL с выходом из программы
 * @param err Код ошибки
 * @param msg Сообщение об ошибке
 */
#define CHECK_CL_ERROR_EXIT(err, msg) \
    do { \
        if (err != CL_SUCCESS) { \
            fprintf(stderr, "OpenCL Error %d: %s\n", err, msg); \
            exit(1); \
        } \
    } while(0)

/**
 * @brief Макрос для проверки выделения памяти
 * @param ptr Указатель на выделенную память
 * @param size Запрошенный размер в байтах
 * @param ret Значение для возврата при неудаче
 */
#define CHECK_ALLOC_RET(ptr, size, ret) \
    do { \
        if (ptr == NULL) { \
            fprintf(stderr, "Ошибка: Не удалось выделить память (%zu байт)\n", size); \
            return ret; \
        } \
    } while(0)

// ============================================================
// КОНСТАНТЫ
// ============================================================

#define CL_MAX_PLATFORMS 16
#define CL_MAX_DEVICES 16
#define CL_MAX_SOURCE_SIZE 0x100000
#define CL_MAX_BUILD_LOG_SIZE 0x10000

// ============================================================
// СТРУКТУРЫ ДАННЫХ
// ============================================================

/**
 * @brief Контекст OpenCL для управления ресурсами
 */
typedef struct {
    cl_platform_id platform;           /**< Платформа OpenCL */
    cl_device_id device;               /**< Устройство (GPU/CPU) */
    cl_context context;                /**< Контекст */
    cl_command_queue queue;            /**< Очередь команд */
    cl_program program;                /**< Программа */
    cl_kernel kernel_sha256;           /**< Kernel для SHA-256 */
    cl_kernel kernel_djb2;             /**< Kernel для DJB2 */
    cl_kernel kernel_fnv1a;            /**< Kernel для FNV-1a */
    int is_initialized;                /**< Флаг инициализации */
} OpenCLContext;

/**
 * @brief Информация об устройстве
 */
typedef struct {
    char name[128];                    /**< Название устройства */
    char vendor[128];                  /**< Производитель */
    char version[128];                 /**< Версия OpenCL */
    cl_device_type type;               /**< Тип устройства */
    cl_uint compute_units;             /**< Количество вычислительных блоков */
    size_t max_work_group_size;        /**< Максимальный размер work-group */
    cl_ulong global_mem_size;          /**< Размер глобальной памяти */
    cl_ulong local_mem_size;           /**< Размер локальной памяти */
} DeviceInfo;

/**
 * @brief Результаты бенчмарка
 */
typedef struct {
    const char* name;                  /**< Название теста */
    double cpu_time_ms;                /**< Время CPU (мс) */
    double gpu_time_ms;                /**< Время GPU kernel (мс) */
    double gpu_total_time_ms;          /**< Общее время GPU с overhead (мс) */
    double speedup;                    /**< Ускорение (CPU/GPU) */
    size_t memory_used;                /**< Использовано памяти (байт) */
    int correct;                       /**< Флаг корректности результата */
} BenchmarkResult;

// ============================================================
// ФУНКЦИИ ОБРАБОТКИ ОШИБОК
// ============================================================

/**
 * @brief Получение текстового описания ошибки OpenCL
 * @param err Код ошибки
 * @return Строковое описание ошибки
 */
const char* cl_get_error_string(cl_int err);

// ============================================================
// ФУНКЦИИ УПРАВЛЕНИЯ КОНТЕКСТОМ
// ============================================================

/**
 * @brief Инициализация OpenCL контекста
 * @param ctx Указатель на структуру контекста
 * @param device_type Предпочтительный тип устройства (CL_DEVICE_TYPE_GPU или CL_DEVICE_TYPE_CPU)
 * @param print_info Выводить ли информацию об устройстве
 * @return 0 при успехе, -1 при ошибке
 */
int cl_context_init(OpenCLContext* ctx, cl_device_type device_type, int print_info);

/**
 * @brief Освобождение ресурсов OpenCL контекста
 * @param ctx Указатель на структуру контекста
 */
void cl_context_cleanup(OpenCLContext* ctx);

/**
 * @brief Компиляция OpenCL программы из файла
 * @param ctx Контекст OpenCL
 * @param kernel_filename Имя файла с kernel'ом
 * @param build_options Опции компиляции (может быть NULL)
 * @return 0 при успехе, -1 при ошибке
 */
int cl_compile_kernel_from_file(OpenCLContext* ctx, const char* kernel_filename, 
                                 const char* build_options);

/**
 * @brief Компиляция OpenCL программы из строки
 * @param ctx Контекст OpenCL
 * @param kernel_source Исходный код kernel'а
 * @param build_options Опции компиляции (может быть NULL)
 * @return 0 при успехе, -1 при ошибке
 */
int cl_compile_kernel_from_source(OpenCLContext* ctx, const char* kernel_source,
                                   const char* build_options);

/**
 * @brief Создание kernel'а из программы
 * @param ctx Контекст OpenCL
 * @param kernel_name Имя kernel'а
 * @return Созданный kernel или NULL при ошибке
 */
cl_kernel cl_create_kernel(OpenCLContext* ctx, const char* kernel_name);

// ============================================================
// ФУНКЦИИ ИНФОРМАЦИИ ОБ УСТРОЙСТВЕ
// ============================================================

/**
 * @brief Получение информации об устройстве
 * @param device Устройство OpenCL
 * @param info Указатель на структуру для заполнения
 * @return 0 при успехе, -1 при ошибке
 */
int cl_get_device_info(cl_device_id device, DeviceInfo* info);

/**
 * @brief Вывод информации об устройстве в stdout
 * @param device Устройство OpenCL
 */
void cl_print_device_info(cl_device_id device);

/**
 * @brief Вывод информации о всех доступных платформах и устройствах
 */
void cl_print_platforms_info(void);

/**
 * @brief Автоопределение оптимального размера work-group
 * @param device Устройство OpenCL
 * @param suggested Рекомендуемое значение (может быть 0)
 * @return Оптимальный размер work-group
 */
size_t cl_auto_detect_local_size(cl_device_id device, size_t suggested);

// ============================================================
// ФУНКЦИИ РАБОТЫ С ФАЙЛАМИ
// ============================================================

/**
 * @brief Чтение исходного кода kernel из файла
 * @param filename Имя файла
 * @param size Указатель на переменную для размера файла
 * @return Указатель на буфер с исходным кодом (освобождается через free) или NULL при ошибке
 */
char* cl_read_kernel_file(const char* filename, size_t* size);

/**
 * @brief Проверка существования файла
 * @param path Путь к файлу
 * @return 1 если файл существует, 0 если нет
 */
int cl_file_exists(const char* path);

// ============================================================
// ФУНКЦИИ БЕНЧМАРКА
// ============================================================

/**
 * @brief Получение времени выполнения kernel в миллисекундах
 * @param event Событие OpenCL с включённым профилированием
 * @return Время выполнения в мс
 */
double cl_get_kernel_time_ms(cl_event event);

/**
 * @brief Форматирование результата бенчмарка в строку
 * @param result Указатель на структуру результата
 * @param buffer Буфер для вывода
 * @param buffer_size Размер буфера
 */
void cl_format_benchmark_result(const BenchmarkResult* result, char* buffer, size_t buffer_size);

// ============================================================
// INLINE ФУНКЦИИ
// ============================================================

/**
 * @brief Проверка корректности инициализации контекста
 */
static inline int cl_context_is_valid(const OpenCLContext* ctx) {
    return ctx && ctx->is_initialized && ctx->context != NULL && ctx->device != NULL;
}

#endif /* CL_COMMON_H */
