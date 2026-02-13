-- Write your PostgreSQL query statement below
SELECT
    sample_id,
    dna_sequence,
    species,
    (dna_sequence LIKE 'ATG%')::int AS has_start,
    (dna_sequence LIKE '%TAA' OR dna_sequence LIKE '%TAG' OR dna_sequence LIKE '%TGA')::int AS has_stop,
    (dna_sequence LIKE '%ATAT%')::int AS has_atat,
    (dna_sequence LIKE '%GGG%')::int AS has_ggg
FROM Samples
ORDER BY sample_id;