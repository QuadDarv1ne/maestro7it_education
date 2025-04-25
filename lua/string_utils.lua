--- Разворачивает строку.
-- @param str string Исходная строка.
-- @return string Развёрнутая строка.
-- @example
--   reverse_string("Lua") --> "auL"
function reverse_string(str)
    return str:reverse()
end



--- Проверяет, является ли строка палиндромом.
-- @param str string Строка для проверки.
-- @return boolean `true`, если палиндром, иначе `false`.
-- @example
--   is_palindrome("racecar") --> true
--   is_palindrome("hello")   --> false
function is_palindrome(str)
    return str == reverse_string(str)
end