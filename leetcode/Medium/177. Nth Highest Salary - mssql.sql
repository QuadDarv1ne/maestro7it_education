CREATE FUNCTION getNthHighestSalary (@N INT)
RETURNS INT
AS
BEGIN
    IF @N <= 0
        RETURN NULL;
    
    RETURN (
        SELECT DISTINCT salary
        FROM (
            SELECT salary, 
                   DENSE_RANK() OVER (ORDER BY salary DESC) AS rank_num
            FROM Employee
        ) AS ranked
        WHERE rank_num = @N
    );
END