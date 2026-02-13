import pandas as pd

def meltTable(report: pd.DataFrame) -> pd.DataFrame:
    return pd.melt(
        report,
        id_vars=['product'],                       # столбец(ы), который остаётся без изменений
        value_vars=['quarter_1', 'quarter_2', 'quarter_3', 'quarter_4'],  # что «плавим»
        var_name='quarter',                        # новое имя для столбца с названиями
        value_name='sales'                        # новое имя для столбца со значениями
    )