--- Генерирует случайный пароль заданной длины.
-- @param length integer Длина пароля.
-- @return string Случайный пароль.
-- @example
--   generate_password(8) --> "aB3!kL9@"
function generate_password(length)
    local chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    local password = ""
    math.randomseed(os.time())
    for i = 1, length do
        local rand_index = math.random(1, #chars)
        password = password .. chars:sub(rand_index, rand_index)
    end
    return password
end