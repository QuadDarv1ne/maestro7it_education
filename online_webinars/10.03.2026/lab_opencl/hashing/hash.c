/*
 * Лабораторная работа: Использование технологий вычислений на GPU
 * Задача: Параллельное хэширование - вычисление SHA-256 хэшей
 * 
 * Реализация:
 *   - CPU версия (последовательная и многопоточная)
 *   - GPU версия (OpenCL)
 *   - Сравнение производительности
 * 
 * Компиляция:
 *   gcc -o hash hash.c -lOpenCL -lm -lpthread
 *   или
 *   clang -o hash hash.c -lOpenCL -lm -lpthread
 * 
 * Запуск:
 *   ./hash [количество_хэшей] [длина_данных] [local_size]
 *   Например: ./hash 100000 64 256
 * 
 * Автор: Дуплей Максим Игоревич -//-
 * Дата: 2026
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>

#ifdef __APPLE__
#include <OpenCL/opencl.h>
#else
#include <CL/cl.h>
#endif

#ifdef _WIN32
#include <windows.h>
#else
#include <pthread.h>
#endif

/* strdup для систем, где его нет */
#ifndef HAVE_STRDUP
char* strdup(const char* s) {
    if (s == NULL) return NULL;
    size_t len = strlen(s) + 1;
    char* copy = (char*)malloc(len);
    if (copy != NULL) memcpy(copy, s, len);
    return copy;
}
#endif

// ============================================================
// КОНСТАНТЫ И МАКРОСЫ
// ============================================================

#define MAX_SOURCE_SIZE (0x100000)
#define DEFAULT_NUM_HASHES 100000
#define DEFAULT_DATA_LEN 64
#define DEFAULT_LOCAL_SIZE 256

// Максимальные значения для валидации
#define MAX_NUM_HASHES (100 * 1000 * 1000)  // 100 миллионов
#define MAX_DATA_LEN (1024 * 1024)           // 1 MB
#define MAX_LOCAL_SIZE 4096
#define MIN_LOCAL_SIZE 1

/**
 * @brief Расширенная проверка ошибок OpenCL с детальной информацией
 * @param err Код ошибки
 * @param msg Сообщение
 * @param file Имя файла
 * @param line Номер строки
 */
#define CHECK_CL_ERROR_EX(err, msg, file, line) \
    do { \
        if (err != CL_SUCCESS) { \
            fprintf(stderr, "\n[OpenCL Error] %s\n", msg); \
            fprintf(stderr, "  Файл: %s, Строка: %d\n", file, line); \
            fprintf(stderr, "  Код ошибки: %d (%s)\n", err, cl_error_string(err)); \
            fprintf(stderr, "  Платформа: %s\n", get_platform_name()); \
            fprintf(stderr, "  Устройство: %s\n", get_device_name(device)); \
            exit(1); \
        } \
    } while(0)

/**
 * @brief Проверка ошибок с возвратом значения (для функций)
 */
#define CHECK_CL_ERROR_RET(err, msg, ret) \
    do { \
        if (err != CL_SUCCESS) { \
            fprintf(stderr, "[OpenCL Error] %s: %s\n", msg, cl_error_string(err)); \
            return ret; \
        } \
    } while(0)

/**
 * @brief Проверка выделения памяти с детальным сообщением
 */
#define CHECK_ALLOC_EX(ptr, size, file, line) \
    do { \
        if (ptr == NULL) { \
            fprintf(stderr, "\n[Memory Error] Не удалось выделить память\n"); \
            fprintf(stderr, "  Файл: %s, Строка: %d\n", file, line); \
            fprintf(stderr, "  Запрошено байт: %zu\n", size); \
            exit(1); \
        } \
    } while(0)

/**
 * @brief Проверка валидности указателя
 */
#define CHECK_PTR(ptr, msg) \
    do { \
        if (ptr == NULL) { \
            fprintf(stderr, "[Error] NULL pointer: %s\n", msg); \
            return -1; \
        } \
    } while(0)

#define SAFE_FREE(ptr) do { if (ptr) { free(ptr); ptr = NULL; } } while(0)

/**
 * @brief Получение текстового описания ошибки OpenCL
 */
const char* cl_error_string(cl_int err) {
    switch (err) {
        case CL_SUCCESS:                        return "Success";
        case CL_DEVICE_NOT_FOUND:               return "Device not found";
        case CL_DEVICE_NOT_AVAILABLE:           return "Device not available";
        case CL_COMPILER_NOT_AVAILABLE:         return "Compiler not available";
        case CL_MEM_OBJECT_ALLOCATION_FAILURE:  return "Memory allocation failure";
        case CL_OUT_OF_RESOURCES:               return "Out of resources";
        case CL_OUT_OF_HOST_MEMORY:             return "Out of host memory";
        case CL_BUILD_PROGRAM_FAILURE:          return "Build program failure";
        case CL_INVALID_VALUE:                  return "Invalid value";
        case CL_INVALID_DEVICE:                 return "Invalid device";
        case CL_INVALID_CONTEXT:                return "Invalid context";
        case CL_INVALID_COMMAND_QUEUE:          return "Invalid command queue";
        case CL_INVALID_MEM_OBJECT:             return "Invalid memory object";
        case CL_INVALID_PROGRAM:                return "Invalid program";
        case CL_INVALID_KERNEL:                 return "Invalid kernel";
        case CL_INVALID_ARG_INDEX:              return "Invalid argument index";
        case CL_INVALID_ARG_VALUE:              return "Invalid argument value";
        case CL_INVALID_ARG_SIZE:               return "Invalid argument size";
        case CL_INVALID_KERNEL_ARGS:            return "Invalid kernel arguments";
        case CL_INVALID_WORK_DIMENSION:         return "Invalid work dimension";
        case CL_INVALID_WORK_GROUP_SIZE:        return "Invalid work group size";
        case CL_INVALID_WORK_ITEM_SIZE:         return "Invalid work item size";
        case CL_INVALID_GLOBAL_OFFSET:          return "Invalid global offset";
        case CL_INVALID_EVENT_WAIT_LIST:        return "Invalid event wait list";
        case CL_INVALID_EVENT:                  return "Invalid event";
        case CL_INVALID_OPERATION:              return "Invalid operation";
        case CL_INVALID_GL_OBJECT:              return "Invalid GL object";
        case CL_INVALID_BUFFER_SIZE:            return "Invalid buffer size";
        case CL_INVALID_MIP_LEVEL:              return "Invalid MIP level";
        default:                                return "Unknown error";
    }
}

// ============================================================
// SHA-256 КОНСТАНТЫ
// ============================================================

static const uint32_t sha256_h[8] = {
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
};

static const uint32_t sha256_k[64] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
};

// ============================================================
// СТРУКТУРЫ ДЛЯ OPENCL
// ============================================================

/**
 * @brief Контекст OpenCL для управления ресурсами
 */
typedef struct {
    cl_platform_id platform;
    cl_device_id device;
    cl_context context;
    cl_command_queue queue;
    cl_program program;
    cl_kernel kernel_sha256;
    cl_kernel kernel_djb2;
    cl_kernel kernel_fnv1a;
    int is_initialized;
} OpenCLContext;

/**
 * @brief Результаты бенчмарка
 */
typedef struct {
    double cpu_time_ms;
    double gpu_kernel_time_ms;
    double gpu_total_time_ms;
    double speedup;
    uint32_t matches;
    uint32_t total;
} BenchmarkResult;

// ============================================================
// ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
// ============================================================

#define ROTR32(x, n) (((x) >> (n)) | ((x) << (32 - (n))))
#define CH(x, y, z)  (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x, y, z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define EP0(x)       (ROTR32(x, 2) ^ ROTR32(x, 13) ^ ROTR32(x, 22))
#define EP1(x)       (ROTR32(x, 6) ^ ROTR32(x, 11) ^ ROTR32(x, 25))
#define SIG0(x)      (ROTR32(x, 7) ^ ROTR32(x, 18) ^ ((x) >> 3))
#define SIG1(x)      (ROTR32(x, 17) ^ ROTR32(x, 19) ^ ((x) >> 10))

// ============================================================
// CPU ВЕРСИЯ SHA-256
// ============================================================

/**
 * Вычисление SHA-256 хэша для одного сообщения (CPU)
 */
void sha256_cpu(const uint8_t* data, size_t len, uint8_t* hash) {
    uint32_t h[8];
    for (int i = 0; i < 8; i++) h[i] = sha256_h[i];
    
    // Подготовка данных с padding
    size_t total_len = len + 9;  // данные + 0x80 + длина (8 байт)
    size_t padded_len = ((total_len + 63) / 64) * 64;
    
    uint8_t* padded = (uint8_t*)calloc(padded_len, 1);
    memcpy(padded, data, len);
    padded[len] = 0x80;
    
    // Длина в битах (big-endian)
    uint64_t bit_len = len * 8;
    padded[padded_len - 8] = (bit_len >> 56) & 0xFF;
    padded[padded_len - 7] = (bit_len >> 48) & 0xFF;
    padded[padded_len - 6] = (bit_len >> 40) & 0xFF;
    padded[padded_len - 5] = (bit_len >> 32) & 0xFF;
    padded[padded_len - 4] = (bit_len >> 24) & 0xFF;
    padded[padded_len - 3] = (bit_len >> 16) & 0xFF;
    padded[padded_len - 2] = (bit_len >> 8) & 0xFF;
    padded[padded_len - 1] = bit_len & 0xFF;
    
    // Обработка блоков по 64 байта
    for (size_t block = 0; block < padded_len; block += 64) {
        uint32_t w[64];
        
        // Первые 16 слов из блока (big-endian)
        for (int i = 0; i < 16; i++) {
            w[i] = ((uint32_t)padded[block + i*4 + 0] << 24) |
                   ((uint32_t)padded[block + i*4 + 1] << 16) |
                   ((uint32_t)padded[block + i*4 + 2] << 8) |
                   ((uint32_t)padded[block + i*4 + 3]);
        }
        
        // Расширение до 64 слов
        for (int i = 16; i < 64; i++) {
            w[i] = SIG1(w[i-2]) + w[i-7] + SIG0(w[i-15]) + w[i-16];
        }
        
        // Основной цикл
        uint32_t a = h[0], b = h[1], c = h[2], d = h[3];
        uint32_t e = h[4], f = h[5], g = h[6], h_val = h[7];
        
        for (int i = 0; i < 64; i++) {
            uint32_t t1 = h_val + EP1(e) + CH(e, f, g) + sha256_k[i] + w[i];
            uint32_t t2 = EP0(a) + MAJ(a, b, c);
            h_val = g; g = f; f = e; e = d + t1;
            d = c; c = b; b = a; a = t1 + t2;
        }
        
        h[0] += a; h[1] += b; h[2] += c; h[3] += d;
        h[4] += e; h[5] += f; h[6] += g; h[7] += h_val;
    }
    
    free(padded);
    
    // Запись результата
    for (int i = 0; i < 8; i++) {
        hash[i*4 + 0] = (h[i] >> 24) & 0xFF;
        hash[i*4 + 1] = (h[i] >> 16) & 0xFF;
        hash[i*4 + 2] = (h[i] >> 8) & 0xFF;
        hash[i*4 + 3] = h[i] & 0xFF;
    }
}

/**
 * Вычисление хэшей для всех данных (CPU, последовательно)
 */
void hash_all_cpu(const uint8_t* data, const uint32_t* lens, 
                  uint8_t* hashes, uint32_t num_hashes, uint32_t max_len) {
    for (uint32_t i = 0; i < num_hashes; i++) {
        sha256_cpu(data + i * max_len, lens[i], hashes + i * 32);
    }
}

// ============================================================
// DJB2 И FNV-1A ХЭШИ (для сравнения скорости)
// ============================================================

uint32_t djb2_cpu(const uint8_t* data, size_t len) {
    uint32_t hash = 5381;
    for (size_t i = 0; i < len; i++) {
        hash = ((hash << 5) + hash) + data[i];
    }
    return hash;
}

uint32_t fnv1a_cpu(const uint8_t* data, size_t len) {
    uint32_t hash = 2166136261u;
    for (size_t i = 0; i < len; i++) {
        hash ^= data[i];
        hash *= 16777619u;
    }
    return hash;
}

// ============================================================
// ГЕНЕРАЦИЯ ТЕСТОВЫХ ДАННЫХ
// ============================================================

void generate_test_data(uint8_t* data, uint32_t* lens, 
                        uint32_t num_hashes, uint32_t max_len) {
    srand(42);  // Фиксированный seed для воспроизводимости
    
    for (uint32_t i = 0; i < num_hashes; i++) {
        // Случайная длина от 8 до max_len
        lens[i] = 8 + (rand() % (max_len - 7));
        
        // Генерируем данные
        for (uint32_t j = 0; j < lens[i]; j++) {
            data[i * max_len + j] = rand() % 256;
        }
    }
}

// ============================================================
// ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ OpenCL
// ============================================================

/**
 * @brief Получение названия платформы
 */
const char* get_platform_name(void) {
    static char platform_name[128] = {0};
    cl_platform_id platform;
    cl_int err = clGetPlatformIDs(1, &platform, NULL);
    if (err == CL_SUCCESS) {
        clGetPlatformInfo(platform, CL_PLATFORM_NAME, sizeof(platform_name), platform_name, NULL);
    } else {
        snprintf(platform_name, sizeof(platform_name), "Unknown");
    }
    return platform_name;
}

/**
 * @brief Получение названия устройства
 */
const char* get_device_name(cl_device_id device) {
    static char device_name[128] = {0};
    if (device) {
        clGetDeviceInfo(device, CL_DEVICE_NAME, sizeof(device_name), device_name, NULL);
    } else {
        snprintf(device_name, sizeof(device_name), "Unknown");
    }
    return device_name;
}

/**
 * @brief Проверка версии OpenCL
 * @param device Устройство OpenCL
 * @param min_major Минимальная требуемая мажорная версия
 * @param min_minor Минимальная требуемая минорная версия
 * @return 1 если версия подходит, 0 если нет
 */
int check_opencl_version(cl_device_id device, int min_major, int min_minor) {
    char version_str[128];
    cl_int err;
    
    err = clGetDeviceInfo(device, CL_DEVICE_VERSION, sizeof(version_str), version_str, NULL);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "[Error] Не удалось получить версию OpenCL\n");
        return 0;
    }
    
    // Парсинг версии формата "OpenCL X.Y ..."
    int major = 0, minor = 0;
    if (sscanf(version_str, "OpenCL %d.%d", &major, &minor) != 2) {
        fprintf(stderr, "[Warning] Не удалось распарсить версию OpenCL: %s\n", version_str);
        // Предполагаем минимальную совместимость
        return 1;
    }
    
    if (major > min_major || (major == min_major && minor >= min_minor)) {
        return 1;
    }
    
    fprintf(stderr, "[Error] Требуется OpenCL %d.%d или выше, найдено %d.%d\n",
            min_major, min_minor, major, minor);
    return 0;
}

/**
 * @brief Вывод информации об устройстве
 */
void print_device_info(cl_device_id device) {
    char name[128], vendor[128], version[128];
    cl_uint compute_units;
    size_t max_wg_size;
    cl_ulong global_mem, local_mem;

    clGetDeviceInfo(device, CL_DEVICE_NAME, sizeof(name), name, NULL);
    clGetDeviceInfo(device, CL_DEVICE_VENDOR, sizeof(vendor), vendor, NULL);
    clGetDeviceInfo(device, CL_DEVICE_VERSION, sizeof(version), version, NULL);
    clGetDeviceInfo(device, CL_DEVICE_MAX_COMPUTE_UNITS, sizeof(compute_units), &compute_units, NULL);
    clGetDeviceInfo(device, CL_DEVICE_MAX_WORK_GROUP_SIZE, sizeof(max_wg_size), &max_wg_size, NULL);
    clGetDeviceInfo(device, CL_DEVICE_GLOBAL_MEM_SIZE, sizeof(global_mem), &global_mem, NULL);
    clGetDeviceInfo(device, CL_DEVICE_LOCAL_MEM_SIZE, sizeof(local_mem), &local_mem, NULL);

    printf("\n========================================\n");
    printf("ИНФОРМАЦИЯ О GPU УСТРОЙСТВЕ:\n");
    printf("========================================\n");
    printf("  Название:              %s\n", name);
    printf("  Производитель:         %s\n", vendor);
    printf("  Версия OpenCL:         %s\n", version);
    printf("  Вычислительные блоки:  %u\n", compute_units);
    printf("  Макс. work-group:      %zu\n", max_wg_size);
    printf("  Глобальная память:     %.0f MB\n", (double)global_mem / (1024*1024));
    printf("  Локальная память:      %.0f KB\n", (double)local_mem / 1024);
    printf("========================================\n\n");
}

/**
 * @brief Чтение kernel source из файла с обработкой ошибок
 */
char* read_kernel_source(const char* filename, size_t* size) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        fprintf(stderr, "[Warning] Не удалось открыть файл kernel: %s\n", filename);
        return NULL;
    }

    char* source = (char*)malloc(MAX_SOURCE_SIZE);
    if (!source) {
        fprintf(stderr, "[Error] Не удалось выделить память для kernel source (%d байт)\n", MAX_SOURCE_SIZE);
        fclose(file);
        return NULL;
    }

    *size = fread(source, 1, MAX_SOURCE_SIZE - 1, file);
    if (*size == 0) {
        fprintf(stderr, "[Error] Пустой файл kernel: %s\n", filename);
        SAFE_FREE(source);
        fclose(file);
        return NULL;
    }
    
    source[*size] = '\0';
    fclose(file);
    return source;
}

/**
 * @brief Освобождение ресурсов OpenCL
 */
void cl_cleanup(OpenCLContext* ctx) {
    if (!ctx) return;
    
    if (ctx->kernel_sha256) clReleaseKernel(ctx->kernel_sha256);
    if (ctx->kernel_djb2) clReleaseKernel(ctx->kernel_djb2);
    if (ctx->kernel_fnv1a) clReleaseKernel(ctx->kernel_fnv1a);
    if (ctx->program) clReleaseProgram(ctx->program);
    if (ctx->queue) clReleaseCommandQueue(ctx->queue);
    if (ctx->context) clReleaseContext(ctx->context);
    
    memset(ctx, 0, sizeof(OpenCLContext));
}

/**
 * @brief Инициализация OpenCL с автоматическим выбором лучшего устройства
 */
int cl_init(OpenCLContext* ctx, int print_info) {
    cl_int err;
    cl_uint num_platforms, num_devices;
    
    memset(ctx, 0, sizeof(OpenCLContext));
    
    // Получение платформ
    err = clGetPlatformIDs(1, &ctx->platform, &num_platforms);
    if (err != CL_SUCCESS || num_platforms == 0) {
        fprintf(stderr, "Ошибка: Не найдено OpenCL платформ\n");
        return -1;
    }
    
    // Попытка найти GPU
    err = clGetDeviceIDs(ctx->platform, CL_DEVICE_TYPE_GPU, 1, &ctx->device, &num_devices);
    if (err != CL_SUCCESS || num_devices == 0) {
        // Fallback на CPU
        err = clGetDeviceIDs(ctx->platform, CL_DEVICE_TYPE_CPU, 1, &ctx->device, &num_devices);
        if (err != CL_SUCCESS) {
            fprintf(stderr, "Ошибка: Не найдено OpenCL устройств\n");
            return -1;
        }
        printf("GPU не найден, используется CPU...\n");
    }
    
    if (print_info) {
        print_device_info(ctx->device);
    }

    // Проверка версии OpenCL (требуется 1.2+)
    if (!check_opencl_version(ctx->device, 1, 2)) {
        fprintf(stderr, "[Error] Требуется OpenCL 1.2 или выше\n");
        fprintf(stderr, "  Обновите драйверы GPU или используйте другое устройство\n");
        return -1;
    }
    if (print_info) {
        printf("[OK] Версия OpenCL соответствует требованиям (1.2+)\n\n");
    }

    // Создание контекста
    ctx->context = clCreateContext(NULL, 1, &ctx->device, NULL, NULL, &err);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "[Error] Не удалось создать OpenCL контекст: %s\n", cl_error_string(err));
        fprintf(stderr, "  Проверьте установку драйверов GPU и OpenCL runtime\n");
        return -1;
    }

    // Создание очереди команд
    ctx->queue = clCreateCommandQueue(ctx->context, ctx->device, CL_QUEUE_PROFILING_ENABLE, &err);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "[Error] Не удалось создать очередь команд: %s\n", cl_error_string(err));
        cl_cleanup(ctx);
        return -1;
    }

    ctx->is_initialized = 1;
    return 0;
}

/**
 * @brief Компиляция kernel из файла или встроенного источника
 */
int cl_compile_kernel(OpenCLContext* ctx, const char* filename) {
    cl_int err;
    size_t source_size;
    char* source = read_kernel_source(filename, &source_size);

    if (!source) {
        printf("[Info] Используем встроенный kernel\n");
        const char* embedded = get_embedded_kernel();
        source = strdup(embedded);
        if (!source) {
            fprintf(stderr, "[Error] Не удалось выделить память для встроенного kernel\n");
            return -1;
        }
        source_size = strlen(source);
    } else {
        printf("[Info] Используем kernel из файла %s\n", filename);
    }

    ctx->program = clCreateProgramWithSource(ctx->context, 1, (const char**)&source, &source_size, &err);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "[Error] Не удалось создать программу: %s\n", cl_error_string(err));
        SAFE_FREE(source);
        return -1;
    }

    // Компиляция
    err = clBuildProgram(ctx->program, 1, &ctx->device, "-cl-std=CL1.2", NULL, NULL);
    if (err != CL_SUCCESS) {
        size_t log_size;
        clGetProgramBuildInfo(ctx->program, ctx->device, CL_PROGRAM_BUILD_LOG, 0, NULL, &log_size);
        char* build_log = (char*)malloc(log_size + 1);
        if (build_log) {
            clGetProgramBuildInfo(ctx->program, ctx->device, CL_PROGRAM_BUILD_LOG, log_size, build_log, NULL);
            build_log[log_size] = '\0';
            fprintf(stderr, "[Error] Ошибка компиляции kernel:\n%s\n", build_log);
            SAFE_FREE(build_log);
        } else {
            fprintf(stderr, "[Error] Ошибка компиляции kernel (не удалось получить лог)\n");
        }
        SAFE_FREE(source);
        return -1;
    }

    // Создание kernel'ов
    ctx->kernel_sha256 = clCreateKernel(ctx->program, "sha256_hash", &err);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "[Error] Не удалось создать kernel sha256_hash: %s\n", cl_error_string(err));
        SAFE_FREE(source);
        return -1;
    }

    SAFE_FREE(source);
    return 0;
}

const char* get_embedded_kernel();

// ============================================================
// GPU ВЕРСИЯ (с улучшенной обработкой ошибок)
// ============================================================

int hash_gpu(const uint8_t* data, const uint32_t* lens, uint8_t* hashes,
             uint32_t num_hashes, uint32_t max_len, size_t local_size,
             int print_info, double* kernel_time_ms) {
    cl_int err;
    OpenCLContext ctx;
    cl_mem d_data = NULL, d_lens = NULL, d_hashes = NULL;
    cl_event event = NULL;
    int result = 0;
    
    // Инициализация
    if (cl_init(&ctx, print_info) != 0) {
        return -1;
    }
    
    // Компиляция kernel
    if (cl_compile_kernel(&ctx, "hash.cl") != 0) {
        cl_cleanup(&ctx);
        return -1;
    }
    
    // Создание буферов с проверкой размера
    size_t data_size = (size_t)num_hashes * max_len * sizeof(uint8_t);
    size_t lens_size = (size_t)num_hashes * sizeof(uint32_t);
    size_t hashes_size = (size_t)num_hashes * 32 * sizeof(uint8_t);
    
    // Проверка на переполнение
    if (data_size / max_len / sizeof(uint8_t) != num_hashes) {
        fprintf(stderr, "Ошибка: Слишком большой размер данных (переполнение)\n");
        cl_cleanup(&ctx);
        return -1;
    }
    
    d_data = clCreateBuffer(ctx.context, CL_MEM_READ_ONLY, data_size, NULL, &err);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "Ошибка создания буфера data: %s\n", cl_error_string(err));
        result = -1;
        goto cleanup;
    }
    
    d_lens = clCreateBuffer(ctx.context, CL_MEM_READ_ONLY, lens_size, NULL, &err);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "Ошибка создания буфера lens: %s\n", cl_error_string(err));
        result = -1;
        goto cleanup;
    }
    
    d_hashes = clCreateBuffer(ctx.context, CL_MEM_WRITE_ONLY, hashes_size, NULL, &err);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "Ошибка создания буфера hashes: %s\n", cl_error_string(err));
        result = -1;
        goto cleanup;
    }
    
    // Копирование данных на GPU
    err = clEnqueueWriteBuffer(ctx.queue, d_data, CL_TRUE, 0, data_size, data, 0, NULL, NULL);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "Ошибка записи данных: %s\n", cl_error_string(err));
        result = -1;
        goto cleanup;
    }
    
    err = clEnqueueWriteBuffer(ctx.queue, d_lens, CL_TRUE, 0, lens_size, lens, 0, NULL, NULL);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "Ошибка записи длин: %s\n", cl_error_string(err));
        result = -1;
        goto cleanup;
    }
    
    // Установка аргументов
    clSetKernelArg(ctx.kernel_sha256, 0, sizeof(cl_mem), &d_data);
    clSetKernelArg(ctx.kernel_sha256, 1, sizeof(cl_mem), &d_lens);
    clSetKernelArg(ctx.kernel_sha256, 2, sizeof(cl_mem), &d_hashes);
    clSetKernelArg(ctx.kernel_sha256, 3, sizeof(cl_uint), &max_len);
    
    // Выполнение kernel
    size_t global_size = ((num_hashes + local_size - 1) / local_size) * local_size;
    
    err = clEnqueueNDRangeKernel(ctx.queue, ctx.kernel_sha256, 1, NULL,
                                  &global_size, &local_size, 0, NULL, &event);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "Ошибка выполнения kernel: %s\n", cl_error_string(err));
        result = -1;
        goto cleanup;
    }
    
    clWaitForEvents(1, &event);
    
    // Получение времени выполнения
    cl_ulong time_start, time_end;
    clGetEventProfilingInfo(event, CL_PROFILING_COMMAND_START, sizeof(time_start), &time_start, NULL);
    clGetEventProfilingInfo(event, CL_PROFILING_COMMAND_END, sizeof(time_end), &time_end, NULL);
    *kernel_time_ms = (double)(time_end - time_start) / 1000000.0;
    
    // Чтение результатов
    err = clEnqueueReadBuffer(ctx.queue, d_hashes, CL_TRUE, 0, hashes_size, hashes, 0, NULL, NULL);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "Ошибка чтения результатов: %s\n", cl_error_string(err));
        result = -1;
        goto cleanup;
    }

cleanup:
    if (event) clReleaseEvent(event);
    if (d_data) clReleaseMemObject(d_data);
    if (d_lens) clReleaseMemObject(d_lens);
    if (d_hashes) clReleaseMemObject(d_hashes);
    cl_cleanup(&ctx);
    
    return result;
}

// ============================================================
// ВСТРОЕННЫЙ KERNEL
// ============================================================

const char* get_embedded_kernel() {
    return
    "// SHA-256 Constants\n"
    "constant uint SHA256_H[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};\n"
    "constant uint SHA256_K[64] = {0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};\n"
    "#define ROTR(x,n) (((x)>>(n))|((x)<<(32-(n))))\n"
    "#define CH(x,y,z) (((x)&(y))^(~(x)&(z)))\n"
    "#define MAJ(x,y,z) (((x)&(y))^((x)&(z))^((y)&(z)))\n"
    "#define EP0(x) (ROTR(x,2)^ROTR(x,13)^ROTR(x,22))\n"
    "#define EP1(x) (ROTR(x,6)^ROTR(x,11)^ROTR(x,25))\n"
    "#define SIG0(x) (ROTR(x,7)^ROTR(x,18)^((x)>>3))\n"
    "#define SIG1(x) (ROTR(x,17)^ROTR(x,19)^((x)>>10))\n"
    "__kernel void sha256_hash(__global const uchar* input,__global const uint* input_lens,__global uchar* output,const uint max_len){\n"
    "uint gid=get_global_id(0);uint offset=gid*max_len;uint len=input_lens[gid];uint w[64];uint h[8];for(int i=0;i<8;i++)h[i]=SHA256_H[i];\n"
    "uint num_blocks=(len+9+63)/64;if(num_blocks<1)num_blocks=1;\n"
    "for(uint block=0;block<num_blocks;block++){\n"
    "for(int i=0;i<64;i++)w[i]=0;\n"
    "uint bytes_in_block=0;for(uint i=0;i<64;i++){uint pos=block*64+i;if(pos<len){uint wi=i>>2;uint bi=3-(i&3);w[wi]|=((uint)input[offset+pos])<<(bi<<3);bytes_in_block++;}}\n"
    "if(bytes_in_block<64){uint wi=bytes_in_block>>2;uint bi=3-(bytes_in_block&3);w[wi]|=((uint)0x80)<<(bi<<3);}\n"
    "if(block==num_blocks-1){w[14]=(len>>29)&0x07;w[15]=(len<<3)&0xFFFFFFFF;}\n"
    "for(int i=16;i<64;i++)w[i]=SIG1(w[i-2])+w[i-7]+SIG0(w[i-15])+w[i-16];\n"
    "uint a=h[0],b=h[1],c=h[2],d=h[3],e=h[4],f=h[5],g=h[6],hv=h[7];\n"
    "for(int i=0;i<64;i++){uint t1=hv+EP1(e)+CH(e,f,g)+SHA256_K[i]+w[i];uint t2=EP0(a)+MAJ(a,b,c);hv=g;g=f;f=e;e=d+t1;d=c;c=b;b=a;a=t1+t2;}\n"
    "h[0]+=a;h[1]+=b;h[2]+=c;h[3]+=d;h[4]+=e;h[5]+=f;h[6]+=g;h[7]+=hv;}\n"
    "for(int i=0;i<8;i++){output[gid*32+(i<<2)+0]=(h[i]>>24)&0xFF;output[gid*32+(i<<2)+1]=(h[i]>>16)&0xFF;output[gid*32+(i<<2)+2]=(h[i]>>8)&0xFF;output[gid*32+(i<<2)+3]=h[i]&0xFF;}}\n"
    "__kernel void djb2_hash(__global const uchar* input,__global const uint* input_lens,__global uint* output,const uint max_len){\n"
    "uint gid=get_global_id(0);uint offset=gid*max_len;uint len=input_lens[gid];uint hash=5381;\n"
    "for(uint i=0;i<len;i++)hash=((hash<<5)+hash)+input[offset+i];output[gid]=hash;}\n"
    "__kernel void fnv1a_hash(__global const uchar* input,__global const uint* input_lens,__global uint* output,const uint max_len){\n"
    "uint gid=get_global_id(0);uint offset=gid*max_len;uint len=input_lens[gid];uint hash=2166136261u;\n"
    "for(uint i=0;i<len;i++){hash^=input[offset+i];hash*=16777619u;}output[gid]=hash;}\n";
}

// ============================================================
// ВЫВОД ХЭШЕЙ
// ============================================================

void print_hash(const uint8_t* hash, const char* label) {
    printf("%s: ", label);
    for (int i = 0; i < 32; i++) {
        printf("%02x", hash[i]);
    }
    printf("\n");
}

void compare_hashes(const uint8_t* cpu, const uint8_t* gpu, uint32_t num_hashes) {
    int matches = 0;
    for (uint32_t i = 0; i < num_hashes; i++) {
        int match = 1;
        for (int j = 0; j < 32; j++) {
            if (cpu[i*32 + j] != gpu[i*32 + j]) {
                match = 0;
                break;
            }
        }
        if (match) matches++;
    }
    printf("  Совпадений: %u / %u (%.1f%%)\n", matches, num_hashes, 
           100.0 * matches / num_hashes);
}

// ============================================================
// ВАЛИДАЦИЯ ВХОДНЫХ ДАННЫХ
// ============================================================

/**
 * @brief Валидация входных параметров программы
 * @param num_hashes Количество хэшей
 * @param max_len Максимальная длина данных
 * @param local_size Размер work-group
 * @return 0 при успехе, -1 при ошибке
 */
int validate_inputs(uint32_t* num_hashes, uint32_t* max_len, size_t* local_size) {
    // Проверка num_hashes
    if (*num_hashes < 1) {
        fprintf(stderr, "[Error] num_hashes должен быть >= 1\n");
        return -1;
    }
    if (*num_hashes > MAX_NUM_HASHES) {
        fprintf(stderr, "[Error] num_hashes слишком большой (максимум %d)\n", MAX_NUM_HASHES);
        fprintf(stderr, "  Установлено значение: %d\n", MAX_NUM_HASHES);
        *num_hashes = MAX_NUM_HASHES;
    }

    // Проверка max_len
    if (*max_len < 1) {
        fprintf(stderr, "[Error] max_len должен быть >= 1\n");
        return -1;
    }
    if (*max_len > MAX_DATA_LEN) {
        fprintf(stderr, "[Error] max_len слишком большой (максимум %zu)\n", MAX_DATA_LEN);
        *max_len = MAX_DATA_LEN;
    }

    // Проверка local_size
    if (*local_size < MIN_LOCAL_SIZE) {
        fprintf(stderr, "[Error] local_size должен быть >= %d\n", MIN_LOCAL_SIZE);
        return -1;
    }
    if (*local_size > MAX_LOCAL_SIZE) {
        fprintf(stderr, "[Warning] local_size слишком большой, уменьшено до %d\n", MAX_LOCAL_SIZE);
        *local_size = MAX_LOCAL_SIZE;
    }

    // Округляем local_size до степени двойки
    size_t power = 1;
    while (power * 2 <= *local_size) power *= 2;
    *local_size = power;

    // Проверка на переполнение при вычислении размера памяти
    size_t data_size = (size_t)*num_hashes * *max_len;
    if (data_size / *max_len != *num_hashes) {
        fprintf(stderr, "[Error] Переполнение при вычислении размера данных\n");
        return -1;
    }

    return 0;
}

// ============================================================
// ГЛАВНАЯ ФУНКЦИЯ
// ============================================================

int main(int argc, char** argv) {
    uint32_t num_hashes = DEFAULT_NUM_HASHES;
    uint32_t max_len = DEFAULT_DATA_LEN;
    size_t local_size = DEFAULT_LOCAL_SIZE;

    // Парсинг аргументов
    if (argc >= 2) num_hashes = (uint32_t)atol(argv[1]);
    if (argc >= 3) max_len = (uint32_t)atol(argv[2]);
    if (argc >= 4) local_size = (size_t)atol(argv[3]);

    // Валидация входных данных
    if (validate_inputs(&num_hashes, &max_len, &local_size) != 0) {
        fprintf(stderr, "Использование: %s [num_hashes] [max_len] [local_size]\n", argv[0]);
        fprintf(stderr, "  num_hashes: 1 - %d (по умолчанию %d)\n", MAX_NUM_HASHES, DEFAULT_NUM_HASHES);
        fprintf(stderr, "  max_len: 1 - %zu (по умолчанию %d)\n", MAX_DATA_LEN, DEFAULT_DATA_LEN);
        fprintf(stderr, "  local_size: 1 - %d (по умолчанию %d)\n", MAX_LOCAL_SIZE, DEFAULT_LOCAL_SIZE);
        return 1;
    }
    
    printf("============================================================\n");
    printf("  ЛАБОРАТОРНАЯ РАБОТА: Параллельное хэширование на GPU\n");
    printf("============================================================\n");
    printf("  Параметры:\n");
    printf("    Количество хэшей:   %u\n", num_hashes);
    printf("    Макс. длина данных: %u байт\n", max_len);
    printf("    Размер work-group:  %zu\n", local_size);
    printf("============================================================\n\n");
    
    // Выделение памяти
    uint8_t* data = (uint8_t*)malloc(num_hashes * max_len);
    uint32_t* lens = (uint32_t*)malloc(num_hashes * sizeof(uint32_t));
    uint8_t* cpu_hashes = (uint8_t*)malloc(num_hashes * 32);
    uint8_t* gpu_hashes = (uint8_t*)malloc(num_hashes * 32);
    
    if (!data || !lens || !cpu_hashes || !gpu_hashes) {
        fprintf(stderr, "Ошибка: Не удалось выделить память\n");
        free(data);
        free(lens);
        free(cpu_hashes);
        free(gpu_hashes);
        return 1;
    }
    
    // Генерация тестовых данных
    printf(">>> Генерация тестовых данных...\n");
    generate_test_data(data, lens, num_hashes, max_len);
    printf("    Сгенерировано %u блоков данных\n\n", num_hashes);
    
    // CPU версия
    printf(">>> Запуск CPU версии (SHA-256)...\n");
    clock_t cpu_start = clock();
    hash_all_cpu(data, lens, cpu_hashes, num_hashes, max_len);
    clock_t cpu_end = clock();
    double cpu_time_ms = ((double)(cpu_end - cpu_start)) / CLOCKS_PER_SEC * 1000.0;
    printf("    Время выполнения: %.3f мс\n", cpu_time_ms);
    printf("    Скорость: %.0f хэшей/сек\n\n", num_hashes / (cpu_time_ms / 1000.0));
    
    // GPU версия
    printf(">>> Запуск GPU версии (SHA-256)...\n");
    double gpu_kernel_time = 0;
    clock_t gpu_total_start = clock();
    int gpu_result = hash_gpu(data, lens, gpu_hashes, num_hashes, max_len, local_size, 1, &gpu_kernel_time);
    clock_t gpu_total_end = clock();
    double gpu_total_time_ms = ((double)(gpu_total_end - gpu_total_start)) / CLOCKS_PER_SEC * 1000.0;
    
    if (gpu_result != 0) {
        fprintf(stderr, "Ошибка выполнения GPU версии\n");
        free(data);
        free(lens);
        free(cpu_hashes);
        free(gpu_hashes);
        return 1;
    }
    
    printf("    Время kernel: %.3f мс\n", gpu_kernel_time);
    printf("    Общее время: %.3f мс\n", gpu_total_time_ms);
    printf("    Скорость: %.0f хэшей/сек\n\n", num_hashes / (gpu_kernel_time / 1000.0));
    
    // Сравнение результатов
    printf("============================================================\n");
    printf("  РЕЗУЛЬТАТЫ СРАВНЕНИЯ\n");
    printf("============================================================\n");
    
    compare_hashes(cpu_hashes, gpu_hashes, num_hashes);
    
    printf("\n");
    printf("  Время CPU:        %10.3f мс\n", cpu_time_ms);
    printf("  Время GPU kernel: %10.3f мс\n", gpu_kernel_time);
    printf("  Время GPU общее:  %10.3f мс\n", gpu_total_time_ms);
    
    double speedup = cpu_time_ms / gpu_kernel_time;
    printf("\n  Ускорение (kernel): %10.2fx\n", speedup);
    printf("  Ускорение (общее):  %10.2fx\n", cpu_time_ms / gpu_total_time_ms);
    
    printf("============================================================\n\n");
    
    // Вывод первых хэшей
    printf("Примеры хэшей:\n");
    for (int i = 0; i < 3 && i < (int)num_hashes; i++) {
        printf("\nХэш #%d (длина данных: %u байт):\n", i+1, lens[i]);
        print_hash(cpu_hashes + i*32, "  CPU");
        print_hash(gpu_hashes + i*32, "  GPU");
    }
    
    // Освобождение памяти
    free(data);
    free(lens);
    free(cpu_hashes);
    free(gpu_hashes);
    
    return 0;
}
