import pandas as pd
import numpy as np
from db_utils import load_data
from config import SAVING_TABLE

from src.save_utils import saving_data, save_results, append_to_summary
from src.data_preprocessing import Preprocessor
from src.feature_engineering import FeatureEngineer
from src.model_training import BalancedStackingRegressor
from src.evaluation import evaluate_model
from src.interpretability import explain_model

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

import warnings
warnings.filterwarnings("ignore", message="No further splits with positive gain")

# 1. LOAD DATA
df = load_data(SAVING_TABLE)

# 2. SPLIT FEATURES / TARGET
X = df.drop(columns=['price'])
y = df['price'].values

# --- chuyển y sang log scale để train ---
y_log = np.log1p(y)  # log1p = log(1+y) tránh log(0)

# Split train/test
X_train, X_test, y_train_log, y_test_log, y_train_orig, y_test_orig = train_test_split(
    X, y_log, y, test_size=0.2, random_state=42
)

y_train_orig = y_train_log.copy()
y_test_orig  = y_test_log.copy()

# 3. PIPELINE FEATURE
full_pipeline = Pipeline([
    ('preprocess', Preprocessor()),
    ('feature_engineer', FeatureEngineer()),
])

# Fit-transform train, transform test
X_train_final = full_pipeline.fit_transform(X_train)
X_test_final  = full_pipeline.transform(X_test)

prep = Preprocessor()
fe = FeatureEngineer()

# Preprocess
X_train_prep = prep.fit_transform(X_train)
X_test_prep  = prep.transform(X_test)

# Feature engineer trên dữ liệu đã preprocess
X_train_fe = fe.fit_transform(X_train_prep)
X_test_fe  = fe.transform(X_test_prep)

print("pre Train shape:", X_train_prep.shape)
print("pre Test shape :", X_test_prep.shape)

print("fe Train shape:", X_train_fe.shape)
print("fe Test shape :", X_test_fe.shape)

# print("Train shape:", X_train_final.shape)
# print("Test shape :", X_test_final.shape)

# 4. TRAIN STACKING MODEL
print("\n=== STACKING PHASE ===")
model = BalancedStackingRegressor()
model.fit(X_train_final, y_train_log)

# 5. PREDICT (chuyển ngược log để đánh giá)
y_train_pred_log = model.predict(X_train_final)
y_test_pred_log  = model.predict(X_test_final)

y_train_pred = np.expm1(y_train_pred_log)  # revert về scale gốc
y_test_pred  = np.expm1(y_test_pred_log)

# 6. FINAL EVALUATION
results = evaluate_model(model, X_train_final, X_test_final, y_train_orig, y_test_orig)

# 7. SAVE MODEL + PREPROCESSOR + LOG
model_name = "stacking_model"
save_results(model_name, results, model=model.model_, preprocessor=full_pipeline)

# 8. UPDATE SUMMARY
append_to_summary(model_name, results)

# 9. INTERPRETABILITY
explain_model(model.model_, X_train_final)
