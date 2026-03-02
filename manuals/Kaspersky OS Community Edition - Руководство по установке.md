# Kaspersky OS Community Edition: Руководство по установке

> **Важно:** Kaspersky OS — это микроядерная операционная система для встраиваемых решений и IoT, а не десктопная ОС для общего пользования.

---

## 📋 О проекте

**Kaspersky OS Community Edition (CE)** — бесплатная версия для разработчиков, включающая:
- SDK с инструментами сборки и отладки
- Эмулятор QEMU для тестирования
- Примеры кода и документацию
- Поддержку архитектур x86_64, ARM (Raspberry Pi 4B, Radxa ROCK 3A)

**Лицензия:** Только для обучения, исследований и некоммерческого использования.

---

## 🔧 Системные требования

| Компонент | Требование |
|-----------|-----------|
| ОС хоста | Linux (Ubuntu 20.04/22.04, Debian 10+) |
| Архитектура | x86_64 |
| ОЗУ | ≥ 4 ГБ |
| Место на диске | ≥ 5 ГБ |
| Права | Доступ к `sudo` |

> Для Windows используйте WSL2 с Ubuntu или виртуальную машину.

---

## 📥 Установка (QEMU / эмуляция)

### 1. Подготовка системы
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget gnupg
```

2. Скачивание пакета
Перейдите на официальную страницу загрузки
Зарегистрируйтесь и скачайте .deb-пакет для QEMU
3. Установка
bash
12
Пакет установится в:
/opt/KasperskyOS-Community-Edition-<platform>-<version>/
4. Настройка окружения
bash
123456
# Временная активация (на текущую сессию)
source /opt/KasperskyOS-Community-Edition-*/common/set_env.sh

# ИЛИ постоянная активация (добавить в ~/.bashrc)
echo 'source /opt/KasperskyOS-Community-Edition-*/common/set_env.sh' >> ~/.bashrc
source ~/.bashrc
5. Проверка установки
bash
123456
# Проверка переменных
echo $KOSCEDIR  # Путь к SDK
echo $KOSCEVER  # Версия

# Проверка инструментов
kos-build --version
🚀 Первый запуск примера
bash
12345678
# Переход к примеру "hello"
cd $KOSCEDIR/examples/hello

# Сборка проекта
kos-build

# Запуск в эмуляторе
kos-run
💾 Установка на Raspberry Pi 4B
Скачайте образ *.img для Raspberry Pi с официального сайта
Запишите образ на microSD:
bash
1
sudo dd if=kos-ce-rpi4.img of=/dev/sdX bs=4M status=progress conv=fsync
Вставьте карту в Raspberry Pi и включите питание
Подключитесь через UART/SSH для настройки (см. Developer Guide)
🗑️ Удаление
bash
1
sudo apt remove --purge kasperskyos-community-edition-qemu
📚 Ресурсы

Документация
https://support.kaspersky.com/help/KCE/

Quick Start Guide
https://support.kaspersky.com/kos-community-edition/

Форум разработчиков
https://forum.kasperskyos.com/

Партнёрская программа
https://os.kaspersky.com/partners

⚠️ Ограничения Community Edition
❌ Не для коммерческого использования
❌ Без технической поддержки SLA
❌ Ограниченный набор драйверов
✅ Полноценный SDK для обучения
✅ Доступ к исходным примерам
✅ Обновления безопасности
🔍 Troubleshooting
bash
12345678
# Ошибка: "command not found: kos-build"
# Решение: активировать set_env.sh

# Ошибка: QEMU не запускается
# Решение: включить виртуализацию (VT-x/AMD-V) в BIOS

# Ошибка: зависимости apt
# Решение: sudo apt --fix-broken install
Поддержка: Вопросы по установке и разработке направляйте через форму на os.kaspersky.com или на форум разработчиков.

Последнее обновление: 2026