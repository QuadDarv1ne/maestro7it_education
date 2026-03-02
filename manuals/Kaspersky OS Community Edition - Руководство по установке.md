# Kaspersky OS Community Edition: Руководство по установке

> **Важно:** Kaspersky OS — это микроядерная операционная система для встраиваемых решений и IoT, а не десктопная ОС для общего пользования.
>
> **Целевая аудитория:** Разработчики встраиваемых систем, исследователи безопасности, студенты.

---

##📋 О проекте

**Kaspersky OS Community Edition (CE)** — бесплатная версия для разработчиков, включающая:

- **SDK** с инструментами сборки и отладки
- **Эмулятор QEMU** для тестирования
- **Примеры кода** и документацию
- **Поддержку архитектур** x86_64, ARM (Raspberry Pi 4B, Radxa ROCK 3A)

**Лицензия:** Только для обучения, исследований и некоммерческого использования.

**Преимущества:**
- Высокая безопасность за счёт микроядра
- Изоляция процессов на уровне ОС
- Поддержка формальных методов верификации

---

##🔧 Системные требования

| Компонент | Требование |
|-----------|-----------|
| ОС хоста | Linux (Ubuntu 20.04/22.04, Debian 10+) |
| Архитектура | x86_64 |
| ОЗУ | ≥ 4 ГБ (рекомендуется 8 ГБ) |
| Место на диске | ≥ 5 ГБ (с учётом образов) |
| Права | Доступ к `sudo` |
| Виртуализация | VT-x/AMD-V (для QEMU) |

> **Для Windows:** Используйте WSL2 с Ubuntu или виртуальную машину VirtualBox/VMware.
>
> **Проверка виртуализации:** `grep -E "(vmx|svm)" /proc/cpuinfo`

---

## 📥 Установка (QEMU / эмуляция)

### 1. Подготовка системы

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка необходимых пакетов
sudo apt install -y curl wget gnupg qemu-system-x86 qemu-utils

# Проверка виртуализации
if grep -qE "(vmx|svm)" /proc/cpuinfo; then
  echo "✅ Виртуализация поддерживается"
else
  echo "❌ Виртуализация не поддерживается"
  exit 1
fi
```

### 2. Скачивание пакета

1. Перейдите на [официальную страницу загрузки](https://os.kaspersky.com/development/)
2. Зарегистрируйтесь (бесплатно)
3. Скачайте `.deb`-пакет для вашей архитектуры

### 3. Установка

```bash
# Установка пакета
sudo dpkg -i kasperskyos-community-edition-*.deb

# Установка недостающих зависимостей
sudo apt --fix-broken install -y

# Проверка установки
if [ -d "/opt/KasperskyOS-Community-Edition"* ]; then
  echo "✅ Установка завершена успешно"
else
  echo "❌ Ошибка установки"
  exit 1
fi
```

**Пакет установится в:** `/opt/KasperskyOS-Community-Edition-<platform>-<version>/`

### 4. Настройка окружения

```bash
# Временная активация (на текущую сессию)
source /opt/KasperskyOS-Community-Edition-*/common/set_env.sh

# ИЛИ постоянная активация (добавить в ~/.bashrc)
echo '# Kaspersky OS CE' >> ~/.bashrc
echo 'source /opt/KasperskyOS-Community-Edition-*/common/set_env.sh' >> ~/.bashrc
source ~/.bashrc
```

### 5. Проверка установки

```bash
# Проверка переменных окружения
echo "KOSCEDIR: $KOSCEDIR"  # Путь к SDK
echo "KOSCEVER: $KOSCEVER"  # Версия

# Проверка инструментов
if command -v kos-build &> /dev/null; then
  echo "✅ kos-build: $(kos-build --version)"
else
  echo "❌ kos-build не найден"
fi

if command -v kos-run &> /dev/null; then
  echo "✅ kos-run доступен"
else
  echo "❌ kos-run не найден"
fi
```

## Первый запуск примера

```bash
# Переход к примеру "hello"
cd $KOSCEDIR/examples/hello

# Просмотр структуры проекта
ls -la

cat Makefile  # Изучение сборочного файла

# Сборка проекта
kos-build

# Проверка результата сборки
if [ -f "hello.img" ]; then
  echo "✅ Образ создан успешно"
  ls -lh hello.img
else
  echo "❌ Ошибка сборки"
  exit 1
fi

# Запуск в эмуляторе
kos-run

# Ожидаемый вывод:
# Hello, KasperskyOS Community Edition!
```

##💾 Установка на Raspberry Pi 4B

### Подготовка

1. **Скачайте образ** `*.img` для `Raspberry Pi` с [официального сайта](https://os.kaspersky.com/development/)
2. **Определите устройство microSD:**
```bash
lsblk  # Найдите вашу SD-карту (например, /dev/sdb)
```

### Запись образа

```bash
#⚠ ВНИМАНИЕ: Убедитесь в правильности пути!
SD_CARD=/dev/sdX  # Замените на ваше устройство

# Запись образа
sudo dd if=kos-ce-rpi4.img of=$SD_CARD bs=4M status=progress conv=fsync

# Синхронизация
sync

echo "✅ Образ записан на SD-карту"
```

### Первый запуск

1. Вставьте карту в `Raspberry Pi 4B`
2. Подключите HDMI-монитор и клавиатуру
3. Включите питание
4. Подождите загрузки системы

### Настройка подключения

```bash
# Подключение через UART (через USB-UART адаптер)
sudo screen /dev/ttyUSB0 115200

# ИЛИ подключение через SSH (если настроена сеть)
ssh user@raspberry-pi-ip
```

> **Примечание:** Подробная настройка сети и пользователей описана в Developer Guide.

##🗑️ Удаление

```bash
# Удаление пакета
sudo apt remove --purge kasperskyos-community-edition-qemu -y

# Удаление конфигурации из .bashrc
sed -i '/KasperskyOS-Community-Edition/d' ~/.bashrc

# Удаление остаточных файлов
sudo rm -rf /opt/KasperskyOS-Community-Edition-*

echo "✅ Kaspersky OS CE полностью удалён"
```

## 📚 Полезные ресурсы

### 📖 Официальная документация

- **Полная документация:** https://support.kaspersky.com/help/KCE/
- **Руководство по началу работы:** https://support.kaspersky.com/kos-community-edition/
- **API Reference:** Входит в SDK

###💬ество

- **Форум разработчиков:** https://forum.kasperskyos.com/
- **GitHub репозитории:** Примеры от сообщества
- **Telegram/Slack:** Поиск по ключевым словам

###🤝 Партнёрство

- **Партнёрская программа:** https://os.kaspersky.com/partners
- **Коммерческие решения:** Для production-использования

### 📚 Дополнительные материалы

- **Книги по микроядрам:** "Microkernels: From Design to Implementation"
- **Безопасность встроенных систем:** Online-курсы
- **Formal Methods:** Tutorials и примеры

##⚠️ Ограничения Community Edition

### ❌ Ограничения использования

- **Не для коммерческого использования**
- **Без технической поддержки SLA**
- **Ограниченный набор драйверов**
- **Нет гарантий производительности**

###✅ Возможности

- **Полноценный SDK** для обучения
- **Доступ к исходным примерам**
- **Обновления безопасности**
- **Поддержка сообщества**
- **Эмуляция на x86_64**

### 🔄 Альтернативы для production

- **Commercial Edition** (с поддержкой)
- **Enterprise Solutions** (для бизнеса)
- **Партнёрские программы** Kaspersky

##🔍 Устранение неполадок

###⚠️ Частые ошибки и решения

#### 1. Команда не найдена
```bash
# Ошибка: "command not found: kos-build"

# Проверка активации окружения
echo $KOSCEDIR

# Если переменная пуста:
source /opt/KasperskyOS-Community-Edition-*/common/set_env.sh

# Проверка PATH
which kos-build
```

#### 2. Проблемы с QEMU
```bash
# Ошибка: QEMU не запускается

# Проверка виртуализации:
grep -E "(vmx|svm)" /proc/cpuinfo

# Если нет вывода:
# 1. Включите VT-x/AMD-V в BIOS
# 2. Для WSL2: wsl --set-version <distro> 2

# Проверка установки QEMU:
qemu-system-x86_64 --version
```

#### 3. Проблемы с зависимостями
```bash
# Ошибка: зависимости apt

# Исправление зависимостей:
sudo apt --fix-broken install -y

# Повторная установка:
sudo dpkg -i kasperskyos-community-edition-*.deb
```

#### 4. Ошибка сборки
```bash
# Проверка текущей директории
pwd
ls -la  # Должен быть Makefile

# Очистка и пересборка
kos-build clean
kos-build
```

### 📞 Каналы поддержки

- **Форма обратной связи:** https://os.kaspersky.com/contacts/
- **Форум разработчиков:** https://forum.kasperskyos.com/
- **Email поддержки:** community@kaspersky.com

**Последнее обновление:** 2026

---

> **💡 Совет:** Перед началом работы рекомендуется пройти официальный `Quick Start Guide`
