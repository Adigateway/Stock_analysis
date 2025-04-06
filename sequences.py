import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def create_sequences(data, seq_length=30):
    scaler = MinMaxScaler()

    # If data is a DataFrame, convert it to a numpy array for easier manipulation
    if isinstance(data, pd.DataFrame):
        data = data.values  # Convert DataFrame to numpy array for processing

    # Check if the data is 1D or 2D and handle accordingly
    if data.ndim == 1:
        data = data.reshape(-1, 1)  # Convert 1D to 2D if needed
    elif data.shape[1] == 1:
        data = data.squeeze()  # Convert (n_samples, 1) to (n_samples,)

    # Handle NaNs by forward filling or replacing them
    if np.isnan(data).any():
        print(f"NaNs found in data, filling them.")
        data = np.nan_to_num(data, nan=0.0)  # You can replace NaNs with 0.0 or use other methods

    # Apply MinMax scaling
    data_scaled = scaler.fit_transform(data)

    X, y = [], []
    for i in range(len(data_scaled) - seq_length):
        X.append(data_scaled[i:i+seq_length])
        y.append(data_scaled[i+seq_length, 0])  # Assuming 'Price' is the first column

    # Convert to numpy arrays
    X = np.array(X)
    y = np.array(y).flatten()  # Ensure y is 1D

    # Validation
    if X.ndim != 3:
        raise ValueError(f"X must be 3D, got {X.ndim}D")
    if y.ndim != 1:
        raise ValueError(f"y must be 1D, got {y.ndim}D")

    return X, y, scaler