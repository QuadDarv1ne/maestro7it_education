#!/bin/bash
echo "Проверка и настройка локали UTF-8..."
if ! locale -a | grep -i "en_US.utf8"; then
    echo "Установка локали en_US.UTF-8..."
    sudo locale-gen en_US.UTF-8
    sudo update-locale LANG=en_US.UTF-8
fi
echo "Локаль настроена. Запуск калькулятора..."
./calculator