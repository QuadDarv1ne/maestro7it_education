-- Пример теста
local result = extrema(function(x) return x*x end, -1, 1, 100)
for _, ext in ipairs(result) do
    print("Экстремум в x = "..ext.x..", y = "..ext.y)
end