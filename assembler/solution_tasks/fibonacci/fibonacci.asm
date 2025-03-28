; --------------------------------------------------------------------------------------------------- ;
; Программа для вычисления и вывода последовательности Фибоначчи на языке ассемблера x86.             ;
;                                                                                                     ;
; Описание:                                                                                           ;
; Эта программа вычисляет первые несколько чисел последовательности Фибоначчи и выводит их на экран.  ;
;                                                                                                     ;
; Использование:                                                                                      ;
; - Компилируйте программу с помощью NASM.                                                            ;
; - Запустите скомпилированный файл для вывода последовательности Фибоначчи.                          ;
;                                                                                                     ;
; Автор: [Дуплей Максим Игоревич]                                                                     ;
; Дата: [14.03.2025]                                                                                  ;
; --------------------------------------------------------------------------------------------------- ;

section .data
    fib db 'Fibonacci Sequence: ', 0  ; Строка для вывода названия последовательности
    newline db 0xA, 0                 ; Символ новой строки

section .bss
    num resb 10  ; Буфер для хранения числа в виде строки

section .text
    global _start

_start:
    ; Вывод строки "Fibonacci Sequence: "
    mov eax, 4          ; системный вызов для sys_write
    mov ebx, 1          ; файловый дескриптор 1 - стандартный вывод
    mov ecx, fib        ; адрес строки
    mov edx, 18         ; длина строки
    int 0x80            ; вызов ядра

    ; Инициализация первых двух чисел Фибоначчи
    mov ecx, 10         ; количество чисел Фибоначчи для вычисления
    mov eax, 0          ; первое число
    mov ebx, 1          ; второе число

fibonacci_loop:
    ; Вывод текущего числа
    call print_number

    ; Вывод новой строки
    mov eax, 4
    mov ebx, 1
    mov ecx, newline
    mov edx, 1
    int 0x80

    ; Вычисление следующего числа Фибоначчи
    mov edx, eax        ; edx = eax (предыдущее число)
    add eax, ebx        ; eax = eax + ebx (следующее число)
    mov ebx, edx        ; ebx = edx (предыдущее число)

    loop fibonacci_loop

    ; Завершение программы
    mov eax, 1          ; системный вызов для sys_exit
    xor ebx, ebx        ; код возврата 0
    int 0x80            ; вызов ядра

print_number:
    ; Преобразование числа в строку и вывод
    mov esi, num + 9    ; указатель на конец буфера
    mov byte [esi], 0   ; завершающий нуль
    mov edi, 10         ; делитель

convert_loop:
    xor edx, edx        ; очистка edx
    div edi             ; деление eax на 10
    add dl, '0'         ; преобразование остатка в символ
    dec esi             ; уменьшение указателя
    mov [esi], dl       ; сохранение символа в буфере
    test eax, eax       ; проверка, равно ли eax нулю
    jnz convert_loop    ; повторение, если eax не равен нулю

    ; Вывод строки
    mov eax, 4
    mov ebx, 1
    mov ecx, esi
    mov edx, 10
    sub edx, ecx
    int 0x80

    ret
