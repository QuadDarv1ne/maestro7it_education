import pandas as pd

def tree_node(tree: pd.DataFrame) -> pd.DataFrame:
    # Создаем множество ID, которые являются родительскими (p_id)
    parent_ids = set(tree['p_id'].dropna().unique())
    # Применяем логику классификации
    def classify(row):
        if pd.isna(row['p_id']):
            return 'Root'
        elif row['id'] in parent_ids:
            return 'Inner'
        else:
            return 'Leaf'
    tree['type'] = tree.apply(classify, axis=1)
    return tree[['id', 'type']]