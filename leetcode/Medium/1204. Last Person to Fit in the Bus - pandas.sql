import pandas as pd

def last_person_to_fit_in_bus(queue: pd.DataFrame) -> pd.DataFrame:
    # Sort by turn
    queue = queue.sort_values('turn')
    
    # Calculate cumulative sum
    queue['cumulative_weight'] = queue['weight'].cumsum()
    
    # Filter where cumulative weight <= 1000
    valid_people = queue[queue['cumulative_weight'] <= 1000]
    
    # Get the last person (highest turn) who can fit
    if len(valid_people) == 0:
        return pd.DataFrame({'person_name': []})
    
    last_person = valid_people.iloc[-1]
    return pd.DataFrame({'person_name': [last_person['person_name']]})