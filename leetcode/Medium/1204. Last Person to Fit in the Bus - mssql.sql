/* Write your T-SQL query statement below */
WITH CumulativeWeights AS (
    SELECT 
        person_name,
        turn,
        weight,
        SUM(weight) OVER (ORDER BY turn) AS cumulative_weight
    FROM Queue
)
SELECT person_name
FROM CumulativeWeights
WHERE cumulative_weight <= 1000
ORDER BY turn DESC
LIMIT 1;