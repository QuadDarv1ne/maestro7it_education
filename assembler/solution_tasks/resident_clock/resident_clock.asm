; =======================================================
; Резидентные часы для DOS (NASM, 16-bit)               ;
; Уровень: Продвинутый                                  ;
; Особенности:                                          ;
;   - Перехват int 1Ch (таймер) и int 09h (клавиатура)  ;
;   - Прямая работа с видеопамятью                      ;
;   - Горячие клавиши: Ctrl+Alt+T/Q                     ;
; =======================================================

org 0x100
jmp install

; Данные
old_int1Ch dd 0          ; Старый обработчик int 1Ch
old_int09h dd 0          ; Старый обработчик клавиатуры
is_active db 1           ; Флаг активности (1 = включено)
video_seg equ 0xB800     ; Сегмент видеопамяти
time_str db 'HH:MM:SS',0 ; Шаблон времени
color db 0x1E            ; Цвет текста (желтый на синем)

;--------------------------------------;
; Установка резидентной части          ;
;--------------------------------------;
install:
    ; Проверка, уже установлено ли
    mov ax, 0x1C00
    int 21h
    cmp byte [es:di], 0xFE ; Метка резидентной программы
    je already_installed

    ; Перехват int 1Ch (таймер)
    mov ax, 0x351C
    int 21h
    mov [old_int1Ch], bx
    mov [old_int1Ch + 2], es

    mov dx, new_int1Ch
    mov ax, 0x251C
    int 21h

    ; Перехват int 09h (клавиатура)
    mov ax, 0x3509
    int 21h
    mov [old_int09h], bx
    mov [old_int09h + 2], es

    mov dx, new_int09h
    mov ax, 0x2509
    int 21h

    ; Сообщение об успехе
    mov dx, installed_msg
    mov ah, 9
    int 21h

    ; Оставить резидентную часть в памяти
    mov dx, (install_end - install) / 16 + 1
    mov ax, 0x3100
    int 21h

already_installed:
    mov dx, already_msg
    mov ah, 9
    int 21h
    mov ax, 0x4C00
    int 21h

;--------------------------------------;
; Новый обработчик int 1Ch (таймер)    ;
;--------------------------------------;
new_int1Ch:
    pushf
    cmp byte [cs:is_active], 0
    je .exit
    call update_time
.exit:
    jmp far [cs:old_int1Ch] ; Цепочка к старому обработчику

;--------------------------------------;
; Обновление времени на экране         ;
;--------------------------------------;
update_time:
    pusha
    push es
    mov ax, video_seg
    mov es, ax

    ; Получить время через BIOS
    mov ah, 0x02
    int 0x1A          ; CH = часы, CL = минуты, DH = секунды

    ; Конвертировать в ASCII
    mov di, time_str
    call convert_bcd  ; Часы
    inc di
    call convert_bcd  ; Минуты
    inc di
    call convert_bcd  ; Секунды

    ; Вывод в видеопамять (позиция X=60, Y=0)
    mov si, time_str
    mov di, 60 * 2    ; 60 символов * 2 байта (символ + атрибут)
    mov cx, 8         ; Длина строки 'HH:MM:SS'
    mov ah, [color]
.loop:
    lodsb
    stosw             ; ES:DI <- AX (символ + цвет)
    loop .loop

    pop es
    popa
    ret

;--------------------------------------;
; Обработчик клавиатуры (int 09h)      ;
;--------------------------------------;
new_int09h:
    pushf
    push ax
    in al, 0x60       ; Считать скан-код

    ; Проверка на Ctrl+Alt+T
    cmp al, 0x14      ; Скан-код 'T'
    jne .check_q
    mov ah, 0x02      ; Проверить состояние клавиш-модификаторов
    int 0x16
    and al, 0x0C      ; Ctrl + Alt
    cmp al, 0x0C
    jne .chain
    not byte [cs:is_active] ; Переключить флаг активности
    jmp .eoi

.check_q:
    cmp al, 0x10      ; Скан-код 'Q'
    jne .chain
    mov ah, 0x02
    int 0x16
    and al, 0x0C
    cmp al, 0x0C
    jne .chain
    call uninstall

.eoi:
    in al, 0x61       ; Подтвердить обработку клавиши
    or al, 0x80
    out 0x61, al
    and al, 0x7F
    out 0x61, al
    mov al, 0x20
    out 0x20, al
    pop ax
    popf
    iret

.chain:
    pop ax
    popf
    jmp far [cs:old_int09h] ; Стандартный обработчик

;--------------------------------------;
; Выгрузка программы из памяти         ;
;--------------------------------------;
uninstall:
    ; Восстановить исходные обработчики
    mov dx, [old_int1Ch]
    mov ds, [old_int1Ch + 2]
    mov ax, 0x251C
    int 21h

    mov dx, [old_int09h]
    mov ds, [old_int09h + 2]
    mov ax, 0x2509
    int 21h

    ; Освободить память
    mov es, [cs:0x2C] ; Сегмент окружения
    mov ah, 0x49
    int 21h

    mov ax, 0x4C00
    int 21h

;--------------------------------------;
; Вспомогательные функции              ;
;--------------------------------------;
convert_bcd:
    ; Вход: CH (часы), CL (минуты), DH (секунды)
    ; Выход: time_str в формате ASCII
    ret

installed_msg db 'Часы установлены! Ctrl+Alt+T/Q', 0Dh, 0Ah, '$'
already_msg db 'Программа уже резидент!', 0Dh, 0Ah, '$'

install_end:
