/* Write your PL/SQL query statement below */
import pandas as pd

def count_unique_subjects(teacher: pd.DataFrame) -> pd.DataFrame:
    result = teacher.groupby('teacher_id')['subject_id'].nunique().reset_index()
    result.columns = ['teacher_id', 'cnt']
    return result.sort_values(by='teacher_id')  # optional sorting