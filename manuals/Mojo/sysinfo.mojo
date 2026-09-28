# sysinfo.mojo — Сбор информации о системе на Mojo
# Демонстрирует: sys.info, gpu.host, C FFI (external_call)

from std.sys.info import (
    os_is_linux, os_is_macos, os_is_windows,
    _current_cpu, _triple_attr,
    has_sse4, has_avx, has_avx2, has_avx512f,
    is_64bit
)
from std.sys import num_physical_cores, num_logical_cores
from std.ffi import external_call, c_long


# ── Вспомогательная функция: объём памяти в человекочитаемом виде ──
def format_bytes(bytes: Int) -> String:
    """Преобразует байты в строку вида '16.0 GB'."""
    var value = Float64(bytes)
    if value >= 1024.0 ** 3:
        return t"{round(value / (1024.0 ** 3), 2)} GB"
    elif value >= 1024.0 ** 2:
        return t"{round(value / (1024.0 ** 2), 2)} MB"
    else:
        return t"{round(value / 1024.0, 2)} KB"


# ── Секция 1: Операционная система и архитектура ──
def print_os_info():
    print("=" * 50)
    print("  ОПЕРАЦИОННАЯ СИСТЕМА И АРХИТЕКТУРА")
    print("=" * 50)

    var os_name = "Unknown"
    if os_is_linux():
        os_name = "Linux"
    elif os_is_macos():
        os_name = "macOS"
    elif os_is_windows():
        os_name = "Windows"

    var arch = String(_triple_attr())

    print(t"  ОС          : {os_name}")
    print(t"  Архитектура : {arch}")
    print(t"  64-битная   : {is_64bit()}")
    print()


# ── Секция 2: Информация о процессоре ──
def print_cpu_info():
    print("=" * 50)
    print("  ПРОЦЕССОР (CPU)")
    print("=" * 50)

    let cpu_model = String(_current_cpu())
    let phys_cores = num_physical_cores()
    let logic_cores = num_logical_cores()

    print(t"  Модель              : {cpu_model}")
    print(t"  Физических ядер     : {phys_cores}")
    print(t"  Логических потоков  : {logic_cores}")

    var features = String("")
    if has_sse4():
        features += " SSE4"
    if has_avx():
        features += " AVX"
    if has_avx2():
        features += " AVX2"
    if has_avx512f():
        features += " AVX-512"

    if len(features) > 0:
        print(t"  Наборы инструкций   :{features}")
    else:
        print("  Наборы инструкций   : не определены")
    print()


# ── Секция 3: Информация о видеокарте (GPU) ──
def print_gpu_info():
    print("=" * 50)
    print("  ВИДЕОКАРТА (GPU)")
    print("=" * 50)

    try:
        from gpu.host import DeviceContext, DeviceAttribute
        var ctx = DeviceContext()

        print(t"  Устройство          : {ctx.name()}")
        print(t"  API                 : {ctx.api()}")

        let (free_mem, total_mem) = ctx.get_memory_info()
        print(t"  Видеопамять (свободно): {format_bytes(Int(free_mem))}")
        print(t"  Видеопамять (всего)   : {format_bytes(Int(total_mem))}")

        let clock = ctx.get_attribute(DeviceAttribute.CLOCK_RATE)
        print(t"  Тактовая частота      : {clock} MHz")

        let max_blocks = ctx.get_attribute(DeviceAttribute.MAX_BLOCKS_PER_MULTIPROCESSOR)
        print(t"  Макс. блоков/SM      : {max_blocks}")

    except:
        print("  GPU не обнаружен или драйверы не поддерживаются.")
        print("  Mojo поддерживает NVIDIA, AMD и Apple Silicon GPU.")
    print()


# ── Секция 4: Оперативная память через C FFI ──
def print_ram_info():
    print("=" * 50)
    print("  ОПЕРАТИВНАЯ ПАМЯТЬ (RAM)")
    print("=" * 50)

    var phys_pages: c_long = 0
    var page_size: c_long = 0

    try:
        if os_is_linux():
            phys_pages = external_call["sysconf", c_long](c_long(85))
            page_size  = external_call["sysconf", c_long](c_long(30))
        elif os_is_macos():
            phys_pages = external_call["sysconf", c_long](c_long(200))
            page_size  = external_call["sysconf", c_long](c_long(29))

        if phys_pages > 0 and page_size > 0:
            let total_ram = Int(phys_pages) * Int(page_size)
            print(t"  Всего RAM   : {format_bytes(total_ram)}")

            if os_is_linux():
                try:
                    with open("/proc/meminfo", "r") as f:
                        for line in f:
                            if line.startswith("MemAvailable:"):
                                var parts = line.split()
                                if len(parts) >= 2:
                                    let free_kb = Int(parts[1])
                                    print(t"  Свободно    : {format_bytes(free_kb * 1024)}")
                                break
                except:
                    print("  Свободно    : (не удалось прочитать /proc/meminfo)")
        else:
            print("  Не удалось определить объём RAM через sysconf.")
    except:
        print("  Ошибка при запросе информации о RAM.")
    print()


# ── Точка входа ──
def main():
    print()
    print("╔" + "═" * 48 + "╗")
    print("║       СИСТЕМНАЯ ИНФОРМАЦИЯ (Mojo)             ║")
    print("╚" + "═" * 48 + "╝")
    print()

    print_os_info()
    print_cpu_info()
    print_gpu_info()
    print_ram_info()

    print("=" * 50)
    print("  Готово.")
    print("=" * 50)


if __name__ == "__main__":
    main()
