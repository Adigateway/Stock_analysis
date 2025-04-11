from data_loader import load_stock_data
from config import COMPANY_TICKER
from technicals import add_technicals
from macro_loader import load_macro_data
from sentiments_ambi import get_daily_sentiment
import pandas as pd

def preprocess_data():
    df = load_stock_data()
    
    # Fix MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]  # Keep first level only
    
    # Add technicals and sentiment
    df = add_technicals(df)
    sentiment = get_daily_sentiment()
    df = df.join(sentiment, how='left')
    
    macro_data=load_macro_data()
    df=df.join(macro_data, how='left')

    
    # Handle missing data
    df['Sentiment'] = df['Sentiment'].fillna(0)
    df=df.ffill()
    
    
    # Verify columns
    required = ['Price', 'Volume']
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise KeyError(f"Missing columns: {missing}. Current: {df.columns.tolist()}")
    
    return df
