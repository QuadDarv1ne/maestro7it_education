/* Write your PL/SQL query statement below */
SELECT
    sample_id,
    dna_sequence,
    species,
    -- has_start
    CASE WHEN REGEXP_LIKE(dna_sequence, '^ATG') THEN 1 ELSE 0 END AS has_start,
    -- has_stop
    CASE WHEN REGEXP_LIKE(dna_sequence, '(TAA|TAG|TGA)$') THEN 1 ELSE 0 END AS has_stop,
    -- has_atat
    CASE WHEN INSTR(dna_sequence, 'ATAT') > 0 THEN 1 ELSE 0 END AS has_atat,
    -- has_ggg
    CASE WHEN INSTR(dna_sequence, 'GGG') > 0 THEN 1 ELSE 0 END AS has_ggg
FROM Samples
ORDER BY sample_id;