import pandas as pd

def find_classes(courses: pd.DataFrame) -> pd.DataFrame:
    # Group by class, count unique students, and filter
    class_counts = courses.groupby('class')['student'].nunique().reset_index()
    result = class_counts[class_counts['student'] >= 5][['class']]
    return result