import pandas as pd
import numpy as np
from src.save_utils import load_saved_model

# --- LOAD BEST MODEL + PREPROCESSOR ---
model_name = "stacking_model"
model, preprocessor = load_saved_model(model_name)

# --- INPUT EXAMPLE ---
# Dãy giá trị: brand, os, chipset, gpu, ram, rom, battery, camera_primary, camera_secondary,
# display_size, screen, sensor, watt, nfc, jack_support
input_data = {
    "brand": "Apple",
    "os": "High",
    "chipset": "Low",
    "gpu": "Mid",
    "ram": 8,
    "rom": 128,
    "battery": 5000,
    "camera_primary": 52,
    "camera_secondary": 12,
    "display_size": 6.1,
    "screen": 800,
    "sensor": 6,
    "watt": 50,
    "nfc": 1,
    "jack_support": 0
}

X_input = pd.DataFrame([input_data])

# --- TRANSFORM & PREDICT ---
X_transformed = preprocessor.transform(X_input)
y_pred_log = model.predict(X_transformed)
y_pred = np.expm1(y_pred_log)

print(f"Predicted price: {y_pred[0]:,.0f} VND")
