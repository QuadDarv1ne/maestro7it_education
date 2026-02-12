/* Write your T-SQL query statement below */
-- Используем COLLATE для регистрозависимого сравнения домена
SELECT 
    user_id,
    name,
    mail
FROM Users
WHERE 
    -- префикс начинается с буквы
    LEFT(mail, LEN(mail) - 13) LIKE '[A-Za-z]%'
    -- префикс содержит только разрешённые символы
    AND LEFT(mail, LEN(mail) - 13) NOT LIKE '%[^A-Za-z0-9_.-]%' ESCAPE '\'
    -- домен ТОЧНО '@leetcode.com' (регистрозависимо)
    AND mail COLLATE SQL_Latin1_General_CP1_CS_AS LIKE '%@leetcode.com'
    -- длина > 13, чтобы префикс не был пустым
    AND LEN(mail) > 13;