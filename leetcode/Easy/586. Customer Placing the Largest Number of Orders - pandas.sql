import pandas as pd

def largest_orders(orders: pd.DataFrame) -> pd.DataFrame:
    # Group by customer and count orders
    customer_counts = orders.groupby('customer_number').size().reset_index(name='order_count')
    
    # Find the maximum order count
    max_count = customer_counts['order_count'].max()
    
    # Get customers with maximum count
    result = customer_counts[customer_counts['order_count'] == max_count][['customer_number']]
    
    return result