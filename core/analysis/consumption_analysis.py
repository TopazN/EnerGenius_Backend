def get_daily_summary(df):
    df['date'] = df['datetime'].dt.date
    return df.groupby('date')['consumption'].sum()