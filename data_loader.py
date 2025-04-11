import pandas as pd
import yfinance as yf
from config import COMPANY_TICKER, START_DATE, END_DATE

def load_stock_data():
    try:
        # Download data (without group_by to avoid MultiIndex issues)
        df = yf.download(COMPANY_TICKER, start=START_DATE, end=END_DATE)
        
        print("Raw columns from yfinance:", df.columns.tolist())  # Debug print
        
        # Check available price columns
        if 'Adj Close' in df.columns:
            df = df.rename(columns={'Adj Close': 'Price'})
        elif 'Close' in df.columns:
            df = df.rename(columns={'Close': 'Price'})
        else:
            raise KeyError(f"No price column found. Available columns: {df.columns.tolist()}")
            
        # Select only needed columns
        df = df[['Price', 'Volume']]
        
        print("Final columns:", df.columns.tolist())  # Debug print
        return df
        
    except Exception as e:
        print(f"Error loading {COMPANY_TICKER} data: {str(e)}")
        raise
