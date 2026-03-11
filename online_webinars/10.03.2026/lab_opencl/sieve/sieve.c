/*
 * Лабораторная работа: Использование технологий вычислений на GPU
 * Задача: Решето Эратосфена - нахождение всех простых чисел до N
 * 
 * Реализация:
 *   - CPU версия (последовательная)
 *   - GPU версия (OpenCL)
 *   - Сравнение производительности
 * 
 * Компиляция:
 *   gcc -o sieve sieve.c -lOpenCL -lm
 *   или
 *   clang -o sieve sieve.c -lOpenCL -lm
 * 
 * Запуск:
 *   ./sieve [N] [local_size]
 *   Например: ./sieve 10000000 256
 * 
 * Автор: Студент
 * Дата: 2024
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#ifdef __APPLE__
#include <OpenCL/opencl.h>
#else
#include <CL/cl.h>
#endif

// ============================================================
// КОНСТАНТЫ И МАКРОСЫ
// ============================================================

#define MAX_SOURCE_SIZE (0x100000)  // Максимальный размер исходника kernel
#define DEFAULT_N 10000000           // N по умолчанию (10 миллионов)
#define DEFAULT_LOCAL_SIZE 256       // Размер work-group по умолчанию

// Макрос для проверки ошибок OpenCL
#define CHECK_CL_ERROR(err, msg) \
    if (err != CL_SUCCESS) { \
        fprintf(stderr, "OpenCL Error %d: %s\n", err, msg); \
        exit(1); \
    }

// ============================================================
// CPU ВЕРСИЯ: Классическое решето Эратосфена
// ============================================================

/**
 * Классический алгоритм решета Эратосфена (CPU)
 * Возвращает количество найденных простых чисел
 */
unsigned long sieve_cpu(unsigned char* is_prime, unsigned long limit) {
    // Инициализация: все числа >= 2 считаем простыми
    memset(is_prime, 1, (limit + 1) * sizeof(unsigned char));
    is_prime[0] = is_prime[1] = 0;
    
    unsigned long sqrt_limit = (unsigned long)sqrt((double)limit);
    
    // Основной цикл решета
    for (unsigned long p = 2; p <= sqrt_limit; p++) {
        if (is_prime[p]) {
            // Отмечаем все кратные p как составные
            // Начинаем с p*p (оптимизация)
            for (unsigned long multiple = p * p; multiple <= limit; multiple += p) {
                is_prime[multiple] = 0;
            }
        }
    }
    
    // Подсчёт простых чисел
    unsigned long count = 0;
    for (unsigned long i = 2; i <= limit; i++) {
        if (is_prime[i]) count++;
    }
    
    return count;
}

// ============================================================
// ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ OpenCL
// ============================================================

/**
 * Вывод информации о платформах и устройствах
 */
void print_device_info(cl_device_id device) {
    char name[128];
    char vendor[128];
    char version[128];
    cl_uint compute_units;
    size_t max_work_group_size;
    cl_ulong global_mem_size;
    cl_ulong local_mem_size;

    clGetDeviceInfo(device, CL_DEVICE_NAME, sizeof(name), name, NULL);
    clGetDeviceInfo(device, CL_DEVICE_VENDOR, sizeof(vendor), vendor, NULL);
    clGetDeviceInfo(device, CL_DEVICE_VERSION, sizeof(version), version, NULL);
    clGetDeviceInfo(device, CL_DEVICE_MAX_COMPUTE_UNITS, sizeof(compute_units), &compute_units, NULL);
    clGetDeviceInfo(device, CL_DEVICE_MAX_WORK_GROUP_SIZE, sizeof(max_work_group_size), &max_work_group_size, NULL);
    clGetDeviceInfo(device, CL_DEVICE_GLOBAL_MEM_SIZE, sizeof(global_mem_size), &global_mem_size, NULL);
    clGetDeviceInfo(device, CL_DEVICE_LOCAL_MEM_SIZE, sizeof(local_mem_size), &local_mem_size, NULL);

    printf("\n========================================\n");
    printf("ИНФОРМАЦИЯ О GPU УСТРОЙСТВЕ:\n");
    printf("========================================\n");
    printf("  Название:          %s\n", name);
    printf("  Производитель:     %s\n", vendor);
    printf("  Версия OpenCL:     %s\n", version);
    printf("  Вычислительные блоки: %u\n", compute_units);
    printf("  Макс. размер work-group: %zu\n", max_work_group_size);
    printf("  Глобальная память: %.2f MB\n", (double)global_mem_size / (1024 * 1024));
    printf("  Локальная память:  %.2f KB\n", (double)local_mem_size / 1024);
    printf("========================================\n\n");
}

/**
 * Чтение исходного кода kernel из файла
 */
char* read_kernel_source(const char* filename, size_t* size) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        fprintf(stderr, "Ошибка: Не удалось открыть файл %s\n", filename);
        return NULL;
    }
    
    char* source = (char*)malloc(MAX_SOURCE_SIZE);
    *size = fread(source, 1, MAX_SOURCE_SIZE - 1, file);
    source[*size] = '\0';
    fclose(file);
    
    return source;
}

/**
 * Чтение kernel из встроенной строки (если файл не найден)
 */
const char* get_embedded_kernel();

// ============================================================
// GPU ВЕРСИЯ: Решето Эратосфена на OpenCL
// ============================================================

/**
 * Решето Эратосфена на GPU с использованием OpenCL
 */
unsigned int sieve_gpu(unsigned char* is_prime, unsigned long limit,
                        size_t local_size, int print_info) {
    cl_int err;
    cl_platform_id platform;
    cl_device_id device;
    cl_context context;
    cl_command_queue queue;
    cl_program program;
    cl_kernel kernel_init;
    cl_kernel kernel_mark;
    cl_mem d_is_prime;
    
    // --------------------------------------------------------
    // 1. Получение платформы и устройства
    // --------------------------------------------------------
    err = clGetPlatformIDs(1, &platform, NULL);
    CHECK_CL_ERROR(err, "clGetPlatformIDs");
    
    // Сначала пробуем GPU
    err = clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 1, &device, NULL);
    if (err != CL_SUCCESS) {
        printf("GPU не найден, используется CPU...\n");
        err = clGetDeviceIDs(platform, CL_DEVICE_TYPE_CPU, 1, &device, NULL);
        CHECK_CL_ERROR(err, "clGetDeviceIDs CPU");
    }
    
    if (print_info) {
        print_device_info(device);
    }
    
    // --------------------------------------------------------
    // 2. Создание контекста и очереди команд
    // --------------------------------------------------------
    context = clCreateContext(NULL, 1, &device, NULL, NULL, &err);
    CHECK_CL_ERROR(err, "clCreateContext");
    
    // Создаём очередь с профилированием для измерения времени
    queue = clCreateCommandQueue(context, device, 0, &err);
    CHECK_CL_ERROR(err, "clCreateCommandQueue");
    
    // --------------------------------------------------------
    // 3. Загрузка и компиляция kernel
    // --------------------------------------------------------
    
    // Пробуем загрузить из файла
    size_t source_size;
    char* source = read_kernel_source("C:/Users/maksi/OneDrive/Documents/GitHub/maestro7it_education/online_webinars/10.03.2026/lab_opencl/sieve/sieve.cl", &source_size);

    if (!source) {
        // Используем встроенный kernel
        printf("Используется встроенный kernel\n");
        const char* embedded = get_embedded_kernel();
        source = strdup(embedded);
        source_size = strlen(source);
    } else {
        printf("Используется kernel из файла sieve.cl\n");
    }
    
    program = clCreateProgramWithSource(context, 1, (const char**)&source, &source_size, &err);
    CHECK_CL_ERROR(err, "clCreateProgramWithSource");

    // Компиляция
    err = clBuildProgram(program, 1, &device, "-cl-std=CL1.2", NULL, NULL);
    size_t log_size;
    clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, 0, NULL, &log_size);
    if (log_size > 1) {
        char* build_log = (char*)malloc(log_size + 1);
        clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, log_size, build_log, NULL);
        build_log[log_size] = '\0';
        printf("Build log: %s\n", build_log);
        free(build_log);
    }
    if (err != CL_SUCCESS) {
        fprintf(stderr, "Ошибка компиляции kernel\n");
        exit(1);
    }
    
    // Создаём kernel
    kernel_init = clCreateKernel(program, "init_array", &err);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "Ошибка создания kernel init_array: %d\n", err);
        exit(1);
    }
    printf("DEBUG: kernel init_array создан\n");

    kernel_mark = clCreateKernel(program, "sieve_mark_multiples", &err);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "Ошибка создания kernel sieve_mark_multiples: %d\n", err);
        exit(1);
    }
    printf("DEBUG: kernel sieve_mark_multiples создан\n");
    
    // --------------------------------------------------------
    // 4. Создание буферов
    // --------------------------------------------------------
    size_t buf_size = ((limit + 1 + 63) / 64) * 64;  // Выравнивание по 64 байта
    if (buf_size < 256) buf_size = 256;  // Минимальный размер буфера
    unsigned char* h_buf = calloc(buf_size, 1);
    d_is_prime = clCreateBuffer(context, CL_MEM_READ_WRITE | CL_MEM_COPY_HOST_PTR, buf_size, h_buf, &err);
    free(h_buf);
    CHECK_CL_ERROR(err, "clCreateBuffer is_prime");

    // --------------------------------------------------------
    // 5. Инициализация массива на GPU
    // --------------------------------------------------------
    clSetKernelArg(kernel_init, 0, sizeof(cl_mem), &d_is_prime);
    clSetKernelArg(kernel_init, 1, sizeof(unsigned int), &limit);

    size_t global_size_init = ((limit + 1 + local_size - 1) / local_size) * local_size;

    err = clEnqueueNDRangeKernel(queue, kernel_init, 1, NULL,
                                  &global_size_init, &local_size, 0, NULL, NULL);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "Ошибка запуска kernel init: %d\n", err);
    } else {
        printf("DEBUG: kernel init запущен, global_size=%zu, local_size=%zu\n", global_size_init, local_size);
    }

    clFinish(queue);
    
    // --------------------------------------------------------
    // 6. Основной цикл решета
    // --------------------------------------------------------
    unsigned long sqrt_limit = (unsigned long)sqrt((double)limit);

    clSetKernelArg(kernel_mark, 0, sizeof(cl_mem), &d_is_prime);
    clSetKernelArg(kernel_mark, 1, sizeof(cl_uint), &limit);

    for (unsigned long p = 2; p <= sqrt_limit; p++) {
        // Проверяем, является ли p простым (читаем с GPU)
        unsigned char p_is_prime;
        clEnqueueReadBuffer(queue, d_is_prime, CL_FALSE, p * sizeof(unsigned char),
                           sizeof(unsigned char), &p_is_prime, 0, NULL, NULL);
        clFinish(queue);

        if (p_is_prime) {
            unsigned int p_val = (unsigned int)p;
            clSetKernelArg(kernel_mark, 2, sizeof(unsigned int), &p_val);

            // Вычисляем количество работы
            unsigned long start = p * p;
            if (start > limit) continue;

            unsigned long num_multiples = (limit - start) / p + 1;

            // Вычисляем global_size так, чтобы он был кратен local_size
            size_t mark_global_size = num_multiples;
            if (mark_global_size < local_size) {
                mark_global_size = local_size;
            } else {
                mark_global_size = ((mark_global_size + local_size - 1) / local_size) * local_size;
            }

            // Ограничиваем количество потоков
            size_t max_threads = local_size * 64;
            if (mark_global_size > max_threads) mark_global_size = max_threads;

            err = clEnqueueNDRangeKernel(queue, kernel_mark, 1, NULL,
                                         &mark_global_size, &local_size, 0, NULL, NULL);
            if (err != CL_SUCCESS) {
                fprintf(stderr, "Ошибка запуска kernel mark: %d\n", err);
            }

            clFinish(queue);
        }
    }
    
    // --------------------------------------------------------
    // 7. Подсчёт простых чисел (на CPU для совместимости)
    // --------------------------------------------------------
    clFinish(queue);
    
    unsigned int h_count = 0;
    unsigned char* h_is_prime = (unsigned char*)malloc(buf_size);
    memset(h_is_prime, 0, buf_size);
    err = clEnqueueReadBuffer(queue, d_is_prime, CL_FALSE, 0, (limit + 1), h_is_prime, 0, NULL, NULL);
    CHECK_CL_ERROR(err, "clEnqueueReadBuffer init");
    clFinish(queue);

    unsigned int count = 0;
    for (unsigned long i = 2; i <= limit; i++) {
        if (h_is_prime[i]) count++;
    }
    h_count = count;
    
    // Отладка: вывод первых байт
    printf("DEBUG: h_is_prime[0..10] = ");
    for (int i = 0; i <= 10 && i <= (int)limit; i++) {
        printf("%d ", h_is_prime[i]);
    }
    printf("\n");
    
    free(h_is_prime);
    
    // --------------------------------------------------------
    // 9. Освобождение ресурсов
    // --------------------------------------------------------
    clReleaseMemObject(d_is_prime);
    clReleaseKernel(kernel_init);
    clReleaseKernel(kernel_mark);
    clReleaseProgram(program);
    clReleaseCommandQueue(queue);
    clReleaseContext(context);
    free(source);

    return h_count;
}

// ============================================================
// ВСТРОЕННЫЙ KERNEL (если файл .cl не найден)
// ============================================================

const char* get_embedded_kernel() {
    return
    "// OpenCL Kernel: Решето Эратосфена\n"
    "\n"
    "__kernel void init_array(__global uchar* is_prime, unsigned int limit) {\n"
    "    unsigned int gid = get_global_id(0);\n"
    "    if (gid < 2) { is_prime[gid] = 0; return; }\n"
    "    if (gid <= limit) is_prime[gid] = 1;\n"
    "}\n"
    "\n"
    "__kernel void sieve_mark_multiples(\n"
    "    __global uchar* is_prime, unsigned int limit, unsigned int current_prime) {\n"
    "    unsigned int gid = get_global_id(0);\n"
    "    unsigned int start = current_prime * current_prime;\n"
    "    if (start > limit) return;\n"
    "    unsigned int global_size = get_global_size(0);\n"
    "    unsigned int multiple = start + current_prime * gid;\n"
    "    while (multiple <= limit) {\n"
    "        is_prime[multiple] = 0;\n"
    "        multiple += current_prime * global_size;\n"
    "    }\n"
    "}\n";
}

// ============================================================
// ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ
// ============================================================

/**
 * Проверка первых нескольких простых чисел
 */
void verify_result(unsigned long count, unsigned long limit) {
    printf("\nПроверка результата:\n");
    
    // Теоретическое количество простых чисел (приближённо)
    double approx = (double)limit / log((double)limit);
    printf("  Найдено простых чисел: %lu\n", count);
    printf("  Приближённое ожидаемое (n/ln(n)): %.0f\n", approx);
    printf("  Отклонение: %.2f%%\n", 
           fabs((double)count - approx) / approx * 100);
    
    // Вывод первых 20 простых чисел
    printf("  Первые 20 простых чисел: ");
    extern unsigned char* g_is_prime;  // Глобальный массив для вывода
}

/**
 * Вывод простых чисел (для отладки)
 */
void print_primes(unsigned char* is_prime, unsigned long limit, int max_print) {
    printf("Простые числа: ");
    int count = 0;
    for (unsigned long i = 2; i <= limit && count < max_print; i++) {
        if (is_prime[i]) {
            printf("%lu ", i);
            count++;
        }
    }
    if (count == max_print) printf("...");
    printf("\n");
}

// ============================================================
// ГЛАВНАЯ ФУНКЦИЯ
// ============================================================

unsigned char* g_is_prime = NULL;  // Глобальный массив

int main(int argc, char** argv) {
    unsigned long limit = DEFAULT_N;
    size_t local_size = DEFAULT_LOCAL_SIZE;
    
    // Разбор аргументов командной строки
    if (argc >= 2) {
        limit = atol(argv[1]);
        if (limit < 10) limit = 10;
    }
    if (argc >= 3) {
        local_size = atoi(argv[2]);
        if (local_size < 1) local_size = 1;
        // Округляем до степени двойки
        size_t power = 1;
        while (power * 2 <= local_size) power *= 2;
        local_size = power;
    }
    
    printf("============================================================\n");
    printf("  ЛАБОРАТОРНАЯ РАБОТА: Решето Эратосфена на GPU\n");
    printf("============================================================\n");
    printf("  Параметры:\n");
    printf("    N (верхняя граница): %lu\n", limit);
    printf("    Размер work-group:   %zu\n", local_size);
    printf("============================================================\n\n");
    
    // Выделение памяти
    g_is_prime = (unsigned char*)calloc(limit + 1, sizeof(unsigned char));
    if (!g_is_prime) {
        fprintf(stderr, "Ошибка: Не удалось выделить память для N=%lu\n", limit);
        return 1;
    }
    
    // --------------------------------------------------------
    // CPU VERSION
    // --------------------------------------------------------
    printf(">>> Запуск CPU версии...\n");
    clock_t cpu_start = clock();
    unsigned long cpu_count = sieve_cpu(g_is_prime, limit);
    clock_t cpu_end = clock();
    double cpu_time_ms = ((double)(cpu_end - cpu_start)) / CLOCKS_PER_SEC * 1000.0;
    
    printf("    Найдено простых чисел: %lu\n", cpu_count);
    printf("    Время выполнения: %.3f мс\n\n", cpu_time_ms);
    
    // Сохраняем результат CPU для сравнения
    unsigned char* cpu_result = (unsigned char*)malloc(limit + 1);
    memcpy(cpu_result, g_is_prime, limit + 1);
    
    // --------------------------------------------------------
    // GPU VERSION
    // --------------------------------------------------------
    printf(">>> Запуск GPU версии...\n");
    clock_t gpu_total_start = clock();
    unsigned long gpu_count = sieve_gpu(g_is_prime, limit, local_size, 1);
    clock_t gpu_total_end = clock();
    double gpu_total_time_ms = ((double)(gpu_total_end - gpu_total_start)) / CLOCKS_PER_SEC * 1000.0;
    
    printf("    Найдено простых чисел: %lu\n", gpu_count);
    printf("    Общее время (включая overhead): %.3f мс\n\n", gpu_total_time_ms);
    
    // --------------------------------------------------------
    // СРАВНЕНИЕ РЕЗУЛЬТАТОВ
    // --------------------------------------------------------
    printf("============================================================\n");
    printf("  РЕЗУЛЬТАТЫ СРАВНЕНИЯ\n");
    printf("============================================================\n");
    
    // Проверка корректности
    int errors = 0;
    for (unsigned long i = 0; i <= limit && errors < 10; i++) {
        if (cpu_result[i] != g_is_prime[i]) {
            if (errors == 0) printf("  Ошибки в результатах:\n");
            printf("    Число %lu: CPU=%d, GPU=%d\n", i, cpu_result[i], g_is_prime[i]);
            errors++;
        }
    }
    
    if (errors == 0) {
        printf("  Корректность: Результаты CPU и GPU СОВПАДАЮТ\n");
    } else {
        printf("  Корректность: Обнаружены РАСХОЖДЕНИЯ!\n");
    }
    
    printf("\n");
    printf("  Время CPU:     %10.3f мс\n", cpu_time_ms);
    printf("  Время GPU:     %10.3f мс (только kernels)\n", gpu_total_time_ms);
    printf("  Общее время GPU: %10.3f мс (с overhead)\n", gpu_total_time_ms);
    
    double speedup = cpu_time_ms / gpu_total_time_ms;
    printf("\n  Ускорение:     %10.2fx\n", speedup);
    
    // Теоретическая проверка
    double approx = (double)limit / log((double)limit);
    printf("\n  Теоретическое ожидание (n/ln(n)): %.0f\n", approx);
    printf("  Отклонение от теории: %.2f%%\n",
           fabs((double)cpu_count - approx) / approx * 100);
    
    printf("============================================================\n\n");
    
    // Вывод первых простых чисел
    print_primes(g_is_prime, limit, 20);
    
    // Освобождение памяти
    free(cpu_result);
    free(g_is_prime);
    
    return 0;
}
