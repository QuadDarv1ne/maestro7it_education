# Write your MySQL query statement below
WITH all_friendships AS (
    SELECT requester_id AS user_id, accepter_id AS friend_id 
    FROM RequestAccepted
    UNION
    SELECT accepter_id AS user_id, requester_id AS friend_id 
    FROM RequestAccepted
),
unique_friendships AS (
    SELECT DISTINCT user_id, friend_id 
    FROM all_friendships
),
friend_counts AS (
    SELECT user_id AS id, COUNT(*) AS num
    FROM unique_friendships
    GROUP BY user_id
)
SELECT id, num
FROM friend_counts
WHERE num = (SELECT MAX(num) FROM friend_counts);