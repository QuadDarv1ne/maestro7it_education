# Write your MySQL query statement below
SELECT 
    user_id,
    name,
    mail
FROM Users
WHERE REGEXP_LIKE(mail, '^[a-zA-Z][a-zA-Z0-9_.-]*@leetcode\\.com$', 'c');