/*
D. Секундомер на CSS (20 баллов)
Аналоговый секундомер
Нужно написать аналоговый секундомер на HTML и CSS без использования JavaScript.

Секундомер запускается и останавливается по нажатию кнопки. Пока секундомер работает, стрелки движутся; при остановке они остаются на текущем положении и продолжают движение с этого места при следующем запуске.

Формат сдачи
Решение сдаётся в одном HTML-файле, стили встраиваются через тег <style>.
Внутри .stopwatch не должно быть скрытых элементов (display: none, visibility: hidden, атрибут hidden) — в том числе у подписей кнопки «Старт» / «Стоп». Можно использовать clip-path / позиционирование.
За основу возьмите файл template.html: разметку и классы менять не нужно, допишите недостающие стили. Риски можно добавить внутрь .stopwatch__marks.

Что нужно сделать
Отрисовать циферблат с 60 минутными рисками и числами 60, 15, 30, 45. Каждая пятая риска должна быть длиннее остальных.
Добавить две стрелки - секундную и минутную.
По умолчанию стрелки стоят на месте.
При нажатии кнопки секундомер запускается; при повторном нажатии — останавливается в текущем положении (не сбрасывается в начало).
У кнопки:
до запуска — текст Старт и зелёный фон;
во время работы — текст Стоп и красный фон.
Дополнительные стили
Секундная стрелка .stopwatch__hand--seconds
Свойство	Значение
Ширина	4px
Высота	80px
Цвет	#f00
Скругление	0
Длительность полного оборота	60s
Минутная стрелка .stopwatch__hand--minutes
Свойство	Значение
Ширина	6px
Высота	56px
Цвет	#000
Скругление	0
Длительность полного оборота	3600s
Кнопка в состоянии «Стоп»
Свойство	Значение
Фон	#f00
Тень кнопки	0 4px 0 #900
При :active	тень 0 2px 0 #900
Риски на циферблате
Риски рисуются у .stopwatch__marks цветом #000: короткие — через каждую минуту (ширина 2px, высота 8%), длинные — через каждые пять минут (ширина 4px, высота 14%). Риски начинаются от внешнего края области .stopwatch__marks (в шаблоне отступ от края циферблата — 8px) и идут к центру. Цифровые обозначения остаются только в четырёх позициях: 60, 15, 30, 45.

[ Проверка ]
Откройте файл в браузере:
> Кнопка показывает «Старт», стрелки стоят.
> По клику кнопка становится «Стоп», стрелки начинают движение.
> Повторный клик останавливает стрелки на месте.
> Ещё один клик продолжает движение с того же положения.
> Автотесты проверяют совпадение скриншотов в контрольные моменты времени и выполнение ограничений.

Примечание:
Возможно, вам понадобится добавить внутрь .stopwatch__marks некоторые стили, чтобы сделать циферблат более красивым.
Для решения скачайте шаблон. Скриншот результата (начальное положение секундомера).
*/

<!doctype html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Аналоговый секундомер</title>
    <style>
      * {
        box-sizing: border-box;
        -webkit-font-smoothing: antialiased;
        text-rendering: geometricPrecision;
      }

      body {
        display: grid;
        min-height: 100vh;
        margin: 0;
        place-items: center;
        overflow: hidden;
        color: #000;
        font-family: Arial, Helvetica, sans-serif;
        background: #fff;
      }

      .stopwatch {
        display: grid;
        justify-items: center;
        gap: 16px;
      }

      .stopwatch__title {
        margin: 0;
        font-size: 20px;
        font-weight: 700;
        line-height: 1;
      }

      /* Скрытый чекбокс — без display:none, используем clip-path и позиционирование */
      .stopwatch__switch {
        position: absolute;
        width: 1px;
        height: 1px;
        margin: 0;
        padding: 0;
        border: 0;
        clip-path: inset(100%);
        clip: rect(0 0 0 0);
        overflow: hidden;
        white-space: nowrap;
      }

      .stopwatch__clock {
        position: relative;
        width: 220px;
        aspect-ratio: 1;
        border: 8px solid #000;
        border-radius: 50%;
        background: #fff;
        box-shadow: inset 0 0 0 3px #000;
      }

      .stopwatch__marks {
        position: absolute;
        inset: 8px;
        border-radius: 50%;
      }

      /* Короткие риски — каждая минута (ширина ~2px, высота 8%) */
      .stopwatch__marks::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 50%;
        background: repeating-conic-gradient(
          #000 0deg 1.125deg,
          transparent 1.125deg 6deg
        );
        -webkit-mask: radial-gradient(
          circle at center,
          transparent 0,
          transparent calc(100% - 16px),
          black calc(100% - 16px),
          black 100%
        );
        mask: radial-gradient(
          circle at center,
          transparent 0,
          transparent calc(100% - 16px),
          black calc(100% - 16px),
          black 100%
        );
      }

      /* Длинные риски — каждая пятая минута (ширина ~4px, высота 14%) */
      .stopwatch__marks::after {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 50%;
        background: repeating-conic-gradient(
          #000 0deg 2.25deg,
          transparent 2.25deg 30deg
        );
        -webkit-mask: radial-gradient(
          circle at center,
          transparent 0,
          transparent calc(100% - 28px),
          black calc(100% - 28px),
          black 100%
        );
        mask: radial-gradient(
          circle at center,
          transparent 0,
          transparent calc(100% - 28px),
          black calc(100% - 28px),
          black 100%
        );
      }

      .stopwatch__number {
        position: absolute;
        z-index: 1;
        font-size: 18px;
        font-weight: 700;
        line-height: 1;
        color: #000;
      }

      .stopwatch__number--12 {
        top: 28px;
        left: 0;
        width: 100%;
        text-align: center;
      }

      .stopwatch__number--3 {
        top: 101px;
        right: 28px;
        line-height: 18px;
      }

      .stopwatch__number--6 {
        bottom: 28px;
        left: 0;
        width: 100%;
        text-align: center;
      }

      .stopwatch__number--9 {
        top: 101px;
        left: 28px;
        line-height: 18px;
      }

      .stopwatch__hand {
        position: absolute;
        z-index: 2;
        bottom: 50%;
        left: 50%;
        transform-origin: bottom center;
      }

      .stopwatch__hand--seconds {
        width: 4px;
        height: 80px;
        margin-left: -2px; /* центрирование */
        background: #f00;
        border-radius: 0;
        animation: rotate-seconds 60s linear infinite;
        animation-play-state: paused;
      }

      .stopwatch__hand--minutes {
        width: 6px;
        height: 56px;
        margin-left: -3px;
        background: #000;
        border-radius: 0;
        animation: rotate-minutes 3600s linear infinite;
        animation-play-state: paused;
      }

      .stopwatch__pin {
        position: absolute;
        z-index: 3;
        top: 50%;
        left: 50%;
        width: 12px;
        aspect-ratio: 1;
        border: 2px solid #fff;
        border-radius: 50%;
        background: #f00;
        transform: translate(-50%, -50%);
        box-shadow: 0 0 0 2px #f00;
      }

      .stopwatch__button {
        min-width: 120px;
        padding: 10px 20px;
        border: 2px solid #000;
        border-radius: 4px;
        color: #fff;
        font-size: 16px;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        background: #0a0;
        box-shadow: 0 4px 0 #060;
        cursor: pointer;
        user-select: none;
        transition:
          transform 120ms ease,
          box-shadow 120ms ease,
          background-color 120ms ease;
      }

      .stopwatch__button::after {
        content: "Старт";
      }

      .stopwatch__button:active {
        box-shadow: 0 2px 0 #060;
        transform: translateY(2px);
      }

      /* Состояние «Стоп» */
      #stopwatch-toggle:checked ~ .stopwatch__button {
        background: #f00;
        box-shadow: 0 4px 0 #900;
      }

      #stopwatch-toggle:checked ~ .stopwatch__button::after {
        content: "Стоп";
      }

      #stopwatch-toggle:checked ~ .stopwatch__button:active {
        box-shadow: 0 2px 0 #900;
      }

      /* Запуск стрелок */
      #stopwatch-toggle:checked ~ .stopwatch__clock .stopwatch__hand--seconds,
      #stopwatch-toggle:checked ~ .stopwatch__clock .stopwatch__hand--minutes {
        animation-play-state: running;
      }

      .stopwatch__switch:focus-visible ~ .stopwatch__button {
        outline: 3px solid #00f;
        outline-offset: 3px;
      }

      @keyframes rotate-seconds {
        from {
          transform: rotate(0deg);
        }
        to {
          transform: rotate(360deg);
        }
      }

      @keyframes rotate-minutes {
        from {
          transform: rotate(0deg);
        }
        to {
          transform: rotate(360deg);
        }
      }

      @media (max-width: 300px) {
        .stopwatch__clock {
          width: 200px;
        }
      }

      @media (prefers-reduced-motion: reduce) {
        .stopwatch__button {
          transition: none;
        }
        .stopwatch__hand--seconds,
        .stopwatch__hand--minutes {
          animation: none;
        }
      }
    </style>
  </head>
  <body>
    <main class="stopwatch">
      <h1 class="stopwatch__title">Секундомер</h1>

      <!-- Скрытый чекбокс для переключения состояния -->
      <input type="checkbox" id="stopwatch-toggle" class="stopwatch__switch" />

      <div class="stopwatch__clock" aria-hidden="true">
        <div class="stopwatch__marks"></div>

        <span class="stopwatch__number stopwatch__number--12">60</span>
        <span class="stopwatch__number stopwatch__number--3">15</span>
        <span class="stopwatch__number stopwatch__number--6">30</span>
        <span class="stopwatch__number stopwatch__number--9">45</span>

        <div class="stopwatch__hand stopwatch__hand--minutes"></div>
        <div class="stopwatch__hand stopwatch__hand--seconds"></div>
        <div class="stopwatch__pin"></div>
      </div>

      <label class="stopwatch__button" for="stopwatch-toggle"></label>
    </main>
  </body>
</html>