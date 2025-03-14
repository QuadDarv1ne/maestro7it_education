; ----------------------------------------------------------------------------- ;
; Программа для вычисления факториала числа на языке ассемблера x86.            ;
;                                                                               ;
; Описание:                                                                     ;
; Эта программа принимает число от пользователя и вычисляет его факториал.      ;
;                                                                               ;
; Использование:                                                                ;
; - Компилируйте программу с помощью NASM.                                      ;
; - Запустите скомпилированный файл для вывода факториала введенного числа.     ;
;                                                                               ;
; Автор: [Дуплей Максим Игоревич]                                               ;
; Дата: [14.03.2025]                                                            ;
; ----------------------------------------------------------------------------- ;

section .data
    prompt db 'Enter a number: ', 0  ; Строка для вывода приглашения
    result_msg db 'Factorial: ', 0   ; Строка для вывода результата
    newline db 0xA, 0                ; Символ новой строки

section .bss
    num resb 10   ; Буфер для хранения числа в виде строки
    input resb 10 ; Буфер для ввода пользователя

section .text
    global _start

_start:
    ; Вывод приглашения для ввода
    mov eax, 4          ; системный вызов для sys_write
    mov ebx, 1          ; файловый дескриптор 1 - стандартный вывод
    mov ecx, prompt     ; адрес строки
    mov edx, 15         ; длина строки
    int 0x80            ; вызов ядра

    ; Чтение ввода пользователя
    mov eax, 3          ; системный вызов для sys_read
    mov ebx, 0          ; файловый дескриптор 0 - стандартный ввод
    mov ecx, input      ; адрес буфера для ввода
    mov edx, 10         ; максимальная длина ввода
    int 0x80            ; вызов ядра

    ; Преобразование введенной строки в число
    mov esi, input      ; указатель на начало строки
    xor eax, eax        ; очистка eax
    xor ebx, ebx        ; очистка ebx

convert_loop:
    mov cl, [esi]       ; чтение символа из строки
    cmp cl, 0xA         ; проверка на конец строки
    je convert_done     ; если конец строки, завершить преобразование
    sub cl, '0'         ; преобразование символа в число
    imul eax, eax, 10   ; умножение eax на 10
    add eax, ecx        ; добавление числа к eax
    inc esi             ; увеличение указателя
    jmp convert_loop    ; повторение

convert_done:
    ; Вычисление факториала
    mov ecx, eax        ; ecx = число для вычисления факториала
    mov eax, 1          ; eax = 1 (начальное значение факториала)

factorial_loop:
    cmp ecx, 1          ; сравнение ecx с 1
    jle factorial_done  ; если ecx <= 1, завершить вычисление
    imul eax, ecx       ; eax = eax * ecx
    loop factorial_loop ; повторение

factorial_done:
    ; Вывод сообщения "Factorial: "
    mov eax, 4
    mov ebx, 1
    mov ecx, result_msg
    mov edx, 10
    int 0x80

    ; Вывод результата
    call print_number

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

print_number:
    ; Преобразование числа в строку и вывод
    mov esi, num + 9    ; указатель на конец буфера
    mov byte [esi], 0   ; завершающий нуль
    mov edi, 10         ; делитель

convert_number_loop:
    xor edx, edx            ; очистка edx
    div edi                 ; деление eax на 10
    add dl, '0'             ; преобразование остатка в символ
    dec esi                 ; уменьшение указателя
    mov [esi], dl           ; сохранение символа в буфере
    test eax, eax           ; проверка, равно ли eax нулю
    jnz convert_number_loop ; повторение, если eax не равен нулю

    ; Вывод строки
    mov eax, 4
    mov ebx, 1
    mov ecx, esi
    mov edx, 10
    sub edx, ecx
    int 0x80

    ret
