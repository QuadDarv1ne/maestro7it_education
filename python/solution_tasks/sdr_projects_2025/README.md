# Управление радиочастотами в Python

## Радиочастоты и их диапазоны

Радиочастоты делятся на диапазоны, которые регулируются международными соглашениями (например, `ITU`).

**Вот основные:**

Диапазон    Частоты          Применение
НЧ (LF)     30–300 кГц       Радионавигация, AM-радио
СЧ (MF)     300–3000 кГц     AM-радио, авиационная связь
ВЧ (HF)     3–30 МГц         Коротковолновое радио, морская связь
ОВЧ (VHF)   30–300 МГц       FM-радио (88–108 МГц), телевидение
УВЧ (UHF)   300 МГц – 3ГГц   Wi-Fi, Bluetooth, мобильная связь (GSM, LTE)
СВЧ (SHF)   3–30 ГГц         Wi-Fi (5 ГГц), радары, спутники
КВЧ (EHF)   30–300 ГГц       Радиоастрономия, военные системы

## Управление радиочастотами в Python

Для работы с радиочастотами в Python используются `SDR` (`Software-Defined Radio`) устройства, такие как `RTL-SDR`, `HackRF`, `USRP` или `LimeSDR`

1. `Использование RTL-SDR (дешёвый вариант)`

`RTL-SDR` работает в диапазоне 24–1766 МГц (зависит от модели).

**Пример программы для сканирования FM-радио (88–108 МГц):**

```python
import numpy as np
import matplotlib.pyplot as plt
from rtlsdr import RtlSdr

sdr = RtlSdr()

# Настройка параметров
sdr.sample_rate = 2.4e6  # Частота дискретизации
sdr.center_freq = 100e6   # Центральная частота (например, 100 МГц для FM)
sdr.gain = 'auto'         # Автоматическая настройка усиления

# Чтение данных
samples = sdr.read_samples(256 * 1024)

# Построение спектра
plt.psd(samples, NFFT=1024, Fs=sdr.sample_rate / 1e6, Fc=sdr.center_freq / 1e6)
plt.xlabel('Частота (МГц)')
plt.ylabel('Мощность (дБ)')
plt.show()

sdr.close()
```

**Установка библиотеки:**

```bash
pip install pyrtlsdr matplotlib numpy
```

2. `Использование HackRF (более широкий диапазон)`

`HackRF` работает в 1 МГц – 6 ГГц и позволяет не только принимать, но и передавать сигналы.

**Пример передачи синусоидального сигнала:**

```python
import hackrf
import numpy as np

hackrf = hackrf.HackRF()

# Настройка параметров
hackrf.sample_rate = 2e6
hackrf.center_freq = 433e6  # Частота 433 МГц (ISM-диапазон)
hackrf.txvga_gain = 30      # Усиление передатчика

# Генерация сигнала
t = np.linspace(0, 1, hackrf.sample_rate, dtype=np.complex64)
samples = np.exp(1j * 2 * np.pi * 100e3 * t)  # Синусоида 100 кГц

# Передача
hackrf.transmit(samples)

hackrf.close()
```

**Установка библиотеки:**

```bash
pip install hackrf
```

3. `USRP (профессиональное оборудование)`

Для `USRP (от Ettus Research)` можно использовать `UHD (Universal Hardware Driver)` и `GNU Radio`

**Пример приёма сигнала:**

```python
import uhd
import numpy as np

usrp = uhd.usrp.MultiUSRP()

# Настройка
usrp.set_rx_rate(1e6)       # Частота дискретизации 1 МГц
usrp.set_rx_freq(uhd.types.TuneRequest(915e6))  # Частота 915 МГц
usrp.set_rx_gain(30)        # Усиление

# Приём данных
num_samples = 10000
samples = usrp.recv_num_samps(num_samples, 915e6, 1e6, [0], 0)
print("Получено", len(samples), "сэмплов")
```

## Важные моменты

**Законность:** В большинстве стран требуется лицензия на передачу в определённых диапазонах (`например, GSM, авиационные частоты`).

**Оборудование:**

- `RTL-SDR` – только приём, дёшево (`~$20`).
- `HackRF` – приём и передача, дороже (`~$300`).
- `USRP` – профессиональное решение (`от $1000`).

**Библиотеки:**

- `Для RTL-SDR`: `pyrtlsdr`, `librtlsdr`
- `Для HackRF`: `hackrf`, `soapy_power`
- `Для USRP`: `pyuhd`, `gnuradio`

## Инструкция по запуску

1. **Установите зависимости:**

```bash
pip install numpy matplotlib pyrtlsdr jax requests hackrf scipy
```

2. **Для приема FM:**

```bash
python fm_radio_monitor.py --frequency 100.1e6 --gain auto
```

3. **Для передачи ППР:**

```bash
python ppr_signal_generator.py --frequency 146.5e6 --tx_gain 30
```

```textline
✅ JIT-компилятор

В Python 3.13 добавлен экспериментальный JIT-компилятор с многоуровневой оптимизацией байт-кода.
Для активации требуется флаг `--enable-experimental-jit 2`.

✅ Отключение GIL

Экспериментальная сборка Python `--without-gil` позволяет отключать `Global Interpreter Lock`, что улучшает многопоточную производительность. Пока не рекомендуется для продакшена. 
```

```textline
sdr_projects_2025/  
├── fm_radio_monitor.py       # Прием и визуализация FM  
├── ppr_signal_generator.py   # Генерация ППР-сигналов  
├── config/                   # Конфиги  
└── utils/                    # Дополнительные модули  
```

---

💼 **Автор:** Дуплей Максим Игоревич

📲 **Telegram:** @quadd4rv1n7

📅 **Дата:** 09.05.2025

▶️ **Версия 1.0**

```textline
※ Предложения по сотрудничеству можете присылать на почту ※
📧 maksimqwe42@mail.ru
```
