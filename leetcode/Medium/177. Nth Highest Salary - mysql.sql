CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
    IF N <= 0 THEN
        RETURN NULL;
    END IF;
    
    RETURN (
        SELECT DISTINCT salary
        FROM Employee
        ORDER BY salary DESC
        LIMIT 1 OFFSET N-1
    );
END