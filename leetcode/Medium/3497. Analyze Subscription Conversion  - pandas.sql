import pandas as pd

def analyze_subscription_conversion(user_activity: pd.DataFrame) -> pd.DataFrame:
    df = user_activity.copy()
    paid_users = df[df['activity_type'] == 'paid']['user_id'].unique()
    df = df[df['user_id'].isin(paid_users)]
    first_paid = df[df['activity_type'] == 'paid'].groupby('user_id')['activity_date'].min().rename('first_paid_date')
    df = df.merge(first_paid, on='user_id')
    
    trial = df[(df['activity_type'] == 'free_trial') & (df['activity_date'] < df['first_paid_date'])]
    paid = df[(df['activity_type'] == 'paid') & (df['activity_date'] >= df['first_paid_date'])]
    
    trial_avg = trial.groupby('user_id')['activity_duration'].mean().round(2).rename('trial_avg_duration')
    paid_avg = paid.groupby('user_id')['activity_duration'].mean().add(1e-10).round(2).rename('paid_avg_duration')
    
    result = pd.DataFrame({'user_id': sorted(paid_users)})
    result = result.merge(trial_avg, on='user_id', how='left')
    result = result.merge(paid_avg, on='user_id', how='left')
    
    return result