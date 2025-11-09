import streamlit as st
import pandas as pd
import numpy as np
from src.save_utils import load_saved_model

# Load best model + preprocessor
model_name = "stacking_model"
model, preprocessor = load_saved_model(model_name)

st.title("Predict Cellphone Price")

# --- INPUTS ---
st.sidebar.header("Enter product specifications:")

ram = st.sidebar.number_input("RAM (GB)", min_value=1, max_value=64, value=8)
rom = st.sidebar.number_input("ROM / Storage (GB)", min_value=8, max_value=1024, value=128)
battery = st.sidebar.number_input("Battery (mAh)", min_value=1000, max_value=10000, value=4500)
camera_primary = st.sidebar.number_input("Primary Camera (MP)", min_value=1, max_value=200, value=48)
camera_secondary = st.sidebar.number_input("Secondary Camera (MP)", min_value=0, max_value=200, value=12)
display_size = st.sidebar.number_input("Display Size (inch)", min_value=3.0, max_value=10.0, value=6.5)
screen = st.sidebar.selectbox("Screen type", ["LCD", "OLED", "AMOLED", "Retina", "Other"])
sensor = st.sidebar.text_input("Sensor features", "Fingerprint, FaceID")
watt = st.sidebar.number_input("Charging watt", min_value=0, max_value=200, value=33)
brand = st.sidebar.text_input("Brand", "Apple")
os = st.sidebar.text_input("Operating System", "iOS")
chipset = st.sidebar.text_input("Chipset", "Apple A17")
gpu = st.sidebar.text_input("GPU", "Apple GPU")
nfc = st.sidebar.selectbox("NFC support", ["Yes", "No"])
jack_support = st.sidebar.selectbox("Headphone Jack", ["Yes", "No"])

# --- BUTTON ---
if st.button("Predict Price"):
    # Build input dataframe
    X_input = pd.DataFrame([{
        "ram": ram,
        "rom": rom,
        "battery": battery,
        "camera_primary": camera_primary,
        "camera_secondary": camera_secondary,
        "display_size": display_size,
        "screen": screen,
        "sensor": sensor,
        "watt": watt,
        "brand": brand,
        "os": os,
        "chipset": chipset,
        "gpu": gpu,
        "nfc": nfc,
        "jack_support": jack_support
    }])

    # Transform
    X_transformed = preprocessor.transform(X_input)

    # Predict log scale -> revert
    y_pred_log = model.predict(X_transformed)
    y_pred = np.expm1(y_pred_log)

    st.success(f"Predicted price: {y_pred[0]:,.0f} VND")
