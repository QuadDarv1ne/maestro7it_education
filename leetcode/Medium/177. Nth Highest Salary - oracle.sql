CREATE OR REPLACE FUNCTION getNthHighestSalary(N IN NUMBER) 
RETURN NUMBER
IS
    result_salary NUMBER;
BEGIN
    IF N <= 0 THEN
        RETURN NULL;
    END IF;
    
    SELECT salary INTO result_salary
    FROM (
        SELECT DISTINCT salary,
               DENSE_RANK() OVER (ORDER BY salary DESC) as rnk
        FROM Employee
    )
    WHERE rnk = N
    AND ROWNUM = 1;
    
    RETURN result_salary;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN NULL;
END;