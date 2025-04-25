--- Парсит CSV-строку в таблицу.
-- @param csv_str string CSV-данные (разделитель — запятая, строки — через `\n`).
-- @return table Таблица с распарсенными данными.
-- @example
--   parse_csv("Name,Age\nAlice,30\nBob,25") --> {{"Name", "Age"}, {"Alice", "30"}, {"Bob", "25"}}
function parse_csv(csv_str)
    local lines = {}
    for line in csv_str:gmatch("[^\n]+") do
        local row = {}
        for field in line:gmatch("([^,]+)") do
            table.insert(row, field)
        end
        table.insert(lines, row)
    end
    return lines
end