/* Write your T-SQL query statement below */
-- SQL Server не поддерживает полноценный regexp в WHERE,
-- используем комбинацию LIKE
SELECT 
    patient_id,
    patient_name,
    conditions
FROM Patients
WHERE 
    conditions LIKE 'DIAB1%' 
    OR conditions LIKE '% DIAB1%';