"""
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
"""

import asyncio

def debounce(fn, t):
    """
    Возвращает асинхронную функцию, которая "стабилизирует" вызовы fn.
    При каждом вызове предыдущий запланированный вызов отменяется,
    и новый планируется через t миллисекунд.
    """
    timer_task = None  # здесь будем хранить текущую запланированную задачу

    async def debounced(*args):
        nonlocal timer_task
        # Если уже есть запланированная задача, отменяем её
        if timer_task:
            timer_task.cancel()
        # Создаём новую задачу, которая запустит fn через t мс
        async def call_fn():
            await asyncio.sleep(t / 1000)  # переводим миллисекунды в секунды
            fn(*args)  # вызываем исходную функцию
        timer_task = asyncio.create_task(call_fn())

    return debounced