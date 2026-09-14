/*
A. Управление задачами (40 баллов)
Крупный инженерный объект должен быть сдан в установленный срок. Для завершения проекта необходимо выполнить множество работ: провести изыскания, подготовить проектную документацию, проверить коммуникации, смонтировать оборудование и наладить системы связи. Некоторые работы можно выполнять независимо, другие разрешается начинать только после завершения предшествующих этапов.

Срок сдачи ограничен: каждый час простоя повышает риск задержки. При этом число бригад на площадке также ограничено. Невозможно выполнять неограниченное количество работ одновременно, но и оставлять бригады без дела, когда есть готовые к запуску этапы, нельзя.

Вы — диспетчер строительного участка. Руководство передало вам список работ и зависимостей между ними. Необходимо разработать планировщик, который запускает доступные работы как можно раньше, соблюдая их зависимости и ограничение на число одновременно работающих бригад.

Если в плане обнаружена ошибка — например, зависимость от несуществующей работы или замкнутая цепочка зависимостей, — выполнение должно быть остановлено: реализовать такой план невозможно.

От правильного распределения ресурсов и точности планирования зависит, будет ли объект сдан вовремя.

Условие
Напишите асинхронную функцию runTasks(tasks, options), которая выполняет строительные работы с учётом зависимостей и возвращает результаты всех этапов.


async function runTasks(tasks, options) {
  // Your code here...
}

module.exports = runTasks;
Входные данные
tasks — массив объектов следующего вида:


{
  id: "inspect-communications",
  deps: ["prepare-project-documents"],
  run: async (depResults) => value
}
Поля объекта:
id — уникальный строковый идентификатор работы;
deps — массив идентификаторов работ, которые должны завершиться до начала текущей;
run — асинхронная функция, которую нужно вызвать после завершения всех зависимостей.
В run(depResults) необходимо передать объект, содержащий результаты только тех работ, от которых непосредственно зависит текущая:


{
  [depId]: result
}
options — необязательный объект:


{
  concurrency: number
}
Параметр concurrency ограничивает число работ, выполняемых одновременно. Если concurrency не передан, ограничений на параллельное выполнение нет.

Результат
Функция должна вернуть объект следующего вида:


{
  [id]: result
}
Работы без зависимостей можно начинать сразу. После завершения работы становятся доступны все этапы, для которых она была последней незавершённой зависимостью.

Важно: независимые готовые работы необходимо запускать параллельно, если это позволяют число свободных бригад и значение concurrency.

Ошибки
Функция должна выбросить ошибку в следующих случаях:

если две работы имеют одинаковый id:


new Error("duplicate task id: <id>")
если работа ссылается на неизвестную зависимость:


new Error("unknown dependency: <id>")
если план содержит цикл зависимостей:


new Error("cycle detected")
если выполнение run одной из работ завершилось ошибкой, runTasks должна завершиться с этой же ошибкой. Работы, зависящие от неудачно завершившегося этапа, запускать нельзя.

Входной массив tasks и содержащиеся в нём объекты изменять нельзя.

Примеры
Пример 1

const tasks = [
  {
    id: "prepare-project-documents",
    deps: [],
    run: async () => "documents",
  },
  {
    id: "inspect-communications",
    deps: ["prepare-project-documents"],
    run: async (deps) =>
      `inspected using: ${deps["prepare-project-documents"]}`,
  },
];

await runTasks(tasks);
// {
//   "prepare-project-documents": "documents",
//   "inspect-communications": "inspected using: documents"
// }
Пример 2

const tasks = [
  {
    id: "prepare-documents",
    deps: [],
    run: async () => "documents",
  },
  {
    id: "inspect-site",
    deps: [],
    run: async () => "site inspected",
  },
  {
    id: "begin-installation",
    deps: ["prepare-documents", "inspect-site"],
    run: async (deps) =>
      `${deps["prepare-documents"]}, ${deps["inspect-site"]}`,
  },
];

await runTasks(tasks);
// {
//   "prepare-documents": "documents",
//   "inspect-site": "site inspected",
//   "begin-installation": "documents, site inspected"
// }
Работы prepare-documents и inspect-site должны начаться одновременно, если значение concurrency это позволяет.

Пример 3

const tasks = [
  {
    id: "inspect-site",
    deps: [],
    run: async () => "site inspected",
  },
  {
    id: "check-communications",
    deps: [],
    run: async () => "communications checked",
  },
  {
    id: "deliver-equipment",
    deps: [],
    run: async () => "equipment delivered",
  },
];

await runTasks(tasks, { concurrency: 2 });
// {
//   "inspect-site": "site inspected",
//   "check-communications": "communications checked",
//   "deliver-equipment": "equipment delivered"
// }
Все три работы готовы к запуску сразу. При concurrency: 2 планировщик запускает две из них одновременно. Третья начнётся после завершения одной из первых двух. В каждый момент времени выполняется не более двух работ.

Пример 4

const tasks = [
  {
    id: "inspect-site",
    deps: [],
    run: async () => "site inspected",
  },
  {
    id: "check-communications",
    deps: [],
    run: async () => "communications checked",
  },
  {
    id: "deliver-equipment",
    deps: [],
    run: async () => "equipment delivered",
  },
];

await runTasks(tasks, { concurrency: 1 });
При concurrency: 1 одновременно работает только одна строительная бригада.

Пример 5

const tasks = [
  {
    id: "approve-project",
    deps: ["prepare-project"],
    run: async () => "approved",
  },
  {
    id: "prepare-project",
    deps: ["approve-project"],
    run: async () => "prepared",
  },
];

await runTasks(tasks);
// throws Error("cycle detected")
Ограничения
0 <= tasks.length <= 1000;
0 <= deps.length <= 1000;
если параметр concurrency передан, то 1 <= concurrency;
все работы возвращают JSON-сериализуемые результаты.
*/

async function runTasks(tasks, options) {
  const concurrency = options && options.concurrency !== undefined
    ? options.concurrency
    : Infinity;

  // 1. Проверка на дубликаты id
  const taskMap = new Map();
  for (const task of tasks) {
    if (taskMap.has(task.id)) {
      throw new Error(`duplicate task id: ${task.id}`);
    }
    taskMap.set(task.id, task);
  }

  // 2. Построение графа зависимостей
  const graph = new Map(); // id -> { task, indegree, dependents, deps, status, result }
  for (const task of tasks) {
    graph.set(task.id, {
      task,
      indegree: task.deps.length,
      dependents: [],
      deps: [...task.deps],
      status: 'pending',
      result: undefined,
    });
  }

  // Проверка неизвестных зависимостей и заполнение dependents
  for (const task of tasks) {
    const node = graph.get(task.id);
    for (const depId of task.deps) {
      if (!graph.has(depId)) {
        throw new Error(`unknown dependency: ${depId}`);
      }
      graph.get(depId).dependents.push(node);
    }
  }

  // 3. Проверка циклов (алгоритм Кана)
  const indegreeCopy = new Map();
  for (const [id, node] of graph) {
    indegreeCopy.set(id, node.indegree);
  }
  const queue = [];
  for (const [id, deg] of indegreeCopy) {
    if (deg === 0) queue.push(id);
  }
  let processed = 0;
  while (queue.length > 0) {
    const id = queue.shift();
    processed++;
    const node = graph.get(id);
    for (const dependent of node.dependents) {
      const newDeg = indegreeCopy.get(dependent.task.id) - 1;
      indegreeCopy.set(dependent.task.id, newDeg);
      if (newDeg === 0) {
        queue.push(dependent.task.id);
      }
    }
  }
  if (processed !== tasks.length) {
    throw new Error("cycle detected");
  }

  // 4. Планировщик выполнения
  const readyQueue = []; // массив узлов, готовых к запуску
  let runningCount = 0;
  const results = {};
  let globalError = null;

  let resolvePromise, rejectPromise;
  const promise = new Promise((resolve, reject) => {
    resolvePromise = resolve;
    rejectPromise = reject;
  });

  // Запуск одной задачи
  const launchTask = async (node) => {
    if (globalError) return;
    node.status = 'running';
    runningCount++;

    // Собираем результаты непосредственных зависимостей
    const depResults = {};
    for (const depId of node.deps) {
      depResults[depId] = graph.get(depId).result;
    }

    try {
      const result = await node.task.run(depResults);
      if (globalError) return; // уже произошла ошибка в другом месте
      node.result = result;
      node.status = 'done';
      results[node.task.id] = result;
    } catch (err) {
      if (!globalError) {
        globalError = err;
        rejectPromise(err);
      }
      return;
    } finally {
      runningCount--;

      // Если ошибок нет, уменьшаем indegree у зависимых задач
      if (!globalError) {
        for (const dependent of node.dependents) {
          dependent.indegree--;
          if (dependent.indegree === 0) {
            readyQueue.push(dependent);
          }
        }
      }

      // Пытаемся запустить следующие задачи
      schedule();
    }
  };

  // Планирование запуска задач из очереди готовых
  const schedule = () => {
    if (globalError) return;

    while (runningCount < concurrency && readyQueue.length > 0) {
      const nextNode = readyQueue.shift();
      launchTask(nextNode);
    }

    // Если все задачи завершены и нет ошибок
    if (runningCount === 0 && readyQueue.length === 0 && !globalError) {
      const allDone = [...graph.values()].every(node => node.status === 'done');
      if (allDone) {
        resolvePromise(results);
      }
    }
  };

  // Инициализация очереди готовых задач
  for (const [id, node] of graph) {
    if (node.indegree === 0) {
      readyQueue.push(node);
    }
  }

  schedule();

  return promise;
}

module.exports = runTasks;