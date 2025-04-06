from preprocess import preprocess_data
from sequences import create_sequences

data = preprocess_data()
X, y, _ = create_sequences(data)
print(f"Final X shape: {X.shape}")
print(f"Final y shape: {y.shape}")
print(f"X[0][0]: {X[0][0]}")
print(f"y[0:5]: {y[0:5]}")