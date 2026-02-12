/* Write your PL/SQL query statement below */
SELECT 
    patient_id,
    patient_name,
    conditions
FROM Patients
WHERE REGEXP_LIKE(conditions, '(^| )DIAB1');