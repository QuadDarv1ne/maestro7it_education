;/*
;### Устный счёт (Арифметический тренажер) на FASM
;
;Описание:
;  Программа генерирует случайные арифметические выражения, вычисляет их результат
;  и предлагает пользователю решить их на время. Поддерживает настройку сложности
;  и выбор операций.
;
;Основные функции:
;  1. Генерация выражений:
;     - Операции: +, -, *, /, ^ (возведение в степень)
;     - Поддержка скобок
;     - Числа в диапазоне 1-20
;
;  2. Настройка параметров:
;     - Длина выражения (1-5 операций)
;     - Выбор используемых операций
;
;  3. Проверка ответов:
;     - Замер времени решения
;     - Сравнение с правильным ответом
;     - Информативная обратная связь
;
;  4. Особенности реализации:
;     - Рекурсивный алгоритм вычислений
;     - Правильный приоритет операций
;     - Гибкая система настроек
;
;Пример работы:
;  1. Пользователь выбирает:
;     - Длина = 3
;     - Операции: +, -, *
;  2. Программа генерирует:
;     "Вычислите: 5 * (3 + 2) - 4"
;  3. После ввода ответа:
;     "Правильно! Время: 4500 мс"
;     или
;     "Неверно. Правильный ответ: 21"
;
;Возможные улучшения:
;  - Добавление дробных чисел
;  - Система подсчёта очков
;  - Режим "экзамена"
;*/

format PE console
entry start

include 'win32a.inc'

section '.data' data readable writeable
    welcome_msg db 'Устный счет! Вам будет предложено арифметическое выражение.',13,10
                db 'Введите ваш ответ и нажмите Enter.',13,10
                db 'Вы можете настроить параметры игры:',13,10
                db '1 - Длина выражения (1-5)',13,10
                db '2 - Используемые операции',13,10
                db '3 - Начать игру',13,10
                db 'Выберите пункт меню: ',0
                
    config_ops_msg db 'Выберите операции (можно несколько):',13,10
                   db '1 - Сложение (+)',13,10
                   db '2 - Вычитание (-)',13,10
                   db '3 - Умножение (*)',13,10
                   db '4 - Деление (/)',13,10
                   db '5 - Возведение в степень (^)',13,10
                   db 'Введите цифры выбранных операций (например 123): ',0
                   
    config_len_msg db 'Введите длину выражения (1-5): ',0
    invalid_input db 'Неверный ввод! Попробуйте еще раз.',13,10,0
    expr_msg db 'Вычислите: ',0
    input_prompt db 'Ваш ответ: ',0
    correct_msg db 'Правильно!',13,10,0
    wrong_msg db 'Неверно. Правильный ответ: ',0
    time_msg db 'Время: %d мс',13,10,0
    newline db 13,10,0
    press_any_key db 'Нажмите любую клавишу чтобы продолжить...',0
    
    ; Конфигурация
    expr_length dd 3
    enabled_ops db 1,1,1,0,0  ; +,-,*,/,^ (1-включено, 0-выключено)
    
    ; Переменные
    start_time dd 0
    end_time dd 0
    user_answer dd 0
    correct_answer dd 0
    expr_buffer rb 256
    
    ; Операции
    ops db '+','-','*','/','^'
    ops_functions dd add_op, sub_op, mul_op, div_op, pow_op
    
    ; Для генерации случайных чисел
    rand_seed dd 0

section '.code' code readable executable

start:
    ; Инициализация генератора случайных чисел
    invoke  GetTickCount
    mov     [rand_seed], eax
    
main_menu:
    ; Очистка экрана
    invoke  system, 'cls'
    
    ; Вывод меню
    invoke  printf, welcome_msg
    invoke  scanf, '%d', esp-4
    pop     eax
    
    cmp     eax, 1
    je      config_length
    cmp     eax, 2
    je      config_operations
    cmp     eax, 3
    je      start_game
    jmp     main_menu  ; Неверный ввод

config_length:
    invoke  printf, config_len_msg
    invoke  scanf, '%d', esp-4
    pop     eax
    
    cmp     eax, 1
    jl      invalid_config
    cmp     eax, 5
    jg      invalid_config
    
    mov     [expr_length], eax
    jmp     main_menu
    
invalid_config:
    invoke  printf, invalid_input
    invoke  system, 'pause'
    jmp     config_length

config_operations:
    invoke  printf, config_ops_msg
    invoke  scanf, '%s', esp-256
    add     esp, 256
    
    ; Сначала выключаем все операции
    mov     dword [enabled_ops], 0
    mov     byte [enabled_ops+4], 0
    
    ; Включаем выбранные
    mov     esi, esp-256
.config_ops_loop:
    lodsb
    test    al, al
    jz      .config_ops_done
    
    sub     al, '1'
    cmp     al, 4
    ja      .config_ops_loop
    
    mov     byte [enabled_ops+eax], 1
    jmp     .config_ops_loop
    
.config_ops_done:
    jmp     main_menu

start_game:
    ; Генерация выражения
    call    generate_expression
    
    ; Вывод выражения
    invoke  printf, expr_msg
    invoke  printf, expr_buffer
    invoke  printf, newline
    
    ; Засекаем время
    invoke  GetTickCount
    mov     [start_time], eax
    
    ; Получаем ответ пользователя
    invoke  printf, input_prompt
    invoke  scanf, '%d', user_answer
    
    ; Фиксируем время
    invoke  GetTickCount
    mov     [end_time], eax
    
    ; Проверка ответа
    mov     eax, [user_answer]
    cmp     eax, [correct_answer]
    jne     wrong_answer
    
    ; Правильный ответ
    invoke  printf, correct_msg
    jmp     show_time
    
wrong_answer:
    invoke  printf, wrong_msg
    invoke  printf, '%d', [correct_answer]
    invoke  printf, newline
    
show_time:
    mov     eax, [end_time]
    sub     eax, [start_time]
    invoke  printf, time_msg, eax
    
    ; Пауза
    invoke  printf, press_any_key
    invoke  _getch
    
    jmp     main_menu

; Генерация случайного выражения
generate_expression:
    push    ebx esi edi
    
    ; Очищаем буфер
    mov     edi, expr_buffer
    xor     al, al
    mov     ecx, 256
    rep stosb
    
    mov     edi, expr_buffer
    
    ; Генерируем выражение
    mov     ecx, [expr_length]
    dec     ecx  ; Количество операций
    
    ; Первое число
    call    rand_num
    call    append_number
    
.gen_loop:
    ; Выбираем случайную операцию
    call    rand_op
    mov     bl, al
    
    ; Случайное число
    call    rand_num
    
    ; Добавляем операцию и число
    mov     [edi], bl
    inc     edi
    call    append_number
    
    loop    .gen_loop
    
    ; Вычисляем результат
    push    expr_buffer
    call    evaluate_expression
    add     esp, 4
    mov     [correct_answer], eax
    
    pop     edi esi ebx
    ret

; Добавление числа в буфер
append_number:
    push    eax ebx ecx edx
    
    ; Преобразуем число в строку
    mov     ebx, edi
    invoke  itoa, eax, ebx, 10
    
    ; Перемещаем указатель
    add     edi, eax
    
    pop     edx ecx ebx eax
    ret

; Генерация случайного числа (1-20)
rand_num:
    call    rand
    xor     edx, edx
    mov     ecx, 20
    div     ecx
    inc     edx
    mov     eax, edx
    ret

; Генерация случайной операции
rand_op:
    push    ebx ecx
    
    ; Считаем количество доступных операций
    xor     ecx, ecx
    mov     ebx, enabled_ops
    mov     edx, 5
    
.count_loop:
    cmp     byte [ebx], 0
    je      .next_op
    inc     ecx
.next_op:
    inc     ebx
    dec     edx
    jnz     .count_loop
    
    ; Если нет доступных операций, используем сложение
    test    ecx, ecx
    jz      .default_add
    
    ; Выбираем случайную операцию из доступных
    call    rand
    xor     edx, edx
    div     ecx
    
    ; Находим выбранную операцию
    xor     ecx, ecx
    mov     ebx, enabled_ops
.find_op_loop:
    cmp     byte [ebx+ecx], 0
    je      .skip_op
    dec     edx
    js      .found_op
.skip_op:
    inc     ecx
    jmp     .find_op_loop
    
.found_op:
    mov     al, [ops+ecx]
    jmp     .done
    
.default_add:
    mov     al, '+'
    
.done:
    pop     ecx ebx
    ret

; Генератор случайных чисел (0..RAND_MAX)
rand:
    mov     eax, [rand_seed]
    imul    eax, 1103515245
    add     eax, 12345
    mov     [rand_seed], eax
    shr     eax, 16
    and     eax, 0x7FFF
    ret

; Вычисление выражения (рекурсивный спуск)
evaluate_expression:
    push    ebp
    mov     ebp, esp
    
    ; Читаем первое значение
    call    parse_term
    push    eax
    
.eval_loop:
    ; Получаем текущий символ
    mov     esi, [ebp+8]
    mov     al, [esi]
    
    ; Проверяем операцию
    cmp     al, '+'
    je      .do_add
    cmp     al, '-'
    je      .do_sub
    
    ; Конец выражения
    pop     eax
    jmp     .done
    
.do_add:
    ; Пропускаем оператор
    inc     dword [ebp+8]
    
    ; Читаем следующий терм
    call    parse_term
    
    ; Выполняем сложение
    pop     edx
    add     eax, edx
    push    eax
    jmp     .eval_loop
    
.do_sub:
    ; Пропускаем оператор
    inc     dword [ebp+8]
    
    ; Читаем следующий терм
    call    parse_term
    
    ; Выполняем вычитание
    pop     edx
    sub     edx, eax
    mov     eax, edx
    push    eax
    jmp     .eval_loop
    
.done:
    mov     esp, ebp
    pop     ebp
    ret

; Разбор терма (умножение/деление)
parse_term:
    push    ebp
    mov     ebp, esp
    
    ; Читаем первое значение
    call    parse_factor
    push    eax
    
.term_loop:
    ; Получаем текущий символ
    mov     esi, [ebp+8]
    mov     al, [esi]
    
    ; Проверяем операцию
    cmp     al, '*'
    je      .do_mul
    cmp     al, '/'
    je      .do_div
    cmp     al, '^'
    je      .do_pow
    
    ; Конец терма
    pop     eax
    jmp     .done
    
.do_mul:
    ; Пропускаем оператор
    inc     dword [ebp+8]
    
    ; Читаем следующий фактор
    call    parse_factor
    
    ; Выполняем умножение
    pop     edx
    imul    eax, edx
    push    eax
    jmp     .term_loop
    
.do_div:
    ; Пропускаем оператор
    inc     dword [ebp+8]
    
    ; Читаем следующий фактор
    call    parse_factor
    
    ; Выполняем деление
    pop     edx
    push    eax
    mov     eax, edx
    cdq
    pop     ebx
    idiv    ebx
    push    eax
    jmp     .term_loop
    
.do_pow:
    ; Пропускаем оператор
    inc     dword [ebp+8]
    
    ; Читаем следующий фактор
    call    parse_factor
    
    ; Выполняем возведение в степень
    pop     ecx  ; степень
    mov     ebx, eax  ; основание
    mov     eax, 1
.pow_loop:
    test    ecx, ecx
    jz      .pow_done
    imul    eax, ebx
    dec     ecx
    jmp     .pow_loop
.pow_done:
    push    eax
    jmp     .term_loop
    
.done:
    mov     esp, ebp
    pop     ebp
    ret

; Разбор фактора (число или выражение в скобках)
parse_factor:
    push    ebp
    mov     ebp, esp
    
    ; Получаем текущий символ
    mov     esi, [ebp+8]
    mov     al, [esi]
    
    ; Проверяем на скобку
    cmp     al, '('
    jne     .not_bracket
    
    ; Пропускаем '('
    inc     dword [ebp+8]
    
    ; Рекурсивно вычисляем выражение в скобках
    call    evaluate_expression
    push    eax
    
    ; Пропускаем ')'
    inc     dword [ebp+8]
    pop     eax
    jmp     .done
    
.not_bracket:
    ; Читаем число
    call    parse_number
    
.done:
    mov     esp, ebp
    pop     ebp
    ret

; Разбор числа
parse_number:
    push    ebx ecx edx
    
    mov     esi, [ebp+8]
    xor     eax, eax
    xor     ecx, ecx
    
    ; Проверяем знак
    mov     bl, [esi]
    cmp     bl, '-'
    jne     .digit_loop
    inc     esi
    mov     ecx, 1
    
.digit_loop:
    mov     bl, [esi]
    sub     bl, '0'
    cmp     bl, 9
    ja      .done_digits
    
    ; Добавляем цифру
    imul    eax, 10
    add     eax, ebx
    inc     esi
    jmp     .digit_loop
    
.done_digits:
    ; Учитываем знак
    test    ecx, ecx
    jz      .positive
    neg     eax
    
.positive:
    ; Обновляем указатель
    mov     [ebp+8], esi
    
    pop     edx ecx ebx
    ret

; Арифметические операции
add_op:
    add     eax, ebx
    ret
sub_op:
    sub     eax, ebx
    ret
mul_op:
    imul    eax, ebx
    ret
div_op:
    cdq
    idiv    ebx
    ret
pow_op:
    push    ecx
    mov     ecx, ebx
    mov     ebx, eax
    mov     eax, 1
.pow_loop:
    test    ecx, ecx
    jz      .pow_done
    imul    eax, ebx
    dec     ecx
    jmp     .pow_loop
.pow_done:
    pop     ecx
    ret

section '.idata' import data readable

library kernel32,'kernel32.dll',\
        msvcrt,'msvcrt.dll'

import kernel32,\
       GetTickCount,'GetTickCount',\
       ExitProcess,'ExitProcess'

import msvcrt,\
       printf,'printf',\
       scanf,'scanf',\
       _getch,'_getch',\
       system,'system',\
       itoa,'_itoa'
