# Скрипт для скачивания Bootstrap и зависимостей локально

Write-Host "Скачивание Bootstrap и зависимостей..." -ForegroundColor Green

# Создание папок
$folders = @(
    "static/vendor/bootstrap/css",
    "static/vendor/bootstrap/js",
    "static/vendor/bootstrap-icons/font"
)

foreach ($folder in $folders) {
    if (!(Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
        Write-Host "Создана папка: $folder" -ForegroundColor Yellow
    }
}

# URLs для скачивания
$downloads = @{
    "Bootstrap CSS" = @{
        url = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
        path = "static/vendor/bootstrap/css/bootstrap.min.css"
    }
    "Bootstrap JS" = @{
        url = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
        path = "static/vendor/bootstrap/js/bootstrap.bundle.min.js"
    }
    "Bootstrap Icons CSS" = @{
        url = "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css"
        path = "static/vendor/bootstrap-icons/font/bootstrap-icons.css"
    }
    "Bootstrap Icons Fonts" = @{
        url = "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/fonts/bootstrap-icons.woff2"
        path = "static/vendor/bootstrap-icons/font/fonts/bootstrap-icons.woff2"
    }
}

# Создание папки для шрифтов
if (!(Test-Path "static/vendor/bootstrap-icons/font/fonts")) {
    New-Item -ItemType Directory -Path "static/vendor/bootstrap-icons/font/fonts" -Force | Out-Null
}

# Скачивание файлов
foreach ($item in $downloads.GetEnumerator()) {
    Write-Host "Скачивание $($item.Key)..." -ForegroundColor Cyan
    try {
        Invoke-WebRequest -Uri $item.Value.url -OutFile $item.Value.path -ErrorAction Stop
        Write-Host "✓ $($item.Key) скачан успешно" -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Ошибка при скачивании $($item.Key): $_" -ForegroundColor Red
    }
}

Write-Host "`nГотово! Файлы скачаны в static/vendor/" -ForegroundColor Green
Write-Host "Теперь обновите пути в шаблонах для использования локальных файлов." -ForegroundColor Yellow
