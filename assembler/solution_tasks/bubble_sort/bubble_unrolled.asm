; ================================================================
; Пузырьковая сортировка с развернутыми циклами (x86)            ;
; Цель: Снижение накладных расходов за счет уменьшения итераций. ;
; Вход:                                                          ;
;   - array: Массив байт (db).                                   ;
;   - len: Длина массива.                                        ;
; Выход: Отсортированный массив (in-place).                      ;
; Особенности:                                                   ;
;   - Обработка 4 элементов за одну итерацию внутреннего цикла.  ;
;   - Уменьшение числа проверок условий.                         ;
; ================================================================

section .data
    array db 5, 3, 8, 1, 2, 9, 0, 4  ; Пример массива
    len equ $ - array

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
