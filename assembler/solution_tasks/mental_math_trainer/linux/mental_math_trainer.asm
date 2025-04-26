;/*
;### Устный счёт (Арифметический тренажер) для Linux
;
;Для сборки:
;   fasm mental_math_trainer.asm
;   chmod +x mental_math_trainer
;   ./mental_math_trainer
;*/

format ELF executable 3
entry _start

; Системные вызовы
SYS_WRITE = 4
SYS_READ = 3
SYS_TIME = 13
SYS_EXIT = 1
STDOUT = 1
STDIN = 0

macro sys_write str, str_len {
    mov eax, SYS_WRITE
    mov ebx, STDOUT
    mov ecx, str
    mov edx, str_len
    int 0x80
}

macro sys_read buf, buf_len {
    mov eax, SYS_READ
    mov ebx, STDIN
    mov ecx, buf
    mov edx, buf_len
    int 0x80
}

macro sys_time {
    mov eax, SYS_TIME
    xor ebx, ebx
    int 0x80
}

macro sys_exit code {
    mov eax, SYS_EXIT
    mov ebx, code
    int 0x80
}

section '.data' writeable
    ; Сообщения
    welcome_msg db 'Устный счет! Вам будет предложено арифметическое выражение.',10
                db 'Введите ваш ответ и нажмите Enter.',10
                db 'Вы можете настроить параметры игры:',10
                db '1 - Длина выражения (1-5)',10
                db '2 - Используемые операции',10
                db '3 - Начать игру',10
                db 'Выберите пункт меню: ',0
    welcome_len = $ - welcome_msg
    
    config_ops_msg db 'Выберите операции (можно несколько):',10
                   db '1 - Сложение (+)',10
                   db '2 - Вычитание (-)',10
                   db '3 - Умножение (*)',10
                   db '4 - Деление (/)',10
                   db '5 - Возведение в степень (^)',10
                   db 'Введите цифры выбранных операций (например 123): ',0
    config_ops_len = $ - config_ops_msg
    
    config_len_msg db 'Введите длину выражения (1-5): ',0
    config_len_len = $ - config_len_msg
    
    invalid_input db 'Неверный ввод! Попробуйте еще раз.',10,0
    invalid_len = $ - invalid_input
    
    expr_msg db 'Вычислите: ',0
    expr_len = $ - expr_msg
    
    input_prompt db 'Ваш ответ: ',0
    input_len = $ - input_prompt
    
    correct_msg db 'Правильно!',10,0
    correct_len = $ - correct_msg
    
    wrong_msg db 'Неверно. Правильный ответ: ',0
    wrong_len = $ - wrong_msg
    
    newline db 10,0
    newline_len = $ - newline
    
    ; Конфигурация
    expr_length dd 3
    enabled_ops db 1,1,1,0,0  ; +,-,*,/,^
    
    ; Переменные
    start_time dd 0
    end_time dd 0
    user_answer dd 0
    correct_answer dd 0
    expr_buffer rb 256
    input_buffer rb 32
    
    ; Операции
    ops db '+','-','*','/','^'
    
    ; Для генерации случайных чисел
    rand_seed dd 0

section '.text' executable
_start:
    ; Инициализация генератора случайных чисел
    sys_time
    mov [rand_seed], eax
    
main_menu:
    ; Очистка экрана (просто выводим много новых строк)
    mov ecx, 50
.clear_loop:
    push ecx
    sys_write newline, newline_len
    pop ecx
    loop .clear_loop
    
    ; Вывод меню
    sys_write welcome_msg, welcome_len
    
    ; Чтение выбора пользователя
    sys_read input_buffer, 32
    mov al, [input_buffer]
    
    cmp al, '1'
    je config_length
    cmp al, '2'
    je config_operations
    cmp al, '3'
    je start_game
    jmp main_menu

config_length:
    sys_write config_len_msg, config_len_len
    
    sys_read input_buffer, 32
    mov al, [input_buffer]
    sub al, '0'
    
    cmp al, 1
    jl .invalid
    cmp al, 5
    jg .invalid
    
    mov [expr_length], al
    jmp main_menu
    
.invalid:
    sys_write invalid_input, invalid_len
    jmp config_length

config_operations:
    sys_write config_ops_msg, config_ops_len
    
    ; Чтение выбора операций
    sys_read input_buffer, 32
    
    ; Сначала выключаем все операции
    mov dword [enabled_ops], 0
    mov byte [enabled_ops+4], 0
    
    ; Включаем выбранные
    mov esi, input_buffer
.config_ops_loop:
    lodsb
    test al, al
    jz .config_ops_done
    cmp al, 10
    je .config_ops_done
    
    sub al, '1'
    cmp al, 4
    ja .config_ops_loop
    
    mov byte [enabled_ops+eax], 1
    jmp .config_ops_loop
    
.config_ops_done:
    jmp main_menu

start_game:
    ; Генерация выражения
    call generate_expression
    
    ; Вывод выражения
    sys_write expr_msg, expr_len
    sys_write expr_buffer, 256
    sys_write newline, newline_len
    
    ; Засекаем время
    sys_time
    mov [start_time], eax
    
    ; Получаем ответ пользователя
    sys_write input_prompt, input_len
    sys_read input_buffer, 32
    
    ; Преобразуем ввод в число
    call atoi
    mov [user_answer], eax
    
    ; Фиксируем время
    sys_time
    mov [end_time], eax
    
    ; Проверка ответа
    mov eax, [user_answer]
    cmp eax, [correct_answer]
    jne .wrong
    
    ; Правильный ответ
    sys_write correct_msg, correct_len
    jmp .show_time
    
.wrong:
    sys_write wrong_msg, wrong_len
    
    ; Вывод правильного ответа
    mov eax, [correct_answer]
    call itoa
    sys_write expr_buffer, ecx
    sys_write newline, newline_len
    
.show_time:
    ; Вывод времени
    mov eax, [end_time]
    sub eax, [start_time]
    call itoa
    sys_write expr_buffer, ecx
    sys_write newline, newline_len
    
    ; Пауза
    sys_read input_buffer, 1
    
    jmp main_menu

; Генерация случайного выражения
generate_expression:
    push ebx esi edi
    
    ; Очищаем буфер
    mov edi, expr_buffer
    xor al, al
    mov ecx, 256
    rep stosb
    
    mov edi, expr_buffer
    
    ; Генерируем выражение
    mov ecx, [expr_length]
    dec ecx  ; Количество операций
    
    ; Первое число
    call rand_num
    call append_number
    
.gen_loop:
    ; Выбираем случайную операцию
    call rand_op
    mov bl, al
    
    ; Случайное число
    call rand_num
    
    ; Добавляем операцию и число
    mov [edi], bl
    inc edi
    call append_number
    
    loop .gen_loop
    
    ; Вычисляем результат
    push expr_buffer
    call evaluate_expression
    add esp, 4
    mov [correct_answer], eax
    
    pop edi esi ebx
    ret

; Добавление числа в буфер
append_number:
    push eax ebx ecx edx
    
    ; Преобразуем число в строку
    call itoa
    mov esi, expr_buffer
    mov ecx, edx
    rep movsb
    
    pop edx ecx ebx eax
    ret

; Преобразование строки в число (atoi)
atoi:
    push ebx esi
    mov esi, input_buffer
    xor eax, eax
    xor ebx, ebx
    
.convert:
    mov bl, [esi]
    inc esi
    cmp bl, '0'
    jb .done
    cmp bl, '9'
    ja .done
    
    sub bl, '0'
    imul eax, 10
    add eax, ebx
    jmp .convert
    
.done:
    pop esi ebx
    ret

; Преобразование числа в строку (itoa)
itoa:
    push ebx esi edi
    mov edi, expr_buffer
    mov ebx, 10
    xor ecx, ecx
    
    test eax, eax
    jnz .convert
    mov byte [edi], '0'
    inc edi
    jmp .done
    
.convert:
    xor edx, edx
    div ebx
    add dl, '0'
    push edx
    inc ecx
    test eax, eax
    jnz .convert
    
.store:
    pop eax
    stosb
    loop .store
    
.done:
    mov byte [edi], 0
    mov edx, edi
    sub edx, expr_buffer
    pop edi esi ebx
    ret

; Генерация случайного числа (1-20)
rand_num:
    call rand
    xor edx, edx
    mov ecx, 20
    div ecx
    inc edx
    mov eax, edx
    ret

; Генерация случайной операции
rand_op:
    push ebx ecx
    
    ; Считаем количество доступных операций
    xor ecx, ecx
    mov ebx, enabled_ops
    mov edx, 5
    
.count_loop:
    cmp byte [ebx], 0
    je .next_op
    inc ecx
.next_op:
    inc ebx
    dec edx
    jnz .count_loop
    
    ; Если нет доступных операций, используем сложение
    test ecx, ecx
    jz .default_add
    
    ; Выбираем случайную операцию из доступных
    call rand
    xor edx, edx
    div ecx
    
    ; Находим выбранную операцию
    xor ecx, ecx
    mov ebx, enabled_ops
.find_op_loop:
    cmp byte [ebx+ecx], 0
    je .skip_op
    dec edx
    js .found_op
.skip_op:
    inc ecx
    jmp .find_op_loop
    
.found_op:
    mov al, [ops+ecx]
    jmp .done
    
.default_add:
    mov al, '+'
    
.done:
    pop ecx ebx
    ret

; Генератор случайных чисел
rand:
    mov eax, [rand_seed]
    imul eax, 1103515245
    add eax, 12345
    mov [rand_seed], eax
    shr eax, 16
    and eax, 0x7FFF
    ret

; Вычисление выражения (рекурсивный спуск)
evaluate_expression:
    push ebp
    mov ebp, esp
    
    ; Читаем первое значение
    call parse_term
    push eax
    
.eval_loop:
    ; Получаем текущий символ
    mov esi, [ebp+8]
    mov al, [esi]
    
    ; Проверяем операцию
    cmp al, '+'
    je .do_add
    cmp al, '-'
    je .do_sub
    
    ; Конец выражения
    pop eax
    jmp .done
    
.do_add:
    ; Пропускаем оператор
    inc dword [ebp+8]
    
    ; Читаем следующий терм
    call parse_term
    
    ; Выполняем сложение
    pop edx
    add eax, edx
    push eax
    jmp .eval_loop
    
.do_sub:
    ; Пропускаем оператор
    inc dword [ebp+8]
    
    ; Читаем следующий терм
    call parse_term
    
    ; Выполняем вычитание
    pop edx
    sub edx, eax
    mov eax, edx
    push eax
    jmp .eval_loop
    
.done:
    mov esp, ebp
    pop ebp
    ret

; Разбор терма (умножение/деление/степень)
parse_term:
    push ebp
    mov ebp, esp
    
    ; Читаем первое значение
    call parse_factor
    push eax
    
.term_loop:
    ; Получаем текущий символ
    mov esi, [ebp+8]
    mov al, [esi]
    
    ; Проверяем операцию
    cmp al, '*'
    je .do_mul
    cmp al, '/'
    je .do_div
    cmp al, '^'
    je .do_pow
    
    ; Конец терма
    pop eax
    jmp .done
    
.do_mul:
    ; Пропускаем оператор
    inc dword [ebp+8]
    
    ; Читаем следующий фактор
    call parse_factor
    
    ; Выполняем умножение
    pop edx
    imul eax, edx
    push eax
    jmp .term_loop
    
.do_div:
    ; Пропускаем оператор
    inc dword [ebp+8]
    
    ; Читаем следующий фактор
    call parse_factor
    
    ; Выполняем деление
    pop edx
    push eax
    mov eax, edx
    cdq
    pop ebx
    idiv ebx
    push eax
    jmp .term_loop
    
.do_pow:
    ; Пропускаем оператор
    inc dword [ebp+8]
    
    ; Читаем следующий фактор
    call parse_factor
    
    ; Выполняем возведение в степень
    pop ecx  ; степень
    mov ebx, eax  ; основание
    mov eax, 1
.pow_loop:
    test ecx, ecx
    jz .pow_done
    imul eax, ebx
    dec ecx
    jmp .pow_loop
.pow_done:
    push eax
    jmp .term_loop
    
.done:
    mov esp, ebp
    pop ebp
    ret

; Разбор фактора (число или выражение в скобках)
parse_factor:
    push ebp
    mov ebp, esp
    
    ; Получаем текущий символ
    mov esi, [ebp+8]
    mov al, [esi]
    
    ; Проверяем на скобку
    cmp al, '('
    jne .not_bracket
    
    ; Пропускаем '('
    inc dword [ebp+8]
    
    ; Рекурсивно вычисляем выражение в скобках
    call evaluate_expression
    push eax
    
    ; Пропускаем ')'
    inc dword [ebp+8]
    pop eax
    jmp .done
    
.not_bracket:
    ; Читаем число
    call parse_number
    
.done:
    mov esp, ebp
    pop ebp
    ret

; Разбор числа
parse_number:
    push ebx ecx edx
    
    mov esi, [ebp+8]
    xor eax, eax
    xor ecx, ecx
    
    ; Проверяем знак
    mov bl, [esi]
    cmp bl, '-'
    jne .digit_loop
    inc esi
    mov ecx, 1
    
.digit_loop:
    mov bl, [esi]
    sub bl, '0'
    cmp bl, 9
    ja .done_digits
    
    ; Добавляем цифру
    imul eax, 10
    add eax, ebx
    inc esi
    jmp .digit_loop
    
.done_digits:
    ; Учитываем знак
    test ecx, ecx
    jz .positive
    neg eax
    
.positive:
    ; Обновляем указатель
    mov [ebp+8], esi
    
    pop edx ecx ebx
    ret