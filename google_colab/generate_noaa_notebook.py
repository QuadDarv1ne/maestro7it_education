import nbformat as nbf
import os

# Создаём новый ноутбук
nb = nbf.v4.new_notebook()

# Ячейка 1: Заголовок (Markdown)
nb["cells"].append(nbf.v4.new_markdown_cell("""
# 🛰️ Приём и декодирование изображений со спутников NOAA

Этот ноутбук позволяет:
1. Предсказать пролёты спутников NOAA
2. Записать радиосигнал во время пролёта (требуется RTL-SDR)
3. Декодировать сигнал в изображение (требуется SatDump)

> 💡 **Требования**:
> - RTL-SDR устройство
> - Установленный [SatDump](https://github.com/SatDump/SatDump)
> - Запуск **локально** (не в Colab!)
"""))

# Ячейка 2: Проверка среды
nb["cells"].append(nbf.v4.new_code_cell("""
import sys
import os

if 'google.colab' in sys.modules:
    print("❌ Этот ноутбук НЕ РАБОТАЕТ в Google Colab — требуется локальный запуск с RTL-SDR.")
    print("Пожалуйста, скачайте ноутбук и запустите его на своём компьютере.")
else:
    print("✅ Запуск в локальной среде — продолжаем.")
"""))

# Ячейка 3: Установка зависимостей
nb["cells"].append(nbf.v4.new_code_cell("""
import subprocess
import sys

def install_packages():
    packages = ["pyorbital", "ephem", "pyrtlsdr", "numpy"]
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir"] + packages)

try:
    import pyorbital, ephem, rtlsdr, numpy
    print("✅ Все Python-библиотеки уже установлены.")
except ImportError:
    print("📦 Установка недостающих библиотек...")
    install_packages()
    print("✅ Установка завершена.")
"""))

# Ячейка 4: Предсказание пролёта
nb["cells"].append(nbf.v4.new_code_cell("""
from pyorbital.orbital import Orbital
from datetime import datetime, timedelta

def get_next_pass(sat_name="NOAA 19", location=(55.75, 37.62, 144), hours=24):
    orb = Orbital(sat_name)
    now = datetime.utcnow()
    end_time = now + timedelta(hours=hours)
    current = now
    
    while current < end_time:
        az, el = orb.get_observer_look(current, location[1], location[0], location[2])
        if el > 10:
            start = current
            while el > 10 and current < end_time:
                current += timedelta(seconds=30)
                az, el = orb.get_observer_look(current, location[1], location[0], location[2])
            end = current
            duration = (end - start).seconds // 60
            return {
                'satellite': sat_name,
                'start': start,
                'end': end,
                'duration_min': duration,
                'frequency_mhz': 137.62  # NOAA 19
            }
        current += timedelta(minutes=1)
    return None

LOCATION = (55.75, 37.62, 144)  # Москва
next_pass = get_next_pass(location=LOCATION)

if next_pass:
    print(f"🛰️  Ближайший пролёт: {next_pass['satellite']}")
    print(f"⏰ Начало: {next_pass['start'].strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"⏱️  Длительность: {next_pass['duration_min']} минут")
else:
    print("❌ Пролётов не найдено в ближайшие 24 часа.")
"""))

# Ячейка 5: Запись сигнала
nb["cells"].append(nbf.v4.new_code_cell("""
import time
import numpy as np
import os
from rtlsdr import RtlSdr
from datetime import datetime

def record_pass(pass_info, output_dir="recordings"):
    os.makedirs(output_dir, exist_ok=True)
    
    now = datetime.utcnow()
    wait_sec = (pass_info['start'] - now).total_seconds()
    if wait_sec > 0:
        print(f"⏳ Ожидание начала пролёта... ({int(wait_sec)} сек)")
        time.sleep(wait_sec)
    
    sdr = RtlSdr()
    sdr.sample_rate = 2.4e6
    sdr.center_freq = pass_info['frequency_mhz'] * 1e6
    sdr.gain = 'auto'
    
    duration = (pass_info['end'] - pass_info['start']).seconds
    total_samples = int(sdr.sample_rate * duration)
    chunk = 256 * 1024
    
    filename = f"{output_dir}/{pass_info['satellite'].replace(' ', '_')}_{pass_info['start'].strftime('%Y%m%d_%H%M%S')}.cu8"
    print(f"📡 Запись сигнала... ({duration} сек)")
    
    with open(filename, 'wb') as f:
        collected = 0
        while collected < total_samples:
            samples = sdr.read_samples(min(chunk, total_samples - collected))
            np.array(samples.view(np.float32)).astype(np.int8).tofile(f)
            collected += len(samples)
            print(f"   Записано: {collected / sdr.sample_rate:.1f} / {duration} сек", end='\\r')
    
    sdr.close()
    print(f"\\n✅ Сигнал сохранён: {filename}")
    return filename

# Раскомментируйте, когда будете готовы записывать:
# if 'next_pass' in locals() and next_pass:
#     iq_file = record_pass(next_pass)
"""))

# Ячейка 6: Декодирование через SatDump
nb["cells"].append(nbf.v4.new_code_cell("""
import subprocess
import os

def decode_with_satdump(iq_file, satellite="NOAA-19"):
    base = os.path.splitext(iq_file)[0]
    cmd = [
        "satdump", "generic",
        "--input_file", iq_file,
        "--output_file", base,
        "--satellite", satellite,
        "--baseband_type", "iq",
        "--baseband_format", "cu8"
    ]
    
    print("🔄 Запуск SatDump...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            png_files = [f for f in os.listdir('.') if f.startswith(os.path.basename(base)) and f.endswith('.png')]
            if png_files:
                print("✅ Декодирование успешно!")
                for f in png_files:
                    print(f"  - {f}")
                return png_files
        else:
            print("❌ Ошибка SatDump:", result.stderr)
    except FileNotFoundError:
        print("❌ SatDump не найден. Установите его: https://github.com/SatDump/SatDump")
    except subprocess.TimeoutExpired:
        print("⚠️  Декодирование превысило лимит времени (5 мин).")
    return []

# Пример:
# decoded_images = decode_with_satdump("recordings/NOAA_19_20251028_190145.cu8")
"""))

# Ячейка 7: Инструкция
nb["cells"].append(nbf.v4.new_markdown_cell("""
## 📌 Инструкция по использованию

1. **Установите SatDump**: https://github.com/SatDump/SatDump  
2. **Подключите RTL-SDR** к компьютеру.  
3. **Запустите ноутбук локально** (не в облаке!).  
4. Раскомментируйте ячейку записи и запустите её **за 1–2 минуты до пролёта**.  
5. После записи — запустите декодирование.

## 📡 Частоты NOAA
- NOAA 15: 137.620 MHz  
- NOAA 18: 137.9125 MHz  
- NOAA 19: 137.100 MHz  

## 🌐 Полезные ресурсы
- [N2YO.com](https://www.n2yo.com) — отслеживание в реальном времени  
- [SatNOGS](https://satnogs.org) — сеть приёмных станций  
- [RTL-SDR Blog Guide](https://www.rtl-sdr.com/rtl-sdr-tutorial-receiving-noaa-weather-satellite-images/) — подробное руководство
"""))

# Сохраняем в файл
output_file = "NOAA_Satellite_Reception.ipynb"
with open(output_file, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"✅ Ноутбук успешно создан: {os.path.abspath(output_file)}")