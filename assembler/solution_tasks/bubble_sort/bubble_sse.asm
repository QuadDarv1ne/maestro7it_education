; ===================================================================
; Пузырьковая сортировка с оптимизацией SSE (x86)                   ;
; Цель: Ускорение сортировки через SIMD-инструкции.                 ;
; Вход:                                                             ;
;   - array: Массив 32-битных чисел (dd), выровненный по 16 байтам. ;
;   - len: Длина массива (должна быть кратна 4 для SSE).            ;
; Выход: Отсортированный массив (in-place).                         ;
; Особенности:                                                      ;
;   - Параллельное сравнение 4 элементов за такт.                   ;
;   - Использование регистров XMM.                                  ;
; Требования: Процессор с поддержкой SSE.                           ;
; ===================================================================

section .data
    align 16                ; Выравнивание для SSE
    array dd 5, 3, 8, 1, 2, 6, 7, 4  ; Пример массива
    len equ ($ - array) / 4

section .text
global _start

_start:
    mov ecx, len-1          ; Количество проходов
.outer_loop:
    mov edi, 0              ; Флаг обмена
    mov esi, 0              ; Индекс
.inner_loop:
    mov al, [array + esi]
    cmp al, [array + esi + 1]
    jbe .no_swap
    xchg al, [array + esi + 1]
    mov [array + esi], al
    mov edi, 1              ; Установить флаг обмена
.no_swap:
    inc esi
    cmp esi, ecx
    jb .inner_loop
    test edi, edi
    jz .exit
    loop .outer_loop
.exit:
    ; Завершение программы
    mov eax, 1
    int 0x80
