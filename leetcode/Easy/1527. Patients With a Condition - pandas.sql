import pandas as pd

def find_patients(patients: pd.DataFrame) -> pd.DataFrame:
    """
    Возвращает пациентов с диагнозом, начинающимся на DIAB1.
    Диагнозы разделены пробелами.
    """
    # Проверяем: либо начало строки, либо пробел перед DIAB1
    mask = patients['conditions'].str.contains(
        r'(?:^| )DIAB1', 
        na=False, 
        regex=True
    )
    return patients[mask]