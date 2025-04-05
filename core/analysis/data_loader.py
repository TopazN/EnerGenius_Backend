import pandas as pd

def load_consumption_data(file_path):
    df = pd.read_csv(file_path, encoding="ISO-8859-8")  # תואם עברית
    df['datetime'] = pd.to_datetime(df['מועד קריאה'], errors='coerce')
    df['consumption'] = pd.to_numeric(df['צריכה בקוט"ש'], errors='coerce')
    df.dropna(subset=['datetime', 'consumption'], inplace=True)
    return df
