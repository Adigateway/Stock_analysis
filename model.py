from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense

from tensorflow.keras.losses import MeanSquaredError

def build_model(input_shape):
    inputs = Input(shape=input_shape)
    lstm_out = LSTM(64)(inputs)
    outputs = Dense(1)(lstm_out)
    
    model = Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer='adam', 
                 loss=MeanSquaredError())  # Using string reference
    return model
