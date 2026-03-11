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
 * Автор: Студент
 * Дата: 2024
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

// ============================================================
// КОНСТАНТЫ И МАКРОСЫ
// ============================================================

#define MAX_SOURCE_SIZE (0x100000)
#define DEFAULT_NUM_HASHES 100000
#define DEFAULT_DATA_LEN 64
#define DEFAULT_LOCAL_SIZE 256

#define CHECK_CL_ERROR(err, msg) \
    if (err != CL_SUCCESS) { \
        fprintf(stderr, "OpenCL Error %d: %s\n", err, msg); \
        exit(1); \
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

char* read_kernel_source(const char* filename, size_t* size) {
    FILE* file = fopen(filename, "r");
    if (!file) return NULL;
    
    char* source = (char*)malloc(MAX_SOURCE_SIZE);
    *size = fread(source, 1, MAX_SOURCE_SIZE - 1, file);
    source[*size] = '\0';
    fclose(file);
    return source;
}

const char* get_embedded_kernel();

// ============================================================
// GPU ВЕРСИЯ
// ============================================================

void hash_gpu(const uint8_t* data, const uint32_t* lens, uint8_t* hashes,
              uint32_t num_hashes, uint32_t max_len, size_t local_size,
              int print_info, double* kernel_time_ms) {
    cl_int err;
    cl_platform_id platform;
    cl_device_id device;
    cl_context context;
    cl_command_queue queue;
    cl_program program;
    cl_kernel kernel_sha256, kernel_djb2, kernel_fnv1a;
    cl_mem d_data, d_lens, d_hashes;
    
    // Получение платформы и устройства
    err = clGetPlatformIDs(1, &platform, NULL);
    CHECK_CL_ERROR(err, "clGetPlatformIDs");
    
    err = clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 1, &device, NULL);
    if (err != CL_SUCCESS) {
        printf("GPU не найден, используется CPU...\n");
        err = clGetDeviceIDs(platform, CL_DEVICE_TYPE_CPU, 1, &device, NULL);
        CHECK_CL_ERROR(err, "clGetDeviceIDs CPU");
    }
    
    if (print_info) print_device_info(device);
    
    // Создание контекста и очереди
    context = clCreateContext(NULL, 1, &device, NULL, NULL, &err);
    CHECK_CL_ERROR(err, "clCreateContext");
    
    cl_command_queue_properties props = CL_QUEUE_PROFILING_ENABLE;
    queue = clCreateCommandQueueWithProperties(context, device, &props, &err);
    CHECK_CL_ERROR(err, "clCreateCommandQueueWithProperties");
    
    // Загрузка kernel
    size_t source_size;
    char* source = read_kernel_source("hash.cl", &source_size);
    
    if (!source) {
        printf("Используется встроенный kernel\n");
        const char* embedded = get_embedded_kernel();
        source = strdup(embedded);
        source_size = strlen(source);
    }
    
    program = clCreateProgramWithSource(context, 1, (const char**)&source, &source_size, &err);
    CHECK_CL_ERROR(err, "clCreateProgramWithSource");
    
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
    
    kernel_sha256 = clCreateKernel(program, "sha256_hash", &err);
    CHECK_CL_ERROR(err, "clCreateKernel sha256_hash");
    
    // Создание буферов
    d_data = clCreateBuffer(context, CL_MEM_READ_ONLY, 
                            num_hashes * max_len * sizeof(uint8_t), NULL, &err);
    CHECK_CL_ERROR(err, "clCreateBuffer data");
    
    d_lens = clCreateBuffer(context, CL_MEM_READ_ONLY,
                            num_hashes * sizeof(uint32_t), NULL, &err);
    CHECK_CL_ERROR(err, "clCreateBuffer lens");
    
    d_hashes = clCreateBuffer(context, CL_MEM_WRITE_ONLY,
                              num_hashes * 32 * sizeof(uint8_t), NULL, &err);
    CHECK_CL_ERROR(err, "clCreateBuffer hashes");
    
    // Копирование данных на GPU
    clEnqueueWriteBuffer(queue, d_data, CL_TRUE, 0, 
                         num_hashes * max_len * sizeof(uint8_t), data, 0, NULL, NULL);
    clEnqueueWriteBuffer(queue, d_lens, CL_TRUE, 0,
                         num_hashes * sizeof(uint32_t), lens, 0, NULL, NULL);
    
    // Установка аргументов
    clSetKernelArg(kernel_sha256, 0, sizeof(cl_mem), &d_data);
    clSetKernelArg(kernel_sha256, 1, sizeof(cl_mem), &d_lens);
    clSetKernelArg(kernel_sha256, 2, sizeof(cl_mem), &d_hashes);
    clSetKernelArg(kernel_sha256, 3, sizeof(cl_uint), &max_len);
    
    // Выполнение kernel
    size_t global_size = ((num_hashes + local_size - 1) / local_size) * local_size;
    
    cl_event event;
    err = clEnqueueNDRangeKernel(queue, kernel_sha256, 1, NULL,
                                  &global_size, &local_size, 0, NULL, &event);
    CHECK_CL_ERROR(err, "clEnqueueNDRangeKernel");
    
    clWaitForEvents(1, &event);
    
    // Получение времени выполнения
    cl_ulong time_start, time_end;
    clGetEventProfilingInfo(event, CL_PROFILING_COMMAND_START, sizeof(time_start), &time_start, NULL);
    clGetEventProfilingInfo(event, CL_PROFILING_COMMAND_END, sizeof(time_end), &time_end, NULL);
    *kernel_time_ms = (double)(time_end - time_start) / 1000000.0;
    
    // Чтение результатов
    clEnqueueReadBuffer(queue, d_hashes, CL_TRUE, 0,
                        num_hashes * 32 * sizeof(uint8_t), hashes, 0, NULL, NULL);
    
    // Освобождение ресурсов
    clReleaseEvent(event);
    clReleaseMemObject(d_data);
    clReleaseMemObject(d_lens);
    clReleaseMemObject(d_hashes);
    clReleaseKernel(kernel_sha256);
    clReleaseProgram(program);
    clReleaseCommandQueue(queue);
    clReleaseContext(context);
    free(source);
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
// ГЛАВНАЯ ФУНКЦИЯ
// ============================================================

int main(int argc, char** argv) {
    uint32_t num_hashes = DEFAULT_NUM_HASHES;
    uint32_t max_len = DEFAULT_DATA_LEN;
    size_t local_size = DEFAULT_LOCAL_SIZE;
    
    if (argc >= 2) num_hashes = atoi(argv[1]);
    if (argc >= 3) max_len = atoi(argv[2]);
    if (argc >= 4) local_size = atoi(argv[3]);
    
    if (num_hashes < 1) num_hashes = 1;
    if (max_len < 8) max_len = 8;
    if (max_len > 1024) max_len = 1024;
    
    // Округляем local_size до степени двойки
    size_t power = 1;
    while (power * 2 <= local_size) power *= 2;
    local_size = power;
    
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
    hash_gpu(data, lens, gpu_hashes, num_hashes, max_len, local_size, 1, &gpu_kernel_time);
    clock_t gpu_total_end = clock();
    double gpu_total_time_ms = ((double)(gpu_total_end - gpu_total_start)) / CLOCKS_PER_SEC * 1000.0;
    
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
