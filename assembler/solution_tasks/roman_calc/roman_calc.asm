org 0x100        ; COM-файл для DOS
jmp start

; Данные
prompt db 'Введите выражение (например, V+III): $'
error_msg db 0Dh,0Ah,'Ошибка! Некорректный ввод.$'
result_msg db 0Dh,0Ah,'Результат: $'
buffer times 16 db 0
num1 dw 0
num2 dw 0
operator db 0

; Таблица преобразования римских символов
roman_values:
    db 'I', 1
    db 'V', 5
    db 'X', 10
    db 'L', 50
    db 'C', 100
    db 'D', 500
    db 'M', 1000

start:
    ; Вывод приглашения
    mov ah, 9
    mov dx, prompt
    int 21h

    ; Ввод строки
    mov ah, 0Ah
    mov dx, buffer
    int 21h

    ; Парсинг ввода
    call parse_input
    jc .error

    ; Конвертация римских -> арабские
    call roman_to_arabic
    jc .error

    ; Выполнение операции
    call calculate
    jc .error

    ; Конвертация обратно и вывод
    call arabic_to_roman
    jmp .exit

.error:
    mov ah, 9
    mov dx, error_msg
    int 21h

.exit:
    mov ax, 0x4C00
    int 21h

;---------------------------------------
; Процедура парсинга ввода             ;
; Выход: num1, operator, num2          ;
;---------------------------------------
parse_input:
    ; Реализация парсинка строки в num1, оператор и num2
    ret

;-------------------------------------------
; Преобразование римского числа в арабское ;
; Вход: DS:SI - строка                     ;
; Выход: AX - число, CF=1 при ошибке       ;
;-------------------------------------------
roman_to_arabic:
    xor ax, ax
    xor cx, cx
    mov bx, roman_values
.loop:
    ; Реализация сравнения символов и подсчета
    ret

;-------------------------------------------
; Преобразование арабского числа в римское ;
; Вход: AX - число                         ;
; Выход: DS:DI - строка, CF=1 при ошибке   ;
;-------------------------------------------
arabic_to_roman:
    mov di, buffer
    ; Таблица значений: M, CM, D, CD, C, XC...
.values_table:
    dw 1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1
.letters:
    db 'M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I'

    ; Реализация алгоритма подбора символов
    ret

;---------------------------------------
; Выполнение арифметической операции   ;
;---------------------------------------
calculate:
    cmp [operator], '+'
    je .add
    cmp [operator], '-'
    je .sub
    stc
    ret
.add:
    mov ax, [num1]
    add ax, [num2]
    ret
.sub:
    mov ax, [num1]
    sub ax, [num2]
    ret
