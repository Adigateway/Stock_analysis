from config import COMPANY_TICKER
from preprocess import preprocess_data
from sequences import create_sequences
from tensorflow.keras.models import load_model
import numpy as np

def main():
    try:
        # 1. Load the trained model
        print("Loading trained model...")
        model = load_model(f"{COMPANY_TICKER}_attention_lstm.h5")
        
        # 2. Prepare fresh test data
        print("Preparing test data...")
        data = preprocess_data()
        X, y, scaler = create_sequences(data)
        
        # 3. Use the LAST sequence for prediction (most recent data)
        X_test = X[-1:]  # Takes the most recent sequence
        print(f"Test data shape: {X_test.shape}")
        
        # 4. Make prediction
        print("Making prediction...")
        y_pred = model.predict(X_test)
        
        # 5. Inverse transform the prediction
        y_pred_actual = scaler.inverse_transform(
            np.concatenate([
                y_pred.reshape(-1, 1),
                np.zeros((len(y_pred), data.shape[1] - 1))
            ], axis=1))[:, 0]
        
        print(f"\nNext day predicted price: {y_pred_actual[0]:.2f}")
        
    except Exception as e:
        print(f"Prediction failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()