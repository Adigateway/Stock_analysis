from config import COMPANY_TICKER
from preprocess import preprocess_data
from sequences import create_sequences
from model import build_model
import pandas as pd
import numpy as np
import sys



def validate_data(X, y):
    """Ensure data meets requirements before training"""
    checks = {
        'X is numpy array': isinstance(X, np.ndarray),
        'y is numpy array': isinstance(y, np.ndarray),
        'X has 3 dimensions': X.ndim == 3,
        'y has 1 dimension': y.ndim == 1,
        'No NaN in X': not np.isnan(X).any(),
        'No NaN in y': not np.isnan(y).any(),
        'Consistent samples': X.shape[0] == y.shape[0]
    }
    
    for check, result in checks.items():
        if not result:
            raise ValueError(f"Validation failed: {check}")
    
    print("✓ All data validation checks passed")
    return True

def main():
    try:
        print("=== Starting Training Pipeline ===")
        
        # 1. Data Loading
        print("\n[1/5] Loading data...")
        data = preprocess_data()
        print(f"✓ Data loaded. Shape: {data.shape}")
        print(f"Data columns: {data.columns.tolist()}")
        
        # 2. Sequence Creation
        print("\n[2/5] Creating sequences...")
        X, y, scaler = create_sequences(data)
        print(f"✓ Sequences created. X: {X.shape}, y: {y.shape}")
        
        # 3. Data Validation
        print("\n[3/5] Validating data...")
        validate_data(X, y)
        
        # 4. Train-Test Split
        print("\n[4/5] Splitting data...")
        split = int(0.8 * len(X))
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]
        print(f"✓ Split complete. Train: {len(X_train)}, Test: {len(X_test)}")
        
        # 5. Model Training
        print("\n[5/5] Training model...")
        model = build_model(input_shape=(X.shape[1], X.shape[2]))
        history = model.fit(
            X_train, y_train,
            validation_data=(X_test, y_test),
            epochs=70,
            batch_size=32,
            verbose=1
        )
        model.save(f"{COMPANY_TICKER}_attention_lstm.h5")
        print("✓ Training completed successfully!")
        
    except Exception as e:
        print(f"\n!!! Pipeline failed at step: {sys.exc_info()[-1].tb_lineno}")
        print(f"Error: {str(e)}")
        print("\nDebug Info:")
        if 'X' in locals(): print(f"X shape: {X.shape if isinstance(X, np.ndarray) else type(X)}")
        if 'y' in locals(): print(f"y shape: {y.shape if isinstance(y, np.ndarray) else type(y)}")
        if 'data' in locals(): print(f"Data cols: {data.columns.tolist() if hasattr(data, 'columns') else 'No DataFrame'}")
        sys.exit(1)

if __name__ == "__main__":
    main()
