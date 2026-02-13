import pandas as pd

def find_primary_department(employee: pd.DataFrame) -> pd.DataFrame:
    primary = employee[employee['primary_flag'] == 'Y'][['employee_id', 'department_id']]
    
    no_primary_ids = employee[~employee['employee_id'].isin(primary['employee_id'])]['employee_id']
    
    single_dept = (
        employee[employee['employee_id'].isin(no_primary_ids)]
        .groupby('employee_id')
        .filter(lambda x: len(x) == 1)
        [['employee_id', 'department_id']]
    )
    
    return pd.concat([primary, single_dept]).sort_values('employee_id')