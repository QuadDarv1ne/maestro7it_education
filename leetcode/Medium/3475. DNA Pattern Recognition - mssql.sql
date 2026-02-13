/* Write your T-SQL query statement below */
SELECT
    sample_id,
    dna_sequence,
    species,
    -- has_start
    CASE WHEN dna_sequence LIKE 'ATG%' THEN 1 ELSE 0 END AS has_start,
    -- has_stop (RIGHT работает только с фиксированной длиной, LIKE надёжнее)
    CASE WHEN dna_sequence LIKE '%TAA' 
           OR dna_sequence LIKE '%TAG' 
           OR dna_sequence LIKE '%TGA' THEN 1 ELSE 0 END AS has_stop,
    -- has_atat
    CASE WHEN dna_sequence LIKE '%ATAT%' THEN 1 ELSE 0 END AS has_atat,
    -- has_ggg
    CASE WHEN dna_sequence LIKE '%GGG%' THEN 1 ELSE 0 END AS has_ggg
FROM Samples
ORDER BY sample_id;