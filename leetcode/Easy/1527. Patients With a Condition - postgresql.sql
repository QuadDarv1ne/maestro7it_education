-- Write your PostgreSQL query statement below
SELECT 
    patient_id,
    patient_name,
    conditions
FROM Patients
WHERE 
    conditions ~ '^DIAB1| DIAB1';