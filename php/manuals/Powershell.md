# 🪟 Полный мануал по PowerShell: Установка, Настройка и Использование

## 📋 Содержание

1. [Введение в PowerShell](#введение-в-powershell)
2. [Системные требования](#системные-требования)
3. [Установка PowerShell](#установка-powershell)
4. [Базовая настройка](#базовая-настройка)
5. [Основы PowerShell](#основы-powershell)
6. [Конфигурация PowerShell](#конфигурация-powershell)
7. [Управление модулями](#управление-модулями)
8. [Основные команды и cmdlets](#основные-команды-и-cmdlets)
9. [Работа с объектами и переменными](#работа-с-объектами-и-переменными)
10. [Скрипты и функции](#скрипты-и-функции)
11. [Практические примеры](#практические-примеры)
12. [Лучшие практики](#лучшие-практики)

## Введение в PowerShell

**PowerShell** — это мощная среда задач и конфигурации, разработанная Microsoft. Это командная строка и скриптовый язык, ориентированный на задачи автоматизации и управление конфигурациями.

`PowerShell` работает на основе объектов, а не текста, что делает его особенно мощным для автоматизации систем.

**Основные особенности PowerShell:**

- Объектно-ориентированная командная строка
- Поддержка скриптов и функций
- Интеграция с .NET Framework
- Поддержка удаленного управления
- Rich cmdlets (command-lets)
- Поддержка модулей и расширений
- Совместимость с существующими командами Windows

## Системные требования

### Минимальные требования:

- **Операционная система:** Windows 7 SP1+, Windows Server 2008 R2+, macOS 10.13+, Linux (различные дистрибутивы)
- **Процессор:** 1 ГГц или быстрее
- **Память:** 512 МБ RAM (рекомендуется 1 ГБ+)
- **Место на диске:** 100 МБ свободного места
- **.NET Framework:** 4.6.1+ для Windows PowerShell 5.1

### Рекомендуемые требования:

- **Операционная система:** Windows 10+, Windows Server 2019+, Ubuntu 18.04+, macOS 11+
- **Процессор:** Multi-core, 64-бит
- **Память:** 4 ГБ+ RAM
- **Место на диске:** 500 МБ+ свободного места
- **.NET Framework/Core:** 4.8+ или .NET Core 3.1+ для PowerShell 7+

### Поддерживаемые версии PowerShell:

- **PowerShell 7.4** (актуальная стабильная)
- **PowerShell 7.3** (поддерживается)
- **PowerShell 5.1** (встроенная в Windows)

## Установка PowerShell

### Метод №1: Установка PowerShell 7 (рекомендуется)

#### На Windows (с помощью MSI):

```powershell
# Скачайте последнюю версию с GitHub
# https://github.com/PowerShell/PowerShell/releases/latest
# Или используйте winget (Windows 10/11)
winget install --id Microsoft.Powershell --source winget

# Или используйте Chocolatey
choco install powershell-core

# Или используйте Scoop
scoop install pwsh
```

#### На Windows (с помощью установщика):

```powershell
# Установка через PowerShell (требует прав администратора)
irm https://aka.ms/install-powershell.ps1 -OutFile - | iex
```

### Метод №2: Установка на Linux

#### Ubuntu/Debian:

```bash
# Установка через apt
curl -sS https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo add-apt-repository https://packages.microsoft.com/repos/microsoft-debian-$(lsb_release -cs)-prod
sudo apt update
sudo apt install -y powershell
```

#### CentOS/RHEL/Fedora:

```bash
# Установка через RPM
curl -sS https://packages.microsoft.com/config/rhel/7/prod.repo | sudo tee /etc/yum.repos.d/microsoft.repo
sudo dnf install powershell
```

### Метод №3: Установка на macOS

#### С помощью Homebrew:

```bash
# Установка через Homebrew
brew install --cask powershell

# Запуск PowerShell
pwsh
```

#### С помощью установщика:

1. Скачайте PKG установщик с GitHub
2. Запустите установщик как администратор
3. Следуйте инструкциям установщика

## Базовая настройка

### Запуск PowerShell:

- **PowerShell 5.1:** Ищите "Windows PowerShell" в меню Start
- **PowerShell 7+:** Ищите "PowerShell 7" или "pwsh" в меню Start

### Проверка установки:

```powershell
# Проверка версии PowerShell
$PSVersionTable

# Или конкретно:
$PSVersionTable.PSVersion

# Проверка установленных модулей
Get-Module -ListAvailable
```

### Настройка профиля PowerShell:

```powershell
# Проверка пути к профилю
$PROFILE

# Создание профиля (если не существует)
if (!(Test-Path -Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force
}

# Открытие профиля для редактирования
notepad $PROFILE
```

**Пример содержимого профиля:**

```powershell
# PowerShell Profile
Write-Host "Добро пожаловать в PowerShell!" -ForegroundColor Green

# Псевдонимы
Set-Alias ll Get-ChildItem
Set-Alias grep Select-String

# Функции
function which($name) { Get-Command $name | Select-Object -ExpandProperty Definition }

# Настройки
Set-Location ~
Import-Module posh-git -ErrorAction SilentlyContinue
```

## Основы PowerShell

### Основные концепции:

- **Cmdlets** - команды PowerShell в формате Verb-Noun (Get-Process, Set-Location)
- **Пайплайн** - передача объектов между командами (|)
- **Объекты** - PowerShell работает с объектами, а не с текстом
- **Проводник (PowerShell ISE)** - графическая среда для разработки скриптов

### Основные команды:

```powershell
# Помощь
Get-Help Get-Process
Get-Help Get-Process -Detailed
Get-Help Get-Process -Examples

# Навигация
Get-Location          # pwd
Set-Location C:\      # cd
Push-Location         # pushd
Pop-Location          # popd

# Файловая система
Get-ChildItem         # ls/dir
Copy-Item             # cp
Move-Item             # mv
Remove-Item           # rm
New-Item              # создание файлов/директорий

# Процессы
Get-Process
Stop-Process -Name notepad
Start-Process notepad

# Сервисы
Get-Service
Restart-Service Spooler
```

## Конфигурация PowerShell

### Execution Policy (политика выполнения скриптов):

```powershell
# Проверка текущей политики
Get-ExecutionPolicy

# Установка политики (требует прав администратора)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Возможные значения:
# Restricted - ничего нельзя запускать
# RemoteSigned - локальные скрипты без подписи, удаленные требуют подписи
# AllSigned - все скрипты должны быть подписаны
# Unrestricted - всё можно запускать
# Bypass - не блокировать и не отображать предупреждения
```

### Основные настройки:

```powershell
# Проверка конфигурации сессии
$PSVersionTable

# Настройка цветов консоли
$Host.UI.RawUI.BackgroundColor = "Black"
$Host.UI.RawUI.ForegroundColor = "White"

# Настройка размера окна
$Host.UI.RawUI.WindowSize = New-Object System.Management.Automation.Host.Size(120, 40)
```

## Управление модулями

### Установка модулей:

```powershell
# Проверка установленных модулей
Get-Module
Get-Module -ListAvailable

# Установка модуля из PSGallery
Install-Module -Name Az -AllowClobber -Force
Install-Module -Name PSScriptAnalyzer

# Обновление модуля
Update-Module -Name Az

# Удаление модуля
Uninstall-Module -Name ModuleName

# Импорт модуля
Import-Module -Name ModuleName
```

### Популярные модули:

- **Az** - Azure PowerShell модуль
- **Pester** - модуль для тестирования
- **PSScriptAnalyzer** - анализатор скриптов
- **posh-git** - интеграция с Git
- **PowerShellGet** - управление пакетами

## Основные команды и cmdlets

### Cmdlets для работы с файловой системой:

```powershell
# Просмотр содержимого
Get-ChildItem -Path C:\ -Recurse -Include *.txt
Get-Content -Path .\file.txt
Get-Content -Path .\file.txt -Tail 10
Get-Content -Path .\file.txt -Wait  # как tail -f

# Работа с файлами
Copy-Item -Path .\source.txt -Destination .\backup.txt
Move-Item -Path .\oldname.txt -Destination .\newname.txt
Rename-Item -Path .\oldname.txt -NewName newname.txt
Remove-Item -Path .\unwanted.txt

# Создание
New-Item -ItemType File -Path .\newfile.txt
New-Item -ItemType Directory -Path .\newfolder
```

### Cmdlets для работы с процессами:

```powershell
# Получение процессов
Get-Process
Get-Process -Name chrome
Get-Process | Where-Object {$_.CPU -gt 100}

# Управление процессами
Stop-Process -Name notepad
Stop-Process -Id 1234
Start-Process -FilePath "notepad.exe"
```

### Cmdlets для работы с реестром:

```powershell
# Просмотр
Get-Item -Path HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion
Get-ChildItem -Path HKCU:\Software

# Создание
New-Item -Path HKCU:\Software\MyCompany
New-ItemProperty -Path HKCU:\Software\MyCompany -Name "Setting" -Value "Value"

# Удаление
Remove-Item -Path HKCU:\Software\MyCompany
```

### Cmdlets для работы с сетью:

```powershell
# Проверка соединения
Test-NetConnection -ComputerName google.com
Test-NetConnection -ComputerName google.com -Port 80

# Получение IP конфигурации
Get-NetIPConfiguration
Get-DnsClientServerAddress

# Работа с веб-запросами
Invoke-WebRequest -Uri "https://httpbin.org/get"
Invoke-RestMethod -Uri "https://api.github.com/users/octocat"
```

## Работа с объектами и переменными

### Переменные:

```powershell
# Создание переменных
$name = "John"
$age = 30
$isActive = $true

# Объявление массивов
$names = @("John", "Jane", "Bob")
$numbers = 1..10

# Объявление хэш-таблиц
$user = @{
    Name = "John"
    Age = 30
    IsActive = $true
}

# Объявление объектов
$obj = New-Object PSObject -Property @{
    Name = "John"
    Age = 30
}
```

### Работа с объектами:

```powershell
# Получение свойств объекта
Get-Process | Select-Object Name, ID, CPU
Get-Process | Select-Object Name, @{Name="MB";Expression={$_.WorkingSet/1MB}}

# Фильтрация
Get-Process | Where-Object {$_.CPU -gt 100}
Get-Process | Where-Object ProcessName -Like "*chrome*"

# Сортировка
Get-Process | Sort-Object CPU -Descending

# Группировка
Get-Process | Group-Object Company

# Пайплайн
Get-Process | Where-Object {$_.WorkingSet -gt 100MB} | Sort-Object WorkingSet -Descending | Select-Object -First 5 Name, WorkingSet
```

### Форматирование вывода:

```powershell
# Таблица
Get-Process | Format-Table Name, ID, CPU -AutoSize

# Список
Get-Process | Format-List Name, Path, Company

# Широкий формат
Get-ChildItem | Format-Wide Name -Column 4

# Пользовательское форматирование
Get-Process | Select-Object Name, @{Label="Memory(MB)";Expression={[math]::Round($_.WorkingSet/1MB, 2)}} | Sort-Object "Memory(MB)" -Descending
```

## Скрипты и функции

### Создание скриптов:

```powershell
# Пример скрипта (script.ps1)
Param(
    [Parameter(Mandatory=$true)]
    [string]$ComputerName,
    
    [Parameter(Mandatory=$false)]
    [int]$Port = 80
)

Write-Host "Проверка соединения с $ComputerName на порту $Port"
$result = Test-NetConnection -ComputerName $ComputerName -Port $Port
Write-Output $result
```

### Создание функций:

```powershell
# Простая функция
function Get-SystemInfo {
    $os = Get-CimInstance -ClassName Win32_OperatingSystem
    $computer = Get-CimInstance -ClassName Win32_ComputerSystem
    
    return @{
        ComputerName = $env:COMPUTERNAME
        TotalRAM = [math]::Round($computer.TotalPhysicalMemory / 1GB, 2)
        FreeRAM = [math]::Round($os.FreePhysicalMemory * 1KB / 1GB, 2)
        OS = $os.Caption
    }
}

# Функция с параметрами
function Get-FileSize {
    Param(
        [Parameter(Mandatory=$true, ValueFromPipeline=$true)]
        [string]$Path
    )
    
    Process {
        $item = Get-Item $Path
        if ($item.GetType().Name -eq "FileInfo") {
            return [PSCustomObject]@{
                Name = $item.Name
                Size = [math]::Round($item.Length / 1KB, 2)
                Unit = "KB"
            }
        }
    }
}
```

### Работа с ошибками:

```powershell
# Try-Catch-Finally
try {
    Get-Process -Name "NonExistentProcess"
}
catch {
    Write-Warning "Процесс не найден: $($_.Exception.Message)"
}
finally {
    Write-Verbose "Проверка завершена"
}

# Предпочтения ошибок
$ErrorActionPreference = "Stop"  # или "SilentlyContinue", "Continue"
```

## Практические примеры

### Пример №1: Скрипт для мониторинга диска

```powershell
# disk-monitor.ps1
function Get-DiskUsageReport {
    $disks = Get-WmiObject -Class Win32_LogicalDisk | Where-Object {$_.DriveType -eq 3}
    
    foreach ($disk in $disks) {
        $freeSpaceGB = [math]::Round($disk.FreeSpace / 1GB, 2)
        $totalSpaceGB = [math]::Round($disk.Size / 1GB, 2)
        $usedSpaceGB = $totalSpaceGB - $freeSpaceGB
        $percentFree = [math]::Round(($freeSpaceGB / $totalSpaceGB) * 100, 2)
        
        [PSCustomObject]@{
            Drive = $disk.DeviceID
            TotalGB = $totalSpaceGB
            UsedGB = $usedSpaceGB
            FreeGB = $freeSpaceGB
            PercentFree = $percentFree
            Status = if ($percentFree -lt 10) { "WARNING" } else { "OK" }
        }
    }
}

# Использование
Get-DiskUsageReport | Format-Table -AutoSize
```

### Пример №2: Скрипт для управления службами

```powershell
# service-manager.ps1
function Manage-Service {
    param(
        [Parameter(Mandatory=$true)]
        [string]$ServiceName,
        
        [Parameter(Mandatory=$true)]
        [ValidateSet("Start", "Stop", "Restart", "Status")]
        [string]$Action
    )
    
    try {
        switch ($Action) {
            "Start" { 
                Start-Service -Name $ServiceName -ErrorAction Stop
                Write-Host "Служба $ServiceName запущена" -ForegroundColor Green
            }
            "Stop" { 
                Stop-Service -Name $ServiceName -ErrorAction Stop
                Write-Host "Служба $ServiceName остановлена" -ForegroundColor Yellow
            }
            "Restart" {
                Restart-Service -Name $ServiceName -ErrorAction Stop
                Write-Host "Служба $ServiceName перезапущена" -ForegroundColor Cyan
            }
            "Status" {
                $service = Get-Service -Name $ServiceName
                Write-Host "Состояние службы $ServiceName: $($service.Status)" -ForegroundColor White
            }
        }
    }
    catch {
        Write-Error "Ошибка при управлении службой $ServiceName`: $($_.Exception.Message)"
    }
}

# Использование
Manage-Service -ServiceName "Spooler" -Action Status
```

### Пример №3: Работа с JSON и API

```powershell
# api-client.ps1
function Invoke-ApiCall {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Uri,
        
        [Parameter(Mandatory=$false)]
        [hashtable]$Headers = @{},
        
        [Parameter(Mandatory=$false)]
        [string]$Method = "GET"
    )
    
    $params = @{
        Uri = $Uri
        Method = $Method
        Headers = $Headers
        ContentType = "application/json"
    }
    
    try {
        $response = Invoke-RestMethod @params
        return $response
    }
    catch {
        Write-Error "Ошибка API вызова: $($_.Exception.Message)"
        return $null
    }
}

# Использование
$data = Invoke-ApiCall -Uri "https://jsonplaceholder.typicode.com/posts/1"
$data | ConvertTo-Json -Depth 3
```

## Лучшие практики

### 1. Используйте соответствующие имена для cmdlets:

```powershell
# Хорошо: используйте стандартные глаголы PowerShell
Get-User
Set-Configuration
Find-File
Test-Connection

# Плохо: нестандартные глаголы
Show-User
Change-Config
Search-File
Ping-Server
```

### 2. Добавляйте параметры к функциям:

```powershell
# Хорошо: используйте параметры с валидацией
function Get-FileSummary {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true, ValueFromPipeline=$true)]
        [ValidateScript({Test-Path $_ -PathType Leaf})]
        [string]$Path
    )
    
    process {
        $file = Get-Item $Path
        return [PSCustomObject]@{
            Name = $file.Name
            Size = $file.Length
            Extension = $file.Extension
        }
    }
}
```

### 3. Обрабатывайте ошибки должным образом:

```powershell
# Используйте try-catch и соответствующие уровни детализации ошибок
try {
    $result = Get-Content $FilePath -ErrorVariable GetError -ErrorAction Stop
}
catch [System.IO.FileNotFoundException] {
    Write-Error "Файл не найден: $FilePath"
}
catch {
    Write-Error "Неизвестная ошибка: $($_.Exception.Message)"
}
```

### 4. Используйте PSScriptAnalyzer:

```powershell
# Установите и используйте анализатор для проверки качества кода
Install-Module -Name PSScriptAnalyzer -Force
Invoke-ScriptAnalyzer -Path .\MyScript.ps1
```

### 5. Документируйте свои скрипты:

```powershell
<#
.SYNOPSIS
    Краткое описание функции
.DESCRIPTION
    Подробное описание функции
.PARAMETER ParameterName
    Описание параметра
.EXAMPLE
    Пример использования
.INPUTS
    Типы входных данных
.OUTPUTS
    Типы выходных данных
.NOTES
    Дополнительная информация
#>
function Get-Example {
    param(
        [Parameter(Mandatory=$true)]
        [string]$InputObject
    )
    
    # Тело функции
}
```

### 6. Используйте безопасные методы для выполнения:

```powershell
# Всегда проверяйте Execution Policy при запуске скриптов
# Используйте безопасные методы для выполнения команд
$ExecutionContext.SessionState.LanguageMode  # Проверить режим языка
```

---

#### 💼 Автор: Дуплей Максим Игоревич

### 📲 Контакты:

- **Telegram №1:** [@quadd4rv1n7](https://t.me/quadd4rv1n7)
- **Telegram №2:** [@dupley_maxim_1999](https://t.me/dupley_maxim_1999)

📅 **Дата:** 26.01.2026

▶️ Версия 1.0

---
> 📧 **Предложения по сотрудничеству:** maksimqwe42@mail.ru

---

### 💼 Профиль на Profi.ru
[![Profi.ru Profile](https://img.shields.io/badge/Profi.ru-Дуплей%20М.И.-FF6B35?style=for-the-badge)](https://profi.ru/profile/DupleyMI)

> Консультации и услуги программирования на платформе Profi.ru

---

### 📚 Услуги обучения
[![Обучение технологиям и языкам программирования на Kwork](https://img.shields.io/badge/Kwork-Обучение%20Программированию-blue?style=for-the-badge&logo=kwork)](https://kwork.ru/usability-testing/42465951/obuchenie-tekhnologiyam-i-yazykam-programmirovaniya)

> Профессиональное обучение технологиям и языкам программирования. Персональные консультации и курсы от опытного преподавателя.

---

### 🏫 О школе
[![Website](https://img.shields.io/badge/Maestro7IT-school--maestro7it.ru-darkgreen?style=for-the-badge)](https://school-maestro7it.ru/)

> Инновационная школа программирования, специализирующаяся на подготовке специалистов в области современных технологий и языков программирования.