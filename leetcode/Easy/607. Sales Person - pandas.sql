import pandas as pd

def sales_person(sales_person: pd.DataFrame, 
                 company: pd.DataFrame, 
                 orders: pd.DataFrame) -> pd.DataFrame:
    
    # Находим ID компании "RED"
    red_company = company[company['name'] == 'RED']['com_id']
    
    if red_company.empty:
        return sales_person[['name']]
    
    red_com_id = red_company.iloc[0]
    
    # Находим заказы от компании "RED"
    red_orders = orders[orders['com_id'] == red_com_id]
    
    # Находим продавцов, которые имеют заказы от "RED"
    red_sales_ids = red_orders['sales_id'].unique()
    
    # Фильтруем продавцов, у которых нет заказов от "RED"
    result = sales_person[~sales_person['sales_id'].isin(red_sales_ids)][['name']]
    
    return result