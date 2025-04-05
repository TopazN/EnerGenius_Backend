import pandas as pd
from core.models import EnergyConsumption
from prophet import Prophet

def generate_consumption_analysis(user):
    records = EnergyConsumption.objects.filter(user=user).values('date', 'consumption_kwh')
    df = pd.DataFrame.from_records(records)
    df.rename(columns={'date': 'ds', 'consumption_kwh': 'y'}, inplace=True)

    # Prophet Model
    model = Prophet()
    model.fit(df)

    # Future prediction (next month)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
