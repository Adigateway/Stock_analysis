from ta.momentum import RSIIndicator
from ta.trend import MACD

def add_technicals(df):
    # Verify Price column exists
    if 'Price' not in df.columns:
        raise KeyError(f"'Price' column missing. Available columns: {df.columns.tolist()}")
    
    # Calculate indicators
    df['RSI'] = RSIIndicator(close=df['Price'].squeeze()).rsi()
    df['MACD'] = MACD(close=df['Price'].squeeze()).macd()
    
    return df