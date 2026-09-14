/* C. Живой четырехугольник (40 баллов)
cover

В старом городе стоит световое табло, на котором горит одна-единственная фигура — четырёхугольник. Жители прозвали его живым: за долгие годы четырёхугольник менял цвета к праздникам, наливался толстой рамкой в дни штормовых предупреждений и скруглял углы, когда город хотел казаться добрее. Управляют им операторы с разных концов города, и каждый шлёт свои распоряжения по старым телеграфным линиям — буква за буквой, кто-то быстро, кто-то еле-еле. Иногда их указания противоречат друг другу, и тогда табло слушается самого свежего приказа. А по сигналу городского фотографа фигура обязана застыть ровно такой, какой её к этому мгновению успели сделать долетевшие распоряжения. Недавно управляющий блок табло сгорел, и вам предстоит написать новый.

Вам нужно реализовать функцию renderQuadrilateral(streams, root, config).

На странице есть пустой DOM-элемент root. Через несколько асинхронных потоков в функцию приходят символы команд. Команды меняют характеристики четырёхугольника, а специальный символ ! фиксирует кадр: в этот момент на экране должно быть отрисовано актуальное состояние фигуры.

Проверка выполняется поскриншотно. Способ отрисовки свободный: можно использовать SVG, HTML/CSS, canvas или любой другой браузерный DOM-подход без внешних зависимостей.

API

async function renderQuadrilateral(streams, root, config) {
  // streams: Array<AsyncIterable<string>>
  // root: HTMLElement
  // config: {
  //   width: number,
  //   height: number,
  //   initial: {
  //     bg: [number, number, number],
  //     borderColor: [number, number, number],
  //     borderWidth: number,
  //     radius: number,
  //     p1: [number, number],
  //     p2: [number, number],
  //     p3: [number, number],
  //     p4: [number, number]
  //   }
  // }
}
Аргументы:

streams — массив асинхронных потоков символов (AsyncIterable<string>). Один элемент итератора — один символ команды (включая !). Читаются через for await; символы могут приходить с задержками, потоки нужно обрабатывать параллельно.
root — пустой DOM-элемент, внутри которого нужно отрисовывать фигуру.
config — размеры области отрисовки width и height (в пикселях) и начальное состояние фигуры initial: цвета bg и borderColor — массивы RGB [r, g, b] со значениями 0-255, borderWidth и radius — числа в пикселях, p1-p4 — точки [x, y] в пикселях.
Функция может вернуть Promise.

Состояние
Фигура описывается такими характеристиками:

bg — цвет заливки в RGB.
borderColor — цвет рамки в RGB.
borderWidth — ширина рамки в пикселях.
radius — радиус скругления углов в пикселях.
p1, p2, p3, p4 — четыре точки четырёхугольника.
Изначальное состояние передаётся в config.initial.

Формат команд
Каждая команда имеет вид:


#<seq> <key>=<value>;
Примеры:


#1 bg=255,240,220;
#2 p1=80,70;
#3 borderWidth=8;
#4 borderColor=20,20,20;
#5 radius=18;
!
Потоки являются потоками символов: один элемент async-итератора — один символ. Команда может приходить медленно и параллельно с командами из других потоков. Команда считается готовой только после символа ;.

Символ ! — commit marker. Когда он пришёл, нужно немедленно отрисовать все полностью полученные и применённые к этому моменту команды. Незавершённая команда без ; на commit не применяется.

Разрешение конфликтов
Порядок выполнения нескольких потоков не должен влиять на результат.

Для каждого свойства применяется команда с максимальным seq. Если для одного свойства пришло несколько команд с одинаковым seq, побеждает лексикографически минимальное нормализованное значение.

Например, для bg при одинаковом seq значение 10,20,30 побеждает значение 90,90,90, потому что строка "10,20,30" меньше строки "90,90,90".

Команды с меньшим seq для уже обновлённого свойства игнорируются.

Геометрия
Точки p1, p2, p3, p4 задают произвольный четырёхугольник в этом порядке. Это не обязательно квадрат.

Скругление углов должно быть визуально похоже на CSS border-radius, но для четырёхугольника. Если радиус слишком большой для соседних сторон, его нужно ограничить половиной длины ближайшей стороны.

Требования
Нужно обрабатывать все потоки параллельно.
Нельзя ждать завершения всех потоков перед первым commit.
Нужно корректно буферизовать команды до ;.
На каждый символ ! состояние на экране должно соответствовать всем завершённым командам, известным на этот момент.
Рендер должен помещаться в область config.width x config.height.
*/

async function renderQuadrilateral(streams, root, config) {
  const { width, height, initial } = config;

  const state = {
    bg: [...initial.bg],
    borderColor: [...initial.borderColor],
    borderWidth: initial.borderWidth,
    radius: initial.radius,
    p1: [...initial.p1],
    p2: [...initial.p2],
    p3: [...initial.p3],
    p4: [...initial.p4],
  };

  const propNames = ['bg', 'borderColor', 'borderWidth', 'radius', 'p1', 'p2', 'p3', 'p4'];
  const maxSeq = {};
  const maxValue = {};
  propNames.forEach(p => {
    maxSeq[p] = -Infinity;
    maxValue[p] = '';
  });

  const applyCommand = (cmd) => {
    let str = cmd.trim();
    if (str.startsWith('#')) {
      str = str.slice(1);
    }
    const match = str.match(/^(\d+)\s+([^=]+)=(.*)$/);
    if (!match) return;

    const seq = parseInt(match[1], 10);
    const key = match[2].trim();
    const value = match[3].trim();

    if (!propNames.includes(key)) return;

    if (seq > maxSeq[key] || (seq === maxSeq[key] && value < maxValue[key])) {
      maxSeq[key] = seq;
      maxValue[key] = value;

      switch (key) {
        case 'bg':
        case 'borderColor':
          state[key] = value.split(',').map(Number);
          break;
        case 'borderWidth':
        case 'radius':
          state[key] = Number(value);
          break;
        case 'p1':
        case 'p2':
        case 'p3':
        case 'p4':
          state[key] = value.split(',').map(Number);
          break;
      }
    }
  };

  const render = () => {
    root.innerHTML = '';
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    root.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    const pts = [state.p1, state.p2, state.p3, state.p4];
    const radius = state.radius;
    const borderWidth = state.borderWidth;

    const bgColor = `rgb(${state.bg[0]},${state.bg[1]},${state.bg[2]})`;
    const borderColor = `rgb(${state.borderColor[0]},${state.borderColor[1]},${state.borderColor[2]})`;

    const pointOnSegment = (from, to, dist) => {
      const dx = to[0] - from[0];
      const dy = to[1] - from[1];
      const len = Math.hypot(dx, dy);
      if (len === 0) return [...from];
      const t = dist / len;
      return [from[0] + dx * t, from[1] + dy * t];
    };

    // Ограничиваем радиус для каждого угла половинами длин прилежащих сторон
    const radii = pts.map((p, i) => {
      const prev = pts[(i + 3) % 4];
      const next = pts[(i + 1) % 4];
      const lenPrev = Math.hypot(prev[0] - p[0], prev[1] - p[1]);
      const lenNext = Math.hypot(next[0] - p[0], next[1] - p[1]);
      return Math.min(radius, lenPrev / 2, lenNext / 2);
    });

    ctx.beginPath();

    // Стартовая точка на стороне p2 -> p1 на расстоянии radii[1] от p2
    const start = pointOnSegment(pts[1], pts[0], radii[1]);
    ctx.moveTo(start[0], start[1]);

    for (let i = 1; i <= 4; i++) {
      const currIdx = i % 4;
      const prevIdx = (currIdx + 3) % 4;
      const nextIdx = (currIdx + 1) % 4;
      const curr = pts[currIdx];
      const prev = pts[prevIdx];
      const next = pts[nextIdx];
      const rad = radii[currIdx];

      if (rad > 0) {
        const before = pointOnSegment(curr, prev, rad);
        const after = pointOnSegment(curr, next, rad);
        ctx.lineTo(before[0], before[1]);
        ctx.arcTo(curr[0], curr[1], after[0], after[1], rad);
      } else {
        ctx.lineTo(curr[0], curr[1]);
      }
    }
    ctx.closePath();

    ctx.fillStyle = bgColor;
    ctx.fill();
    if (borderWidth > 0) {
      ctx.strokeStyle = borderColor;
      ctx.lineWidth = borderWidth;
      ctx.stroke();
    }
  };

  // Начальная отрисовка
  render();

  // Обработка всех потоков параллельно
  const readers = streams.map(async (stream) => {
    let buffer = '';
    for await (const char of stream) {
      if (char === ';') {
        if (buffer.trim()) {
          applyCommand(buffer);
        }
        buffer = '';
      } else if (char === '!') {
        render();
        // буфер остаётся для незавершённой команды
      } else {
        buffer += char;
      }
    }
  });

  await Promise.all(readers);
}
