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
 * Автор: Дуплей Максим Игоревич -//-
 * Дата: 2026
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#ifdef _WIN32
#include <windows.h>
#else
#include <unistd.h>
#include <limits.h>
#endif

// Явно указываем версию OpenCL 3.0 для избежания предупреждения
#define CL_TARGET_OPENCL_VERSION 300

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

// Режимы работы
typedef enum {
    MODE_BOTH,      // CPU + GPU
    MODE_CPU_ONLY,  // Только CPU
    MODE_GPU_ONLY,  // Только GPU
    MODE_AUTO       // Авто-выбор (по умолчанию)
} RunMode;

// Устройство для запуска
typedef enum {
    DEVICE_AUTO,    // Авто-выбор
    DEVICE_GPU,     // GPU
    DEVICE_CPU      // CPU
} DeviceType;

// Макросы для безопасной работы с памятью
#define SAFE_FREE(ptr) do { if (ptr) { free(ptr); ptr = NULL; } } while(0)

// Макрос для проверки ошибок OpenCL
#define CHECK_CL_ERROR(err, msg) \
    if (err != CL_SUCCESS) { \
        fprintf(stderr, "OpenCL Error %d: %s\n", err, msg); \
        return 0; \
    }

// Макрос для проверки выделения памяти
#define CHECK_ALLOC(ptr, size) \
    if (ptr == NULL) { \
        fprintf(stderr, "Ошибка: Не удалось выделить память (%zu байт)\n", size); \
        return 0; \
    }

// Расширенная проверка ошибок с информацией об устройстве
#define CHECK_CL_ERROR_EX(err, msg) \
    if (err != CL_SUCCESS) { \
        fprintf(stderr, "OpenCL Error %d: %s\n", err, msg); \
        fprintf(stderr, "  Platform: %s\n", get_platform_name()); \
        fprintf(stderr, "  Device: %s\n", get_device_name(device)); \
        exit(1); \
    }

// Глобальные переменные для расширенной диагностики
static cl_platform_id g_platform;
static cl_device_id g_device;

static const char* get_cl_error_string(cl_int err) {
    switch (err) {
        case CL_SUCCESS: return "CL_SUCCESS";
        case CL_DEVICE_NOT_FOUND: return "CL_DEVICE_NOT_FOUND";
        case CL_DEVICE_NOT_AVAILABLE: return "CL_DEVICE_NOT_AVAILABLE";
        case CL_COMPILER_NOT_AVAILABLE: return "CL_COMPILER_NOT_AVAILABLE";
        case CL_MEM_OBJECT_ALLOCATION_FAILURE: return "CL_MEM_OBJECT_ALLOCATION_FAILURE";
        case CL_OUT_OF_RESOURCES: return "CL_OUT_OF_RESOURCES";
        case CL_OUT_OF_HOST_MEMORY: return "CL_OUT_OF_HOST_MEMORY";
        case CL_PROFILING_INFO_NOT_AVAILABLE: return "CL_PROFILING_INFO_NOT_AVAILABLE";
        case CL_MEM_COPY_OVERLAP: return "CL_MEM_COPY_OVERLAP";
        case CL_IMAGE_FORMAT_MISMATCH: return "CL_IMAGE_FORMAT_MISMATCH";
        case CL_IMAGE_FORMAT_NOT_SUPPORTED: return "CL_IMAGE_FORMAT_NOT_SUPPORTED";
        case CL_BUILD_PROGRAM_FAILURE: return "CL_BUILD_PROGRAM_FAILURE";
        case CL_MAP_FAILURE: return "CL_MAP_FAILURE";
        case CL_INVALID_VALUE: return "CL_INVALID_VALUE";
        case CL_INVALID_DEVICE_TYPE: return "CL_INVALID_DEVICE_TYPE";
        case CL_INVALID_PLATFORM: return "CL_INVALID_PLATFORM";
        case CL_INVALID_DEVICE: return "CL_INVALID_DEVICE";
        case CL_INVALID_CONTEXT: return "CL_INVALID_CONTEXT";
        case CL_INVALID_QUEUE_PROPERTIES: return "CL_INVALID_QUEUE_PROPERTIES";
        case CL_INVALID_COMMAND_QUEUE: return "CL_INVALID_COMMAND_QUEUE";
        case CL_INVALID_HOST_PTR: return "CL_INVALID_HOST_PTR";
        case CL_INVALID_MEM_OBJECT: return "CL_INVALID_MEM_OBJECT";
        case CL_INVALID_IMAGE_FORMAT_DESCRIPTOR: return "CL_INVALID_IMAGE_FORMAT_DESCRIPTOR";
        case CL_INVALID_IMAGE_SIZE: return "CL_INVALID_IMAGE_SIZE";
        case CL_INVALID_SAMPLER: return "CL_INVALID_SAMPLER";
        case CL_INVALID_BINARY: return "CL_INVALID_BINARY";
        case CL_INVALID_BUILD_OPTIONS: return "CL_INVALID_BUILD_OPTIONS";
        case CL_INVALID_PROGRAM: return "CL_INVALID_PROGRAM";
        case CL_INVALID_PROGRAM_EXECUTABLE: return "CL_INVALID_PROGRAM_EXECUTABLE";
        case CL_INVALID_KERNEL_NAME: return "CL_INVALID_KERNEL_NAME";
        case CL_INVALID_KERNEL: return "CL_INVALID_KERNEL";
        case CL_INVALID_ARG_INDEX: return "CL_INVALID_ARG_INDEX";
        case CL_INVALID_ARG_VALUE: return "CL_INVALID_ARG_VALUE";
        case CL_INVALID_WORK_DIMENSION: return "CL_INVALID_WORK_DIMENSION";
        case CL_INVALID_WORK_GROUP_SIZE: return "CL_INVALID_WORK_GROUP_SIZE";
        case CL_INVALID_WORK_ITEM_SIZE: return "CL_INVALID_WORK_ITEM_SIZE";
        case CL_INVALID_GLOBAL_OFFSET: return "CL_INVALID_GLOBAL_OFFSET";
        case CL_INVALID_EVENT_WAIT_LIST: return "CL_INVALID_EVENT_WAIT_LIST";
        case CL_INVALID_EVENT: return "CL_INVALID_EVENT";
        case CL_INVALID_OPERATION: return "CL_INVALID_OPERATION";
        case CL_INVALID_GL_OBJECT: return "CL_INVALID_GL_OBJECT";
        case CL_INVALID_BUFFER_SIZE: return "CL_INVALID_BUFFER_SIZE";
        case CL_INVALID_MIP_LEVEL: return "CL_INVALID_MIP_LEVEL";
        default: return "Unknown OpenCL error";
    }
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
 * Проверка существования файла
 */
int file_exists(const char* path) {
    FILE* f = fopen(path, "r");
    if (f) {
        fclose(f);
        return 1;
    }
    return 0;
}

/**
 * Получение пути к исполняемому файлу
 */
static int get_exe_path(char* out_path, size_t size) {
#ifdef _WIN32
    DWORD len = GetModuleFileNameA(NULL, out_path, (DWORD)size);
    if (len == 0 || len >= size) return -1;
    return 0;
#else
    ssize_t len = readlink("/proc/self/exe", out_path, size - 1);
    if (len <= 0) return -1;
    out_path[len] = '\0';
    return 0;
#endif
}

/**
 * Получение директории из полного пути
 */
static void get_dir_from_path(const char* full_path, char* out_dir, size_t size) {
#ifdef _WIN32
    char* last_backslash = strrchr(full_path, '\\');
    char* last_slash = strrchr(full_path, '/');
    char* last_sep = (last_backslash > last_slash) ? last_backslash : last_slash;
#else
    char* last_slash = strrchr(full_path, '/');
    char* last_sep = last_slash;
#endif
    
    if (last_sep) {
        size_t dir_len = last_sep - full_path;
        if (dir_len < size) {
            strncpy(out_dir, full_path, dir_len);
            out_dir[dir_len] = '\0';
        } else {
            out_dir[0] = '\0';
        }
    } else {
        out_dir[0] = '\0';
    }
}

/**
 * Поиск kernel файла в нескольких возможных locations
 * Возвращает 1 если найден, 0 если нет
 */
int find_kernel_file(const char* kernel_name, char* out_path, size_t size) {
    char exe_path[512];
    char dir[512];
    char test_path[512];
    
    // Стратегии поиска (в порядке приоритета):
    const char* search_paths[8];
    int search_count = 0;
    
    // 1. Текущий каталог
    search_paths[search_count++] = kernel_name;
    
    // 2. Относительно расположения исполняемого файла
    if (get_exe_path(exe_path, sizeof(exe_path)) == 0) {
        get_dir_from_path(exe_path, dir, sizeof(dir));
        if (dir[0]) {
            snprintf(test_path, sizeof(test_path), "%s/%s", dir, kernel_name);
            search_paths[search_count++] = strdup(test_path);
            // 3. Родительская директория (bin/ -> parent/)
            char* last_sep = strrchr(dir, '/');
#ifdef _WIN32
            char* last_bs = strrchr(dir, '\\');
            if (!last_sep || (last_bs && last_bs > last_sep)) last_sep = last_bs;
#endif
            if (last_sep) {
                size_t parent_len = last_sep - dir;
                if (parent_len < sizeof(dir)) {
                    strncpy(dir, dir, parent_len);
                    dir[parent_len] = '\0';
                    snprintf(test_path, sizeof(test_path), "%s/%s", dir, kernel_name);
                    search_paths[search_count++] = strdup(test_path);
                }
            }
        }
    }
    
    // 4. Рабочая директория (cwd) + kernel_name
    #ifdef _WIN32
        char cwd[MAX_PATH];
        if (GetCurrentDirectoryA(sizeof(cwd), cwd)) {
            snprintf(test_path, sizeof(test_path), "%s\\%s", cwd, kernel_name);
            search_paths[search_count++] = strdup(test_path);
        }
    #else
        char cwd[PATH_MAX];
        if (getcwd(cwd, sizeof(cwd))) {
            snprintf(test_path, sizeof(test_path), "%s/%s", cwd, kernel_name);
            search_paths[search_count++] = strdup(test_path);
        }
    #endif
    
    // Поиск первого существующего файла
    for (int i = 0; i < search_count; i++) {
        if (file_exists(search_paths[i])) {
            snprintf(out_path, size, "%s", search_paths[i]);
            printf("    Найден kernel: %s\n", search_paths[i]);
            // Освобождаем выделенную память
            for (int j = 1; j < search_count; j++) {
                free((void*)search_paths[j]);
            }
            return 1;
        }
    }
    
    // Освобождаем память
    for (int j = 1; j < search_count; j++) {
        free((void*)search_paths[j]);
    }
    
    return 0;
}

/**
 * Чтение исходного кода kernel из файла
 */
char* read_kernel_source(const char* kernel_name, size_t* size) {
    char full_path[512];
    FILE* file = NULL;
    
    // Пробуем найти файл несколькими способами
    if (find_kernel_file(kernel_name, full_path, sizeof(full_path))) {
        file = fopen(full_path, "r");
    }
    
    // Если не найден, пробуем просто по имени (текущий каталог)
    if (!file) {
        file = fopen(kernel_name, "r");
    }

    if (!file) {
        return NULL;
    }

    char* source = (char*)malloc(MAX_SOURCE_SIZE);
    if (!source) {
        fprintf(stderr, "Ошибка: Не удалось выделить память для kernel\n");
        fclose(file);
        return NULL;
    }

    *size = fread(source, 1, MAX_SOURCE_SIZE - 1, file);
    source[*size] = '\0';
    fclose(file);

    return source;
}

/**
 * Чтение kernel из встроенной строки (если файл не найден)
 */
const char* get_embedded_kernel();

/**
 * Автоматическое определение оптимального local_size
 */
size_t auto_detect_local_size(cl_device_id device, size_t suggested) {
    size_t max_work_group;
    clGetDeviceInfo(device, CL_DEVICE_MAX_WORK_GROUP_SIZE, sizeof(max_work_group), &max_work_group, NULL);
    
    // Рекомендуемое значение или max/2
    size_t optimal = (suggested > 0 && suggested <= max_work_group) ? suggested : max_work_group / 2;
    
    // Округляем до степени двойки
    size_t power = 1;
    while (power * 2 <= optimal && power * 2 <= max_work_group) power *= 2;
    
    printf("    Автоопределение local_size: max=%zu, выбрано=%zu\n", max_work_group, power);
    return power;
}

/**
 * Автоматический выбор устройства на основе N
 */
DeviceType auto_select_device(cl_platform_id platform, unsigned long limit) {
    cl_device_id gpu_device, cpu_device;
    cl_int gpu_err, cpu_err;
    
    gpu_err = clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 1, &gpu_device, NULL);
    cpu_err = clGetDeviceIDs(platform, CL_DEVICE_TYPE_CPU, 1, &cpu_device, NULL);
    
    // Если GPU недоступен — используем CPU
    if (gpu_err != CL_SUCCESS) {
        printf("    GPU недоступен, используется CPU\n");
        return DEVICE_CPU;
    }
    
    // Эвристика: для small N CPU быстрее из-за overhead GPU
    // Для больших N GPU значительно быстрее
    if (limit < 100000) {
        // Small N: CPU обычно быстрее
        printf("    N=%lu (<100K): выбран CPU (overhead GPU слишком большой)\n", limit);
        return DEVICE_CPU;
    } else if (limit < 1000000) {
        // Medium N: зависит от GPU, но CPU ещё может конкурировать
        printf("    N=%lu (100K-1M): выбран GPU\n", limit);
        return DEVICE_GPU;
    } else {
        // Large N: GPU значительно быстрее
        printf("    N=%lu (>1M): выбран GPU (значительное ускорение)\n", limit);
        return DEVICE_GPU;
    }
}
    
// ============================================================
// GPU ВЕРСИЯ: Решето Эратосфена на OpenCL
// ============================================================

/**
 * Решето Эратосфена на GPU с использованием OpenCL
 * Возвращает количество простых чисел и записывает время в *gpu_time_ms
 * device_type: DEVICE_GPU, DEVICE_CPU или DEVICE_AUTO
 */
unsigned int sieve_gpu(unsigned char* is_prime, unsigned long limit,
                        size_t local_size, int print_info, double* gpu_time_ms,
                        DeviceType device_type) {
    cl_int err;
    cl_platform_id platform;
    cl_device_id device;
    cl_context context = NULL;
    cl_command_queue queue = NULL;
    cl_program program = NULL;
    cl_kernel kernel_init = NULL;
    cl_kernel kernel_mark = NULL;
    cl_kernel kernel_full = NULL;
    cl_mem d_is_prime = NULL;

    // Для профилирования
    cl_event init_event = NULL;
    cl_event mark_event = NULL;
    cl_event read_event = NULL;
    cl_event event = NULL;
    
    // --------------------------------------------------------
    // 1. Получение платформы и устройства
    // --------------------------------------------------------
    err = clGetPlatformIDs(1, &platform, NULL);
    CHECK_CL_ERROR(err, "clGetPlatformIDs");
    
    // Определяем тип устройства
    cl_device_type dev_type;
    if (device_type == DEVICE_GPU) {
        dev_type = CL_DEVICE_TYPE_GPU;
    } else if (device_type == DEVICE_CPU) {
        dev_type = CL_DEVICE_TYPE_CPU;
    } else {
        // AUTO - выбираем на основе N
        DeviceType auto_device = auto_select_device(platform, limit);
        dev_type = (auto_device == DEVICE_GPU) ? CL_DEVICE_TYPE_GPU : CL_DEVICE_TYPE_CPU;
    }
    
    err = clGetDeviceIDs(platform, dev_type, 1, &device, NULL);
    if (err != CL_SUCCESS) {
        // Fallback: пробуем другое устройство
        if (dev_type == CL_DEVICE_TYPE_GPU) {
            printf("GPU не найден, используется CPU...\n");
            dev_type = CL_DEVICE_TYPE_CPU;
        } else {
            printf("CPU не найден, используется GPU...\n");
            dev_type = CL_DEVICE_TYPE_GPU;
        }
        err = clGetDeviceIDs(platform, dev_type, 1, &device, NULL);
        CHECK_CL_ERROR(err, "clGetDeviceIDs");
    }
    
    // Автоопределение local_size
    if (local_size == 0) {
        local_size = auto_detect_local_size(device, DEFAULT_LOCAL_SIZE);
    }
    
    if (print_info) {
        print_device_info(device);
    }
    
    // --------------------------------------------------------
    // 2. Создание контекста и очереди команд
    // --------------------------------------------------------
    context = clCreateContext(NULL, 1, &device, NULL, NULL, &err);
    CHECK_CL_ERROR(err, "clCreateContext");
    
    // Создаём очередь команд с поддержкой профилирования
    #if defined(CL_VERSION_2_0)
        cl_queue_properties props[] = { CL_QUEUE_PROPERTIES, CL_QUEUE_PROFILING_ENABLE, 0 };
        queue = clCreateCommandQueueWithProperties(context, device, props, &err);
    #else
        queue = clCreateCommandQueue(context, device, CL_QUEUE_PROFILING_ENABLE, &err);
    #endif
    CHECK_CL_ERROR(err, "clCreateCommandQueue");
    
    // --------------------------------------------------------
    // 3. Загрузка и компиляция kernel
    // --------------------------------------------------------

    // Загрузка kernel из файла
    size_t source_size;
    char* source = read_kernel_source("sieve.cl", &source_size);

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
    if (err != CL_SUCCESS) {
        size_t log_size;
        clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, 0, NULL, &log_size);
        char* build_log = (char*)malloc(log_size + 1);
        clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, log_size, build_log, NULL);
        build_log[log_size] = '\0';
        fprintf(stderr, "Ошибка компиляции kernel:\n%s\n", build_log);
        free(build_log);
        exit(1);
    }
    
    // Создаём kernel
    kernel_init = clCreateKernel(program, "init_array", &err);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "Ошибка создания kernel init_array: %d\n", err);
        exit(1);
    }

    kernel_mark = clCreateKernel(program, "sieve_mark_multiples", &err);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "Ошибка создания kernel sieve_mark_multiples: %d\n", err);
        exit(1);
    }
    
    // Пробуем создать объединенный kernel (оптимизация)
    // Пока отключен - дает неправильные результаты из-за проблем синхронизации
    kernel_full = clCreateKernel(program, "sieve_full", &err);
    int use_full_kernel = 0; // (err == CL_SUCCESS);  // Отключено
    
    // --------------------------------------------------------
    // 4. Создание буферов
    // --------------------------------------------------------
    size_t buf_size = ((limit + 1 + 63) / 64) * 64;  // Выравнивание по 64 байта
    if (buf_size < 256) buf_size = 256;
    
    // Используем pinned memory для быстрой передачи данных
    unsigned char* h_buf = NULL;
    
    // Пробуем создать pinned буфер (CL_MEM_ALLOC_HOST_PTR)
    // Это позволяет использовать DMA для быстрого копирования
    cl_mem_flags buffer_flags = CL_MEM_READ_WRITE;
    
    // Выделяем pinned память если возможно
    h_buf = (unsigned char*)clEnqueueMapBuffer(queue, NULL, CL_TRUE, 
                                                CL_MAP_WRITE, 0, buf_size, 
                                                0, NULL, NULL, &err);
    if (err == CL_SUCCESS && h_buf) {
        memset(h_buf, 0, buf_size);
        clEnqueueUnmapMemObject(queue, h_buf, h_buf, 0, NULL, NULL);
        d_is_prime = clCreateBuffer(context, buffer_flags | CL_MEM_ALLOC_HOST_PTR, 
                                    buf_size, NULL, &err);
    } else {
        // Fallback: обычная память
        h_buf = calloc(buf_size, 1);
        d_is_prime = clCreateBuffer(context, buffer_flags, buf_size, h_buf, &err);
    }
    
    if (h_buf && !(buffer_flags & CL_MEM_ALLOC_HOST_PTR)) {
        // Если используем обычную память - копируем при создании
        d_is_prime = clCreateBuffer(context, CL_MEM_READ_WRITE | CL_MEM_COPY_HOST_PTR, 
                                    buf_size, h_buf, &err);
        free(h_buf);
    }
    CHECK_CL_ERROR(err, "clCreateBuffer is_prime");

    // --------------------------------------------------------
    // 5. Выбор стратегии: объединенный kernel или классический
    // --------------------------------------------------------
    // Объединенный kernel эффективен для small N (весь массив в global work)
    // Для больших N используем классический подход с итерациями
    int use_full = use_full_kernel && (limit <= 10000000);  // Лимит для full kernel
    
    if (use_full) {
        printf("    Используется объединенный kernel (sieve_full)\n");
        clSetKernelArg(kernel_full, 0, sizeof(cl_mem), &d_is_prime);
        clSetKernelArg(kernel_full, 1, sizeof(unsigned int), &limit);
        
        size_t global_size_full = ((limit + 1 + local_size - 1) / local_size) * local_size;
        
        err = clEnqueueNDRangeKernel(queue, kernel_full, 1, NULL,
                                      &global_size_full, &local_size, 0, NULL, &init_event);
        CHECK_CL_ERROR(err, "clEnqueueNDRangeKernel sieve_full");
        
        clFinish(queue);
    } else {
        // Классический подход: init + итерации mark
        printf("    Используется классический подход (init + mark)\n");
        
        // 5a. Инициализация массива на GPU
        clSetKernelArg(kernel_init, 0, sizeof(cl_mem), &d_is_prime);
        clSetKernelArg(kernel_init, 1, sizeof(unsigned int), &limit);

        size_t global_size_init = ((limit + 1 + local_size - 1) / local_size) * local_size;

        err = clEnqueueNDRangeKernel(queue, kernel_init, 1, NULL,
                                      &global_size_init, &local_size, 0, NULL, &init_event);
        CHECK_CL_ERROR(err, "clEnqueueNDRangeKernel init");

        clFinish(queue);
        
        // --------------------------------------------------------
        // 6. Основной цикл решета
        // --------------------------------------------------------
        unsigned long sqrt_limit = (unsigned long)sqrt((double)limit);

        clSetKernelArg(kernel_mark, 0, sizeof(cl_mem), &d_is_prime);
        clSetKernelArg(kernel_mark, 1, sizeof(cl_uint), &limit);

        // Буфер для кэширования состояния простых чисел (читаем блоками)
        unsigned char* h_primes = (unsigned char*)calloc(buf_size, 1);
        if (!h_primes) {
            fprintf(stderr, "Ошибка: Не удалось выделить память для кэша простых чисел (%zu байт)\n", buf_size);
            goto cleanup;
        }
        const unsigned long BATCH_SIZE = 32768;
        unsigned long cached_until = 0;

        // Первоначальная загрузка
        size_t first_read = (limit + 1 > BATCH_SIZE) ? BATCH_SIZE : limit + 1;
        clEnqueueReadBuffer(queue, d_is_prime, CL_TRUE, 0, first_read, h_primes, 0, NULL, NULL);
        cached_until = first_read;

        for (unsigned long p = 2; p <= sqrt_limit; p++) {
            // Читаем новый блок если p выходит за кэш
            if (p >= cached_until && cached_until < limit + 1) {
                unsigned long read_size = BATCH_SIZE;
                if (cached_until + read_size > limit + 1) read_size = limit + 1 - cached_until;
                
                clEnqueueReadBuffer(queue, d_is_prime, CL_TRUE,
                                   cached_until,
                                   read_size, h_primes + cached_until,
                                   0, NULL, NULL);
                cached_until += read_size;
            }
            
            unsigned char p_is_prime = h_primes[p];

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
                                             &mark_global_size, &local_size, 0, NULL, &mark_event);
                CHECK_CL_ERROR(err, "clEnqueueNDRangeKernel mark");
            }
        }

        clFinish(queue);
        SAFE_FREE(h_primes);
    }

cleanup:
    // --------------------------------------------------------
    // 8. Точное время выполнения через профилирование
    // --------------------------------------------------------
    clFinish(queue);

    unsigned char* h_is_prime = (unsigned char*)malloc(buf_size);
    if (!h_is_prime) {
        fprintf(stderr, "Ошибка: Не удалось выделить память для чтения результатов (%zu байт)\n", buf_size);
        goto cleanup;
    }
    memset(h_is_prime, 0, buf_size);
    
    err = clEnqueueReadBuffer(queue, d_is_prime, CL_FALSE, 0, (limit + 1), h_is_prime, 0, NULL, &read_event);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "Ошибка чтения результатов: %s\n", get_cl_error_string(err));
        SAFE_FREE(h_is_prime);
        goto cleanup;
    }
    clFinish(queue);

    unsigned int h_count = 0;
    for (unsigned long i = 2; i <= limit; i++) {
        if (h_is_prime[i]) h_count++;
    }

    memcpy(is_prime, h_is_prime, limit + 1);
    SAFE_FREE(h_is_prime);
    
    // --------------------------------------------------------
    // 8. Точное время выполнения через профилирование
    // --------------------------------------------------------
    if (gpu_time_ms) {
        cl_ulong init_start = 0, init_end = 0;
        cl_ulong read_start = 0, read_end = 0;
        
        // Время kernel (init или full)
        clGetEventProfilingInfo(init_event, CL_PROFILING_COMMAND_START, sizeof(init_start), &init_start, NULL);
        clGetEventProfilingInfo(init_event, CL_PROFILING_COMMAND_END, sizeof(init_end), &init_end, NULL);
        
        // Время чтения результата
        clGetEventProfilingInfo(read_event, CL_PROFILING_COMMAND_START, sizeof(read_start), &read_start, NULL);
        clGetEventProfilingInfo(read_event, CL_PROFILING_COMMAND_END, sizeof(read_end), &read_end, NULL);
        
        // Суммарное время kernel в наносекундах -> миллисекунды
        *gpu_time_ms = (double)(init_end - init_start + read_end - read_start) / 1000000.0;
    }
    
    // Освобождаем events
    clReleaseEvent(init_event);
    clReleaseEvent(read_event);
    if (!use_full_kernel) {
        clReleaseEvent(mark_event);
    }
    
    // --------------------------------------------------------
    // 9. Освобождение ресурсов
    // --------------------------------------------------------
    if (event) clReleaseEvent(event);
    if (init_event) clReleaseEvent(init_event);
    if (mark_event) clReleaseEvent(mark_event);
    if (read_event) clReleaseEvent(read_event);
    
    if (d_is_prime) clReleaseMemObject(d_is_prime);
    if (kernel_init) clReleaseKernel(kernel_init);
    if (kernel_mark) clReleaseKernel(kernel_mark);
    if (kernel_full) clReleaseKernel(kernel_full);
    if (program) clReleaseProgram(program);
    if (queue) clReleaseCommandQueue(queue);
    if (context) clReleaseContext(context);
    SAFE_FREE(source);

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

void print_usage(const char* prog) {
    printf("Использование: %s [N] [local_size] [опции]\n", prog);
    printf("\nПозиционные аргументы:\n");
    printf("  N           - верхняя граница (по умолчанию: %d)\n", DEFAULT_N);
    printf("  local_size  - размер work-group (по умолчанию: авто)\n");
    printf("\nОпции:\n");
    printf("  --cpu       - запустить только CPU версию\n");
    printf("  --gpu       - запустить только GPU версию\n");
    printf("  --auto      - авто-выбор устройства (по умолчанию)\n");
    printf("  --no-info   - не выводить информацию об устройстве\n");
    printf("  --json      - вывод в формате JSON\n");
    printf("  --csv       - вывод в формате CSV (для графиков)\n");
    printf("  -h, --help  - показать эту справку\n");
    printf("\nПримеры:\n");
    printf("  %s                    - авто-выбор параметров\n", prog);
    printf("  %s 1000000 128       - N=1e6, work-group=128\n", prog);
    printf("  %s --cpu             - только CPU версия\n", prog);
    printf("  %s --json            - JSON вывод\n", prog);
    printf("  %s --bench 10        - бенчмарк 10 итераций\n", prog);
}

int main(int argc, char** argv) {
    unsigned long limit = DEFAULT_N;
    size_t local_size = 0;  // 0 = автоопределение
    RunMode mode = MODE_AUTO;
    int print_info = 1;
    int json_output = 0;
    int bench_iterations = 1;  // количество итераций для бенчмарка
    
    // Разбор аргументов командной строки
    int pos_arg_count = 0;
    
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-h") == 0 || strcmp(argv[i], "--help") == 0) {
            print_usage(argv[0]);
            return 0;
        }
        else if (strcmp(argv[i], "--cpu") == 0) {
            mode = MODE_CPU_ONLY;
        }
        else if (strcmp(argv[i], "--gpu") == 0) {
            mode = MODE_GPU_ONLY;
        }
        else if (strcmp(argv[i], "--auto") == 0) {
            mode = MODE_AUTO;
        }
        else if (strcmp(argv[i], "--no-info") == 0) {
            print_info = 0;
        }
        else if (strcmp(argv[i], "--json") == 0) {
            json_output = 1;
        }
        else if (strcmp(argv[i], "--csv") == 0) {
            json_output = 2;  // 2 = CSV режим
        }
        else if (argv[i][0] != '-') {
            // Позиционные аргументы: N, local_size
            if (pos_arg_count == 0) {
                limit = atol(argv[i]);
                if (limit < 10) limit = 10;
            } else if (pos_arg_count == 1) {
                local_size = atoi(argv[i]);
                if (local_size < 1) local_size = 0;  // авто
                // Округляем до степени двойки
                size_t power = 1;
                while (power * 2 <= local_size) power *= 2;
                local_size = power;
            }
            pos_arg_count++;
        }
    }
    
    // По умолчанию запускаем оба режима
    if (mode == MODE_AUTO) {
        mode = MODE_BOTH;
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
        fprintf(stderr, "Ошибка: Не удалось выделить память для N=%lu (%lu байт)\n", limit, limit + 1);
        return 1;
    }

    unsigned long cpu_count = 0;
    unsigned long gpu_count = 0;
    double cpu_time_ms = 0;
    double gpu_kernel_time = 0;
    double gpu_total_time_ms = 0;

    // Сохраняем результат CPU для сравнения
    unsigned char* cpu_result = NULL;
    
    // --------------------------------------------------------
    // CPU VERSION
    // --------------------------------------------------------
    if (mode == MODE_BOTH || mode == MODE_CPU_ONLY) {
        printf(">>> Запуск CPU версии...\n");
        clock_t cpu_start = clock();
        cpu_count = sieve_cpu(g_is_prime, limit);
        clock_t cpu_end = clock();
        cpu_time_ms = ((double)(cpu_end - cpu_start)) / CLOCKS_PER_SEC * 1000.0;
        
        printf("    Найдено простых чисел: %lu\n", cpu_count);
        printf("    Время выполнения: %.3f мс\n\n", cpu_time_ms);
        
        if (mode == MODE_CPU_ONLY) {
            print_primes(g_is_prime, limit, 20);
            free(g_is_prime);
            return 0;
        }
        
        // Сохраняем результат CPU для сравнения
        cpu_result = (unsigned char*)malloc(limit + 1);
        if (!cpu_result) {
            fprintf(stderr, "Ошибка: Не удалось выделить память для сохранения CPU результата\n");
            SAFE_FREE(g_is_prime);
            return 1;
        }
        memcpy(cpu_result, g_is_prime, limit + 1);
    }
    
    // --------------------------------------------------------
    // GPU VERSION
    // --------------------------------------------------------
    if (mode == MODE_BOTH || mode == MODE_GPU_ONLY) {
        printf(">>> Запуск GPU версии...\n");
        
        // Определяем device type
        DeviceType dev_type = DEVICE_GPU;
        
        clock_t gpu_total_start = clock();
        gpu_count = sieve_gpu(g_is_prime, limit, local_size, print_info, &gpu_kernel_time, dev_type);
        clock_t gpu_total_end = clock();
        gpu_total_time_ms = ((double)(gpu_total_end - gpu_total_start)) / CLOCKS_PER_SEC * 1000.0;
        
        printf("    Найдено простых чисел: %lu\n", gpu_count);
        printf("    Время GPU (только kernels): %.3f мс\n", gpu_kernel_time);
        printf("    Общее время (с overhead): %.3f мс\n\n", gpu_total_time_ms);
        
        if (mode == MODE_GPU_ONLY) {
            print_primes(g_is_prime, limit, 20);
            free(g_is_prime);
            return 0;
        }
    }
    
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
    printf("  Время GPU:     %10.3f мс (только kernels)\n", gpu_kernel_time);
    printf("  Общее время GPU: %10.3f мс (с overhead)\n", gpu_total_time_ms);
    
    double speedup = gpu_kernel_time > 0 ? cpu_time_ms / gpu_kernel_time : 0;
    printf("\n  Ускорение:     %10.2fx (по времени kernels)\n", speedup);
    
    // Теоретическая проверка
    double approx = (double)limit / log((double)limit);
    printf("\n  Теоретическое ожидание (n/ln(n)): %.0f\n", approx);
    printf("  Отклонение от теории: %.2f%%\n",
           fabs((double)cpu_count - approx) / approx * 100);
    
    printf("============================================================\n\n");
    
    // Вывод первых простых чисел
    if (!json_output) {
        print_primes(g_is_prime, limit, 20);
    }
    
    // CSV вывод (для графиков)
    if (json_output == 2) {
        printf("%lu,%zu,%.3f,%.3f,%.3f,%lu,%.3f,%.3f,%.3f,%s\n",
               limit, local_size,
               cpu_time_ms,
               gpu_kernel_time, gpu_total_time_ms,
               cpu_count, gpu_count,
               gpu_kernel_time > 0 ? cpu_time_ms / gpu_kernel_time : 0,
               (double)cpu_count - (double)limit / log((double)limit),
               (errors == 0) ? "OK" : "ERROR");
        free(cpu_result);
        free(g_is_prime);
        return 0;
    }
    
    // JSON вывод
    if (json_output) {
        printf("{\n");
        printf("  \"limit\": %lu,\n", limit);
        printf("  \"local_size\": %zu,\n", local_size);
        printf("  \"cpu\": {\n");
        printf("    \"count\": %lu,\n", cpu_count);
        printf("    \"time_ms\": %.3f\n", cpu_time_ms);
        printf("  },\n");
        printf("  \"gpu\": {\n");
        printf("    \"count\": %lu,\n", gpu_count);
        printf("    \"kernel_time_ms\": %.3f,\n", gpu_kernel_time);
        printf("    \"total_time_ms\": %.3f\n", gpu_total_time_ms);
        printf("  },\n");
        printf("  \"speedup\": %.2f,\n", gpu_kernel_time > 0 ? cpu_time_ms / gpu_kernel_time : 0);
        printf("  \"correct\": %s\n", (errors == 0) ? "true" : "false");
        printf("}\n");
    }
    
    // Освобождение памяти
    free(cpu_result);
    free(g_is_prime);
    
    return 0;
}
