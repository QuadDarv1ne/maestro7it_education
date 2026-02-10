import pandas as pd

def human_traffic(stadium: pd.DataFrame) -> pd.DataFrame:
    # Filter rows
    df = stadium[stadium['people'] >= 100].copy()
    
    # Sort by id for consecutive calculation
    df = df.sort_values('id').reset_index(drop=True)
    
    # Create group identifier (id - row_number)
    df['row_num'] = range(1, len(df) + 1)
    df['grp'] = df['id'] - df['row_num']
    
    # Count rows per group
    df['cnt'] = df.groupby('grp')['id'].transform('count')
    
    # Filter groups with at least 3 rows
    result = df[df['cnt'] >= 3][['id', 'visit_date', 'people']]
    
    # Sort by visit_date
    result = result.sort_values('visit_date')
    
    return result