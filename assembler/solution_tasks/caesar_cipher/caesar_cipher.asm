; ----------------------------------------------------------------------------------------
; Программа для шифрования текста с использованием шифра Цезаря на языке ассемблера x86. ;
;                                                                                        ;
; Описание:                                                                              ;
; Эта программа шифрует введенный пользователем текст с использованием шифра Цезаря.     ;
;                                                                                        ;
; Использование:                                                                         ;
; - Компилируйте программу с помощью NASM.                                               ;
; - Запустите скомпилированный файл для шифрования текста.                               ;
;                                                                                        ;
; Автор: [Дуплей Максим Игоревич]                                                        ;
; Дата: [15.03.2025]                                                                     ;
; ----------------------------------------------------------------------------------------

section .data
    prompt db 'Enter text to encrypt: ', 0
    encrypted_msg db 'Encrypted text: ', 0
    newline db 0xA, 0

section .bss
    input resb 100
    output resb 100

section .text
    global _start

_start:
    ; Вывод приглашения для ввода
    mov eax, 4          ; системный вызов для sys_write
    mov ebx, 1          ; файловый дескриптор 1 - стандартный вывод
    mov ecx, prompt     ; адрес строки
    mov edx, 22         ; длина строки
    int 0x80            ; вызов ядра

    ; Чтение ввода пользователя
    mov eax, 3          ; системный вызов для sys_read
    mov ebx, 0          ; файловый дескриптор 0 - стандартный ввод
    mov ecx, input      ; адрес буфера для ввода
    mov edx, 100        ; максимальная длина ввода
    int 0x80            ; вызов ядра

    ; Шифрование текста
    mov esi, input      ; указатель на начало введенного текста
    mov edi, output     ; указатель на начало буфера для вывода
    mov ecx, eax        ; количество символов для шифрования
    mov ebx, 3          ; сдвиг для шифра Цезаря

encrypt_loop:
    lodsb               ; загрузка символа из input в al
    cmp al, 0           ; проверка на конец строки
    je encrypt_done     ; если конец строки, завершить шифрование

    ; Шифрование символа
    cmp al, 'A'
    jl not_upper
    cmp al, 'Z'
    jg not_upper
    add al, bl          ; сдвиг символа
    cmp al, 'Z'
    jle store_char
    sub al, 26          ; коррекция, если вышли за пределы алфавита
    jmp store_char

not_upper:
    cmp al, 'a'
    jl store_char
    cmp al, 'z'
    jg store_char
    add al, bl          ; сдвиг символа
    cmp al, 'z'
    jle store_char
    sub al, 26          ; коррекция, если вышли за пределы алфавита

store_char:
    stosb               ; сохранение символа в output
    loop encrypt_loop   ; повторение

encrypt_done:
    ; Вывод сообщения "Encrypted text: "
    mov eax, 4
    mov ebx, 1
    mov ecx, encrypted_msg
    mov edx, 16
    int 0x80

    ; Вывод зашифрованного текста
    mov eax, 4
    mov ebx, 1
    mov ecx, output
    mov edx, 100
    int 0x80

    ; Вывод новой строки
    mov eax, 4
    mov ebx, 1
    mov ecx, newline
    mov edx, 1
    int 0x80

    ; Завершение программы
    mov eax, 1          ; системный вызов для sys_exit
    xor ebx, ebx        ; код возврата 0
    int 0x80            ; вызов ядра
