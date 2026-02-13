/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

type F = (...args: number[]) => void; // Тип для функции, которая принимает массив чисел и ничего не возвращает

/**
 * Создаёт "debounced" версию функции, которая откладывает её выполнение на `t` миллисекунд.
 * Если функция вызывается снова до истечения этого времени, предыдущий вызов отменяется.
 *
 * @param {F} fn - Исходная функция для "debounce".
 * @param {number} t - Время задержки в миллисекундах.
 * @return {F} - "Debounced" функция.
 */
function debounce(fn: F, t: number): F {
    let timeoutId: ReturnType<typeof setTimeout> | undefined;

    return function(...args: number[]) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            fn(...args);
        }, t);
    };
}