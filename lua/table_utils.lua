--- Создаёт глубокую копию таблицы (копирует все вложенные таблицы).
-- @param tbl table Исходная таблица.
-- @return table Новая таблица (не связана с исходной).
-- @example
--   local t1 = {a = 1, b = {c = 2}}
--   local t2 = deep_copy(t1)
--   t2.b.c = 100
--   print(t1.b.c) --> 2 (не изменилось)
function deep_copy(tbl)
    if type(tbl) ~= "table" then return tbl end
    local copy = {}
    for k, v in pairs(tbl) do
        copy[deep_copy(k)] = deep_copy(v)
    end
    return copy
end