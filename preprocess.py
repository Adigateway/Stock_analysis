from data_loader import load_stock_data
from technicals import add_technicals

def preprocess_data():
    # Load data
    df = load_stock_data()
    if df.isna().any().any():
        print("NaNs found in raw data, filling them")
        df = df.fillna(method='ffill')  # Forward fill NaNs
    # Verify columns exist
    required_columns = ['Price', 'Volume']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns: {missing}. Available: {df.columns.tolist()}")
    
    # Add technical indicators
    df = add_technicals(df)
    
    return df