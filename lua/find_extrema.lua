--[[
Программа для поиска локальных экстремумов функции на заданном интервале.

Основная функция:
    extrema(f, a, b, n) - находит экстремумы функции f на интервале [a, b] 
    с использованием равномерной сетки из n точек.

Возвращает:
    Массив таблиц с полями x и y для каждого найденного экстремума.

Обработка ошибок:
    - При неверных аргументах генерирует ошибку с текстом "bad argument #n"
    - При ошибке в вычислении функции генерирует ошибку "bad function value"
]]

-- Функция проверки аргументов
local function check_args(f, a, b, n)
    --[[
    Проверяет корректность аргументов функции extrema.
    
    Параметры:
        f - функция (должна быть callable)
        a - начало интервала (число, должно быть < b)
        b - конец интервала (число)
        n - количество точек (целое число >= 2)
    
    Генерирует ошибку с соответствующим сообщением при неверных аргументах.
    ]]
    if type(f) ~= 'function' then
        error("bad argument #1 (function expected)")
    end
    if type(a) ~= 'number' then
        error("bad argument #2 (number expected)")
    end
    if type(b) ~= 'number' then
        error("bad argument #3 (number expected)")
    end
    if type(n) ~= 'number' or n < 2 or math.floor(n) ~= n then
        error("bad argument #4 (integer >= 2 expected)")
    end
    if a >= b then
        error("bad argument #2 (a must be less than b)")
    end
end

-- Основная функция для поиска экстремумов
function extrema(f, a, b, n)
    --[[
    Находит локальные экстремумы функции на заданном интервале.
    
    Параметры:
        f - функция одного аргумента, которую исследуем
        a - левая граница интервала
        b - правая граница интервала
        n - количество точек для разбиения интервала
    
    Возвращает:
        Массив таблиц с полями x и y для каждого экстремума
    
    Пример использования:
        local ext = extrema(function(x) return x^2 end, -1, 1, 100)
        -- вернет {{x=0, y=0}} для функции x^2
    ]]
    
    -- Проверяем аргументы
    check_args(f, a, b, n)
    
    local points = {}  -- Точки сетки
    local extrema_list = {}  -- Найденные экстремумы
    
    -- Вычисляем значения функции в точках сетки
    for i = 1, n do
        -- Вычисляем x-координату текущей точки
        local x = a + (b - a) * (i - 1) / (n - 1)
        
        -- Безопасно вызываем функцию (ловим ошибки)
        local success, y = pcall(f, x)
        
        if not success then
            error("bad function value")
        end
        
        -- Проверяем, что функция вернула число
        if type(y) ~= 'number' then
            error("bad function value")
        end
        
        -- Сохраняем точку
        points[i] = {x = x, y = y}
    end
    
    -- Ищем экстремумы (концы отрезка не рассматриваем)
    for i = 2, n - 1 do
        local prev = points[i - 1]
        local curr = points[i]
        local next = points[i + 1]
        
        -- Проверяем условия локального максимума и минимума
        if (curr.y > prev.y and curr.y > next.y) or  -- Максимум
           (curr.y < prev.y and curr.y < next.y) then -- Минимум
            table.insert(extrema_list, {x = curr.x, y = curr.y})
        end
    end
    
    return extrema_list
end

-- Основная функция программы
local function main()
    --[[
    Основной цикл программы:
    1. Читает Lua-скрипт из стандартного ввода
    2. Создает окружение с функцией extrema
    3. Выполняет скрипт
    4. Обрабатывает ошибки компиляции и выполнения
    ]]
    
    -- Читаем скрипт из stdin
    local script = io.read("*a")
    
    -- Создаем окружение с нашей функцией extrema
    local env = {
        extrema = extrema,
        -- Добавляем стандартные библиотеки
        table = table,
        math = math,
        string = string
    }
    setmetatable(env, {__index = _G})
    
    -- Загружаем и выполняем скрипт
    local chunk, err = load(script, "stdin", "t", env)
    if not chunk then
        io.stderr:write("Ошибка компиляции скрипта: ", err, "\n")
        os.exit(1)
    end
    
    local success, result = pcall(chunk)
    if not success then
        io.stderr:write("Ошибка выполнения: ", result, "\n")
        os.exit(2)
    end
    
    os.exit(0)
end

-- Запускаем программу
main()
