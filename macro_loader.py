# macro_loader.py
from fredapi import Fred
import pandas as pd
from config import START_DATE, END_DATE, FRED_API_KEY

def load_macro_data():
    fred = Fred(api_key=FRED_API_KEY)
    inflation = fred.get_series('CPIAUCSL', START_DATE, END_DATE).resample('D').ffill()
    fed_rate = fred.get_series('FEDFUNDS', START_DATE, END_DATE).resample('D').ffill()
    return pd.DataFrame({'Inflation': inflation, 'Fed_Rate': fed_rate})