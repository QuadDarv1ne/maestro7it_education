/*
 * Отладочная версия sieve для тестирования GPU kernel
 * Компиляция: gcc -o sieve_debug sieve_debug.c -lOpenCL -lm -O0 -g
 * Запуск: sieve_debug.exe 1000
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

#ifdef __APPLE__
#include <OpenCL/opencl.h>
#else
#include <CL/cl.h>
#endif

#define CHECK_CL_ERROR(err, msg) \
    if (err != CL_SUCCESS) { \
        fprintf(stderr, "OpenCL Error %d: %s\n", err, msg); \
        return -1; \
    }

const char* get_embedded_kernel() {
    return
    "__kernel void init_array(__global uchar* is_prime, const uint limit) {\n"
    "    uint gid = get_global_id(0);\n"
    "    if (gid > limit) return;\n"
    "    is_prime[gid] = (gid >= 2) ? 1 : 0;\n"
    "}\n"
    "\n"
    "__kernel void sieve_mark(__global uchar* is_prime, uint limit, uint p) {\n"
    "    uint gid = get_global_id(0);\n"
    "    uint start = p * p;\n"
    "    if (start > limit) return;\n"
    "    uint idx = start + p * gid;\n"
    "    if (idx <= limit) is_prime[idx] = 0;\n"
    "}\n";
}

int main(int argc, char** argv) {
    unsigned long limit = 1000;
    if (argc > 1) limit = atol(argv[1]);
    
    printf("=== Sieve Debug Test ===\n");
    printf("N = %lu\n\n", limit);
    
    // CPU версия
    unsigned char* cpu_is_prime = (unsigned char*)malloc(limit + 1);
    memset(cpu_is_prime, 1, limit + 1);
    cpu_is_prime[0] = cpu_is_prime[1] = 0;
    
    for (unsigned long p = 2; p * p <= limit; p++) {
        if (cpu_is_prime[p]) {
            for (unsigned long i = p * p; i <= limit; i += p)
                cpu_is_prime[i] = 0;
        }
    }
    
    unsigned long cpu_count = 0;
    for (unsigned long i = 2; i <= limit; i++)
        if (cpu_is_prime[i]) cpu_count++;
    
    printf("CPU: найдено %lu простых чисел\n", cpu_count);
    
    // GPU версия
    cl_int err;
    cl_platform_id platform;
    cl_device_id device;
    cl_context context;
    cl_command_queue queue;
    cl_program program;
    cl_kernel kernel_init, kernel_mark;
    cl_mem d_is_prime;
    
    err = clGetPlatformIDs(1, &platform, NULL);
    CHECK_CL_ERROR(err, "clGetPlatformIDs");
    
    err = clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 1, &device, NULL);
    if (err != CL_SUCCESS) {
        printf("GPU не найден, пробуем CPU...\n");
        err = clGetDeviceIDs(platform, CL_DEVICE_TYPE_CPU, 1, &device, NULL);
        CHECK_CL_ERROR(err, "clGetDeviceIDs CPU");
    }
    
    char device_name[128];
    clGetDeviceInfo(device, CL_DEVICE_NAME, sizeof(device_name), device_name, NULL);
    printf("Устройство: %s\n\n", device_name);
    
    context = clCreateContext(NULL, 1, &device, NULL, NULL, &err);
    CHECK_CL_ERROR(err, "clCreateContext");
    
    queue = clCreateCommandQueue(context, device, 0, &err);
    CHECK_CL_ERROR(err, "clCreateCommandQueue");
    
    const char* kernel_source = get_embedded_kernel();
    size_t source_size = strlen(kernel_source);
    
    program = clCreateProgramWithSource(context, 1, &kernel_source, &source_size, &err);
    CHECK_CL_ERROR(err, "clCreateProgramWithSource");
    
    err = clBuildProgram(program, 1, &device, "-cl-std=CL1.2", NULL, NULL);
    if (err != CL_SUCCESS) {
        char build_log[2048];
        clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, sizeof(build_log), build_log, NULL);
        printf("Build log:\n%s\n", build_log);
        return -1;
    }
    
    kernel_init = clCreateKernel(program, "init_array", &err);
    CHECK_CL_ERROR(err, "clCreateKernel init_array");
    
    kernel_mark = clCreateKernel(program, "sieve_mark", &err);
    CHECK_CL_ERROR(err, "clCreateKernel sieve_mark");
    
    d_is_prime = clCreateBuffer(context, CL_MEM_READ_WRITE | CL_MEM_ALLOC_HOST_PTR, limit + 1, NULL, &err);
    CHECK_CL_ERROR(err, "clCreateBuffer");
    
    // Инициализация
    err = clSetKernelArg(kernel_init, 0, sizeof(cl_mem), &d_is_prime);
    CHECK_CL_ERROR(err, "clSetKernelArg init 0");
    cl_uint limit_uint = (cl_uint)limit;
    err = clSetKernelArg(kernel_init, 1, sizeof(cl_uint), &limit_uint);
    CHECK_CL_ERROR(err, "clSetKernelArg init 1");
    
    size_t global_size = ((limit + 255) / 256) * 256;
    err = clEnqueueNDRangeKernel(queue, kernel_init, 1, NULL, &global_size, NULL, 0, NULL, NULL);
    CHECK_CL_ERROR(err, "clEnqueueNDRangeKernel init");
    clFinish(queue);
    
    // Основной цикл
    unsigned long sqrt_limit = (unsigned long)sqrt((double)limit);
    
    for (unsigned long p = 2; p <= sqrt_limit; p++) {
        // Читаем текущее значение
        unsigned char p_val = 1;
        err = clEnqueueReadBuffer(queue, d_is_prime, CL_TRUE, p, 1, &p_val, 0, NULL, NULL);
        CHECK_CL_ERROR(err, "clEnqueueReadBuffer");
        
        if (p_val) {
            cl_uint p_uint = (cl_uint)p;
            err = clSetKernelArg(kernel_mark, 0, sizeof(cl_mem), &d_is_prime);
            CHECK_CL_ERROR(err, "clSetKernelArg mark 0");
            err = clSetKernelArg(kernel_mark, 1, sizeof(cl_uint), &limit_uint);
            CHECK_CL_ERROR(err, "clSetKernelArg mark 1");
            err = clSetKernelArg(kernel_mark, 2, sizeof(cl_uint), &p_uint);
            CHECK_CL_ERROR(err, "clSetKernelArg mark 2");
            
            unsigned long start = p * p;
            unsigned long num_multiples = (limit - start) / p + 1;
            size_t mark_global_size = ((num_multiples + 255) / 256) * 256;
            if (mark_global_size < 256) mark_global_size = 256;
            
            err = clEnqueueNDRangeKernel(queue, kernel_mark, 1, NULL, &mark_global_size, NULL, 0, NULL, NULL);
            CHECK_CL_ERROR(err, "clEnqueueNDRangeKernel mark");
            clFinish(queue);
        }
    }
    
    // Чтение результата
    unsigned char* gpu_is_prime = (unsigned char*)malloc(limit + 1);
    err = clEnqueueReadBuffer(queue, d_is_prime, CL_TRUE, 0, limit + 1, gpu_is_prime, 0, NULL, NULL);
    CHECK_CL_ERROR(err, "clEnqueueReadBuffer final");
    
    unsigned long gpu_count = 0;
    for (unsigned long i = 2; i <= limit; i++)
        if (gpu_is_prime[i]) gpu_count++;
    
    printf("GPU: найдено %lu простых чисел\n", gpu_count);
    
    // Сравнение
    int match = 1;
    for (unsigned long i = 0; i <= limit; i++) {
        if (cpu_is_prime[i] != gpu_is_prime[i]) {
            printf("MISMATCH at %lu: CPU=%d GPU=%d\n", i, cpu_is_prime[i], gpu_is_prime[i]);
            match = 0;
            if (i < 20) {
                // Показать первые 20 значений для отладки
            }
        }
    }
    
    if (match) {
        printf("\n✅ CPU и GPU результаты СОВПАДАЮТ!\n");
    } else {
        printf("\n❌ CPU и GPU результаты РАЗЛИЧАЮТСЯ!\n");
    }
    
    // Показать первые простые числа
    printf("\nПервые простые числа: ");
    int count = 0;
    for (unsigned long i = 2; i <= limit && count < 25; i++) {
        if (gpu_is_prime[i]) {
            printf("%lu ", i);
            count++;
        }
    }
    printf("\n");
    
    // Очистка
    free(cpu_is_prime);
    free(gpu_is_prime);
    clReleaseMemObject(d_is_prime);
    clReleaseKernel(kernel_init);
    clReleaseKernel(kernel_mark);
    clReleaseProgram(program);
    clReleaseCommandQueue(queue);
    clReleaseContext(context);
    
    return match ? 0 : 1;
}
