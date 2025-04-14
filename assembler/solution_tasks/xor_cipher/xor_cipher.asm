; ==========================================================
; XOR-шифратор/дешифратор (DOS, 16-bit)                    ;
; Уровень: Начальный                                       ;
; Цель: Шифрование/дешифрование строки с помощью XOR-ключа ;
; Особенности:                                             ;
;   - Ввод текста и ключа через консоль                    ;
;   - Циклическое применение ключа                         ;
;   - Вывод результата в шестнадцатеричном виде            ;
; Пример вызова: Запустить в DOSBox, ввести текст и ключ   ;
; ==========================================================

org 0x100        ; Формат COM-файла
jmp start

; Данные
msg_prompt      db 0Dh,0Ah,'Введите текст: $'
key_prompt      db 0Dh,0Ah,'Введите ключ: $'
result_msg      db 0Dh,0Ah,'Результат: $'
error_msg       db 0Dh,0Ah,'Ошибка: ключ не может быть пустым!$'

text_buf        db 100        ; Максимальная длина текста (99 символов + 0Dh)
text_len        db 0          ; Фактическая длина текста
text            times 100 db 0

key_buf         db 50         ; Максимальная длина ключа
key_len         db 0          ; Фактическая длина ключа
key             times 50 db 0

hex_table       db '0123456789ABCDEF'  ; Таблица для HEX-вывода

;---------------------------------------
; Основная программа                   ;
;---------------------------------------
start:
    ; Ввод текста
    mov ah, 9
    mov dx, msg_prompt
    int 21h

    mov ah, 0Ah
    mov dx, text_buf
    int 21h

    ; Ввод ключа
    mov ah, 9
    mov dx, key_prompt
    int 21h

    mov ah, 0Ah
    mov dx, key_buf
    int 21h

    ; Проверка, что ключ не пустой
    cmp byte [key_len], 0
    je .error

    ; Применение XOR
    call xor_cipher

    ; Вывод результата
    mov ah, 9
    mov dx, result_msg
    int 21h
    call print_hex

    jmp .exit

.error:
    mov ah, 9
    mov dx, error_msg
    int 21h

.exit:
    mov ax, 0x4C00
    int 21h

;---------------------------------------
; Процедура XOR-шифрования             ;
;---------------------------------------
xor_cipher:
    movzx cx, byte [text_len]  ; Длина текста
    test cx, cx
    jz .done

    mov si, 0                  ; Индекс текста
    mov di, 0                  ; Индекс ключа

.loop:
    ; Получить символ ключа (циклически)
    mov al, [key + di]
    inc di
    cmp di, [key_len]
    jb .skip_reset
    xor di, di                 ; Сброс индекса ключа
.skip_reset:

    ; Применить XOR к тексту
    xor [text + si], al
    inc si
    loop .loop

.done:
    ret

;---------------------------------------
; Вывод текста в HEX-формате           ;
;---------------------------------------
print_hex:
    movzx cx, byte [text_len]
    test cx, cx
    jz .exit

    mov si, 0
.next_char:
    mov al, [text + si]
    mov bl, al

    ; Преобразование старшего полубайта
    shr al, 4
    movzx bx, al
    mov ah, 2
    mov dl, [hex_table + bx]
    int 21h

    ; Преобразование младшего полубайта
    mov al, [text + si]
    and al, 0Fh
    movzx bx, al
    mov dl, [hex_table + bx]
    int 21h

    ; Пробел между байтами
    mov dl, ' '
    int 21h

    inc si
    loop .next_char

.exit:
    ret
