/**
 * @file cl_utils.c
 * @brief Реализация общих утилит для работы с OpenCL
 *
 * Этот файл содержит функции для:
 * - Инициализации и управления контекстом OpenCL
 * - Компиляции kernel'ов из файлов и источников
 * - Получения информации об устройствах и платформах
 * - Работы с файлами (загрузка kernel source)
 * - Бенчмаркинга и профилирования
 */

#include "cl_common.h"

#ifdef _WIN32
#include <windows.h>
#else
#include <unistd.h>
#include <limits.h>
#endif

// ============================================================
// ФУНКЦИИ ОБРАБОТКИ ОШИБОК
// ============================================================

const char* cl_get_error_string(cl_int err) {
    switch (err) {
        case CL_SUCCESS:                        return "Success";
        case CL_DEVICE_NOT_FOUND:               return "Device not found";
        case CL_DEVICE_NOT_AVAILABLE:           return "Device not available";
        case CL_COMPILER_NOT_AVAILABLE:         return "Compiler not available";
        case CL_MEM_OBJECT_ALLOCATION_FAILURE:  return "Memory allocation failure";
        case CL_OUT_OF_RESOURCES:               return "Out of resources";
        case CL_OUT_OF_HOST_MEMORY:             return "Out of host memory";
        case CL_PROFILING_INFO_NOT_AVAILABLE:   return "Profiling info not available";
        case CL_BUILD_PROGRAM_FAILURE:          return "Build program failure";
        case CL_INVALID_VALUE:                  return "Invalid value";
        case CL_INVALID_DEVICE:                 return "Invalid device";
        case CL_INVALID_CONTEXT:                return "Invalid context";
        case CL_INVALID_QUEUE_PROPERTIES:       return "Invalid queue properties";
        case CL_INVALID_COMMAND_QUEUE:          return "Invalid command queue";
        case CL_INVALID_MEM_OBJECT:             return "Invalid memory object";
        case CL_INVALID_PROGRAM:                return "Invalid program";
        case CL_INVALID_KERNEL:                 return "Invalid kernel";
        case CL_INVALID_ARG_INDEX:              return "Invalid argument index";
        case CL_INVALID_ARG_VALUE:              return "Invalid argument value";
        case CL_INVALID_ARG_SIZE:               return "Invalid argument size";
        case CL_INVALID_WORK_DIMENSION:         return "Invalid work dimension";
        case CL_INVALID_WORK_GROUP_SIZE:        return "Invalid work group size";
        case CL_INVALID_WORK_ITEM_SIZE:         return "Invalid work item size";
        case CL_INVALID_GLOBAL_OFFSET:          return "Invalid global offset";
        case CL_INVALID_EVENT_WAIT_LIST:        return "Invalid event wait list";
        case CL_INVALID_EVENT:                  return "Invalid event";
        case CL_INVALID_OPERATION:              return "Invalid operation";
        case CL_INVALID_BUFFER_SIZE:            return "Invalid buffer size";
        case CL_INVALID_MIP_LEVEL:              return "Invalid MIP level";
        case CL_INVALID_GL_OBJECT:              return "Invalid GL object";
        default:                                return "Unknown OpenCL error";
    }
}

/**
 * @brief Получение расширенного описания ошибки с кодом
 * @param err Код ошибки
 * @param buffer Буфер для результата
 * @param buffer_size Размер буфера
 * @return Строка с описанием ошибки
 */
void cl_get_error_description(cl_int err, char* buffer, size_t buffer_size) {
    if (!buffer || buffer_size == 0) return;

    const char* error_str = cl_get_error_string(err);
    snprintf(buffer, buffer_size, "Error %d (%s)", err, error_str);
}

// ============================================================
// ФУНКЦИИ УПРАВЛЕНИЯ КОНТЕКСТОМ
// ============================================================

int cl_context_init(OpenCLContext* ctx, cl_device_type device_type, int print_info) {
    cl_int err;
    cl_uint num_platforms, num_devices;

    if (!ctx) return -1;
    memset(ctx, 0, sizeof(OpenCLContext));

    // Получение платформ
    err = clGetPlatformIDs(1, &ctx->platform, &num_platforms);
    if (err != CL_SUCCESS || num_platforms == 0) {
        fprintf(stderr, "Ошибка: Не найдено OpenCL платформ\n");
        return -1;
    }

    // Попытка найти устройство запрошенного типа
    err = clGetDeviceIDs(ctx->platform, device_type, 1, &ctx->device, &num_devices);
    if (err != CL_SUCCESS || num_devices == 0) {
        // Fallback на CPU если GPU не найден
        if (device_type == CL_DEVICE_TYPE_GPU) {
            fprintf(stderr, "GPU не найден, попытка использования CPU...\n");
            err = clGetDeviceIDs(ctx->platform, CL_DEVICE_TYPE_CPU, 1, &ctx->device, &num_devices);
            if (err != CL_SUCCESS) {
                fprintf(stderr, "Ошибка: Не найдено OpenCL устройств\n");
                return -1;
            }
        } else {
            fprintf(stderr, "Ошибка: Не найдено OpenCL устройств\n");
            return -1;
        }
    }

    if (print_info) {
        cl_print_device_info(ctx->device);
    }

    // Создание контекста
    ctx->context = clCreateContext(NULL, 1, &ctx->device, NULL, NULL, &err);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "Ошибка создания контекста: %s\n", cl_get_error_string(err));
        return -1;
    }

    // Создание очереди команд с профилированием
    // Для OpenCL 3.0 используем новый API clCreateCommandQueueWithProperties
    cl_queue_properties queue_props[] = {
        CL_QUEUE_PROPERTIES, CL_QUEUE_PROFILING_ENABLE, 0
    };
    ctx->queue = clCreateCommandQueueWithProperties(ctx->context, ctx->device, queue_props, &err);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "Ошибка создания очереди команд: %s\n", cl_get_error_string(err));
        cl_context_cleanup(ctx);
        return -1;
    }

    ctx->is_initialized = 1;
    return 0;
}

void cl_context_cleanup(OpenCLContext* ctx) {
    if (!ctx) return;

    if (ctx->kernel_sha256) clReleaseKernel(ctx->kernel_sha256);
    if (ctx->kernel_djb2) clReleaseKernel(ctx->kernel_djb2);
    if (ctx->kernel_fnv1a) clReleaseKernel(ctx->kernel_fnv1a);
    if (ctx->program) clReleaseProgram(ctx->program);
    if (ctx->queue) clReleaseCommandQueue(ctx->queue);
    if (ctx->context) clReleaseContext(ctx->context);

    memset(ctx, 0, sizeof(OpenCLContext));
}

int cl_compile_kernel_from_file(OpenCLContext* ctx, const char* kernel_filename, 
                                 const char* build_options) {
    cl_int err;
    size_t source_size;
    char* source = NULL;

    if (!ctx || !kernel_filename) return -1;

    // Чтение файла с kernel'ом
    source = cl_read_kernel_file(kernel_filename, &source_size);
    
    if (!source) {
        fprintf(stderr, "Предупреждение: Файл %s не найден, используется встроенный kernel\n", 
                kernel_filename);
        return -1;  // Caller должен использовать встроенный kernel
    }

    // Создание программы
    ctx->program = clCreateProgramWithSource(ctx->context, 1, (const char**)&source, 
                                              &source_size, &err);
    SAFE_FREE(source);
    
    if (err != CL_SUCCESS) {
        fprintf(stderr, "Ошибка создания программы: %s\n", cl_get_error_string(err));
        return -1;
    }

    // Компиляция
    const char* default_options = "-cl-std=CL1.2";
    err = clBuildProgram(ctx->program, 1, &ctx->device, 
                         build_options ? build_options : default_options, 
                         NULL, NULL);
    
    if (err != CL_SUCCESS) {
        size_t log_size;
        clGetProgramBuildInfo(ctx->program, ctx->device, CL_PROGRAM_BUILD_LOG, 
                              0, NULL, &log_size);
        char* build_log = (char*)malloc(log_size + 1);
        if (build_log) {
            clGetProgramBuildInfo(ctx->program, ctx->device, CL_PROGRAM_BUILD_LOG, 
                                  log_size, build_log, NULL);
            build_log[log_size] = '\0';
            fprintf(stderr, "Ошибка компиляции kernel:\n%s\n", build_log);
            SAFE_FREE(build_log);
        }
        return -1;
    }

    return 0;
}

int cl_compile_kernel_from_source(OpenCLContext* ctx, const char* kernel_source,
                                   const char* build_options) {
    cl_int err;
    size_t source_size;

    if (!ctx || !kernel_source) return -1;

    source_size = strlen(kernel_source);

    // Создание программы
    ctx->program = clCreateProgramWithSource(ctx->context, 1, &kernel_source, 
                                              &source_size, &err);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "Ошибка создания программы: %s\n", cl_get_error_string(err));
        return -1;
    }

    // Компиляция
    const char* default_options = "-cl-std=CL1.2";
    err = clBuildProgram(ctx->program, 1, &ctx->device, 
                         build_options ? build_options : default_options, 
                         NULL, NULL);
    
    if (err != CL_SUCCESS) {
        size_t log_size;
        clGetProgramBuildInfo(ctx->program, ctx->device, CL_PROGRAM_BUILD_LOG, 
                              0, NULL, &log_size);
        char* build_log = (char*)malloc(log_size + 1);
        if (build_log) {
            clGetProgramBuildInfo(ctx->program, ctx->device, CL_PROGRAM_BUILD_LOG, 
                                  log_size, build_log, NULL);
            build_log[log_size] = '\0';
            fprintf(stderr, "Ошибка компиляции kernel:\n%s\n", build_log);
            SAFE_FREE(build_log);
        }
        return -1;
    }

    return 0;
}

cl_kernel cl_create_kernel(OpenCLContext* ctx, const char* kernel_name) {
    cl_int err;
    cl_kernel kernel;

    if (!ctx || !kernel_name) return NULL;

    kernel = clCreateKernel(ctx->program, kernel_name, &err);
    if (err != CL_SUCCESS) {
        fprintf(stderr, "Ошибка создания kernel '%s': %s\n", 
                kernel_name, cl_get_error_string(err));
        return NULL;
    }

    return kernel;
}

// ============================================================
// ФУНКЦИИ ИНФОРМАЦИИ ОБ УСТРОЙСТВЕ
// ============================================================

int cl_get_device_info(cl_device_id device, DeviceInfo* info) {
    cl_int err;

    if (!device || !info) return -1;

    memset(info, 0, sizeof(DeviceInfo));

    err = clGetDeviceInfo(device, CL_DEVICE_NAME, sizeof(info->name), info->name, NULL);
    if (err != CL_SUCCESS) return -1;

    err = clGetDeviceInfo(device, CL_DEVICE_VENDOR, sizeof(info->vendor), info->vendor, NULL);
    if (err != CL_SUCCESS) return -1;

    err = clGetDeviceInfo(device, CL_DEVICE_VERSION, sizeof(info->version), info->version, NULL);
    if (err != CL_SUCCESS) return -1;

    err = clGetDeviceInfo(device, CL_DEVICE_TYPE, sizeof(info->type), &info->type, NULL);
    if (err != CL_SUCCESS) return -1;

    err = clGetDeviceInfo(device, CL_DEVICE_MAX_COMPUTE_UNITS, sizeof(info->compute_units), 
                          &info->compute_units, NULL);
    if (err != CL_SUCCESS) return -1;

    err = clGetDeviceInfo(device, CL_DEVICE_MAX_WORK_GROUP_SIZE, sizeof(info->max_work_group_size), 
                          &info->max_work_group_size, NULL);
    if (err != CL_SUCCESS) return -1;

    err = clGetDeviceInfo(device, CL_DEVICE_GLOBAL_MEM_SIZE, sizeof(info->global_mem_size), 
                          &info->global_mem_size, NULL);
    if (err != CL_SUCCESS) return -1;

    err = clGetDeviceInfo(device, CL_DEVICE_LOCAL_MEM_SIZE, sizeof(info->local_mem_size), 
                          &info->local_mem_size, NULL);
    if (err != CL_SUCCESS) return -1;

    return 0;
}

void cl_print_device_info(cl_device_id device) {
    DeviceInfo info;

    if (cl_get_device_info(device, &info) != 0) {
        fprintf(stderr, "Ошибка получения информации об устройстве\n");
        return;
    }

    printf("\n========================================\n");
    printf("ИНФОРМАЦИЯ ОБ УСТРОЙСТВЕ:\n");
    printf("========================================\n");
    printf("  Название:              %s\n", info.name);
    printf("  Производитель:         %s\n", info.vendor);
    printf("  Версия OpenCL:         %s\n", info.version);
    printf("  Тип устройства:        %s\n", 
           info.type == CL_DEVICE_TYPE_GPU ? "GPU" : 
           info.type == CL_DEVICE_TYPE_CPU ? "CPU" : "Другое");
    printf("  Вычислительные блоки:  %u\n", info.compute_units);
    printf("  Макс. work-group:      %zu\n", info.max_work_group_size);
    printf("  Глобальная память:     %.0f MB\n", (double)info.global_mem_size / (1024 * 1024));
    printf("  Локальная память:      %.0f KB\n", (double)info.local_mem_size / 1024);
    printf("========================================\n\n");
}

void cl_print_platforms_info(void) {
    cl_uint num_platforms;
    cl_platform_id platforms[CL_MAX_PLATFORMS];
    cl_int err;

    err = clGetPlatformIDs(CL_MAX_PLATFORMS, platforms, &num_platforms);
    if (err != CL_SUCCESS || num_platforms == 0) {
        printf("Не найдено OpenCL платформ\n");
        return;
    }

    printf("\n========================================\n");
    printf("ДОСТУПНЫЕ OPENCL ПЛАТФОРМЫ: %u\n", num_platforms);
    printf("========================================\n");

    for (cl_uint i = 0; i < num_platforms; i++) {
        char platform_name[128];
        char platform_vendor[128];
        char platform_version[128];

        clGetPlatformInfo(platforms[i], CL_PLATFORM_NAME, sizeof(platform_name), 
                          platform_name, NULL);
        clGetPlatformInfo(platforms[i], CL_PLATFORM_VENDOR, sizeof(platform_vendor), 
                          platform_vendor, NULL);
        clGetPlatformInfo(platforms[i], CL_PLATFORM_VERSION, sizeof(platform_version), 
                          platform_version, NULL);

        printf("\nПлатформа %u:\n", i + 1);
        printf("  Название:    %s\n", platform_name);
        printf("  Производитель: %s\n", platform_vendor);
        printf("  Версия:      %s\n", platform_version);

        // Получаем устройства для этой платформы
        cl_uint num_devices;
        cl_device_id devices[CL_MAX_DEVICES];
        
        err = clGetDeviceIDs(platforms[i], CL_DEVICE_TYPE_ALL, CL_MAX_DEVICES, 
                             devices, &num_devices);
        if (err == CL_SUCCESS) {
            printf("  Устройств:   %u\n", num_devices);
            
            for (cl_uint j = 0; j < num_devices; j++) {
                DeviceInfo dev_info;
                if (cl_get_device_info(devices[j], &dev_info) == 0) {
                    printf("    [%u] %s (%s)\n", j + 1, dev_info.name, 
                           dev_info.type == CL_DEVICE_TYPE_GPU ? "GPU" : "CPU");
                }
            }
        }
    }
    printf("========================================\n\n");
}

size_t cl_auto_detect_local_size(cl_device_id device, size_t suggested) {
    size_t max_work_group;
    cl_int err;

    err = clGetDeviceInfo(device, CL_DEVICE_MAX_WORK_GROUP_SIZE, 
                          sizeof(max_work_group), &max_work_group, NULL);
    if (err != CL_SUCCESS) {
        return suggested > 0 ? suggested : 256;
    }

    // Рекомендуемое значение или max/2
    size_t optimal = (suggested > 0 && suggested <= max_work_group) ? suggested : max_work_group / 2;

    // Округляем до степени двойки
    size_t power = 1;
    while (power * 2 <= optimal && power * 2 <= max_work_group) {
        power *= 2;
    }

    printf("    Автоопределение local_size: max=%zu, выбрано=%zu\n", 
           max_work_group, power);
    return power;
}

// ============================================================
// ФУНКЦИИ РАБОТЫ С ФАЙЛАМИ
// ============================================================

#ifdef _WIN32
#include <windows.h>
#include <shlwapi.h>
#endif

/**
 * @brief Попытка открыть файл из нескольких возможных мест
 * Сначала ищет в текущей директории, затем рядом с exe, затем в стандартных путях
 * 
 * Пути поиска:
 * 1. Текущая рабочая директория (./)
 * 2. Директория исполняемого файла
 * 3. Директория сборки (../build/)
 * 4. Директория исходников (../../hashing/, ../../sieve/)
 * 5. Системные директории (/usr/local/share/gpu_lab/kernels/)
 */
static FILE* open_kernel_file(const char* filename) {
    FILE* f = NULL;

    // 1. Пробуем открыть в текущей рабочей директории
    f = fopen(filename, "r");
    if (f) return f;

#ifdef _WIN32
    // 2. Пробуем открыть в директории исполняемого файла
    char exe_path[MAX_PATH];
    char kernel_path[MAX_PATH * 2];  // Увеличенный буфер для полного пути

    if (GetModuleFileNameA(NULL, exe_path, MAX_PATH) > 0) {
        // Получаем директорию exe файла
        PathRemoveFileSpecA(exe_path);

        // Копируем путь с проверкой на переполнение
        int written = snprintf(kernel_path, sizeof(kernel_path), "%s\\%s", exe_path, filename);
        if (written > 0 && (size_t)written < sizeof(kernel_path)) {
            f = fopen(kernel_path, "r");
            if (f) return f;
        }

        // 3. Для CMake сборки: kernel может быть в build директории
        written = snprintf(kernel_path, sizeof(kernel_path), "%s\\..\\%s", exe_path, filename);
        if (written > 0 && (size_t)written < sizeof(kernel_path)) {
            f = fopen(kernel_path, "r");
            if (f) return f;
        }

        // 4. Для CMake сборки: kernel может быть в share/gpu_lab/kernels
        written = snprintf(kernel_path, sizeof(kernel_path), "%s\\..\\share\\gpu_lab\\kernels\\%s", exe_path, filename);
        if (written > 0 && (size_t)written < sizeof(kernel_path)) {
            f = fopen(kernel_path, "r");
            if (f) return f;
        }
        
        // 5. Директория исходников hashing/
        written = snprintf(kernel_path, sizeof(kernel_path), "%s\\..\\..\\hashing\\%s", exe_path, filename);
        if (written > 0 && (size_t)written < sizeof(kernel_path)) {
            f = fopen(kernel_path, "r");
            if (f) return f;
        }
        
        // 6. Директория исходников sieve/
        written = snprintf(kernel_path, sizeof(kernel_path), "%s\\..\\..\\sieve\\%s", exe_path, filename);
        if (written > 0 && (size_t)written < sizeof(kernel_path)) {
            f = fopen(kernel_path, "r");
            if (f) return f;
        }
    }
#else
    // 3. Для Linux/Mac: ищем в стандартных путях
    const char* std_paths[] = {
        "./",
        "../",
        "../build/",
        "../../hashing/",
        "../../sieve/",
        "../share/gpu_lab/kernels/",
        "/usr/local/share/gpu_lab/kernels/",
        "/usr/share/gpu_lab/kernels/",
        NULL
    };

    char kernel_path[1024];  // Увеличенный буфер
    for (int i = 0; std_paths[i] != NULL; i++) {
        int written = snprintf(kernel_path, sizeof(kernel_path), "%s%s", std_paths[i], filename);
        if (written > 0 && (size_t)written < sizeof(kernel_path)) {
            f = fopen(kernel_path, "r");
            if (f) return f;
        }
    }
#endif

    return NULL;
}

char* cl_read_kernel_file(const char* filename, size_t* size) {
    FILE* file = NULL;
    char* source = NULL;

    if (!filename || !size) return NULL;

    file = open_kernel_file(filename);
    if (!file) {
        return NULL;
    }

    source = (char*)malloc(CL_MAX_SOURCE_SIZE);
    if (!source) {
        fprintf(stderr, "Ошибка: Не удалось выделить память для kernel source\n");
        fclose(file);
        return NULL;
    }

    *size = fread(source, 1, CL_MAX_SOURCE_SIZE - 1, file);
    source[*size] = '\0';
    fclose(file);

    return source;
}

int cl_file_exists(const char* path) {
    FILE* f = fopen(path, "r");
    if (f) {
        fclose(f);
        return 1;
    }
    return 0;
}

// ============================================================
// ФУНКЦИИ БЕНЧМАРКА
// ============================================================

double cl_get_kernel_time_ms(cl_event event) {
    cl_ulong time_start, time_end;
    cl_int err;

    if (!event) return 0.0;

    err = clGetEventProfilingInfo(event, CL_PROFILING_COMMAND_START, 
                                   sizeof(time_start), &time_start, NULL);
    if (err != CL_SUCCESS) return 0.0;

    err = clGetEventProfilingInfo(event, CL_PROFILING_COMMAND_END, 
                                   sizeof(time_end), &time_end, NULL);
    if (err != CL_SUCCESS) return 0.0;

    return (double)(time_end - time_start) / 1000000.0;
}

void cl_format_benchmark_result(const BenchmarkResult* result, char* buffer, size_t buffer_size) {
    if (!result || !buffer || buffer_size == 0) return;

    snprintf(buffer, buffer_size,
             "Тест: %s\n"
             "  CPU время:     %.3f мс\n"
             "  GPU время:     %.3f мс\n"
             "  GPU общее:     %.3f мс\n"
             "  Ускорение:     %.2fx\n"
             "  Память:        %.2f KB\n"
             "  Корректность:  %s\n",
             result->name,
             result->cpu_time_ms,
             result->gpu_time_ms,
             result->gpu_total_time_ms,
             result->speedup,
             (double)result->memory_used / 1024.0,
             result->correct ? "OK" : "FAILED");
}
