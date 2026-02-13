/* Write your PL/SQL query statement below */
SELECT
    TO_CHAR(event_day, 'YYYY-MM-DD') AS day,
    emp_id,
    SUM(out_time - in_time) AS total_time
FROM Employees
GROUP BY TO_CHAR(event_day, 'YYYY-MM-DD'), emp_id;