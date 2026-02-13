import pandas as pd

def analyze_dna_patterns(samples: pd.DataFrame) -> pd.DataFrame:
    # Копируем, чтобы не изменять исходный DataFrame
    df = samples.copy()
    
    # has_start: начинается с "ATG"
    df['has_start'] = df['dna_sequence'].str.startswith('ATG').astype(int)
    
    # has_stop: заканчивается на "TAA", "TAG" или "TGA"
    df['has_stop'] = df['dna_sequence'].str.endswith(('TAA', 'TAG', 'TGA')).astype(int)
    
    # has_atat: содержит "ATAT"
    df['has_atat'] = df['dna_sequence'].str.contains('ATAT').astype(int)
    
    # has_ggg: содержит "GGG" (три и более G подряд)
    df['has_ggg'] = df['dna_sequence'].str.contains('GGG').astype(int)
    
    # Сортировка и выбор нужных столбцов
    return df[['sample_id', 'dna_sequence', 'species', 'has_start', 'has_stop', 'has_atat', 'has_ggg']].sort_values('sample_id')