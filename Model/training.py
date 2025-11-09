import pandas as pd
import os

from sklearn.model_selection import train_test_split
from src.model_training import train_with_optuna
from src.evaluation import evaluate_model
from src.interpretability import explain_model
from src.save_utils import save_results, append_to_summary, saving_data
from sklearn.linear_model import ElasticNet, Ridge
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.ensemble import StackingRegressor

file_path = os.path.join(os.getcwd(), "data", "engineered_data.csv")

df = pd.read_csv(file_path)
# print(df.head(n=10))

# TRAIN / TEST SPLIT
TARGET_COL = "price"
X_raw = df.drop(columns=[TARGET_COL])
y = df[TARGET_COL]
X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    X_raw, y, test_size=0.2, random_state=42
)

# PREPROCESS
X_train, encoder, imputer, scaler, num_cols, cat_cols = fit_preprocessor(X_train_raw)
X_test = transform_preprocessor(X_test_raw, encoder, imputer, scaler, num_cols, cat_cols)

# HYPERPARAMETER OPTIMIZATION
study = train_with_optuna(X_train, y_train, n_trials=30)
best_params = study.best_trial.params
print("Best params:", best_params)

# # FIT STACKING MODEL VỚI BEST PARAMS
# stack = StackingRegressor(
#     estimators=[
#         ("elasticnet", ElasticNet(
#             alpha=best_params["elasticnet_alpha"],
#             l1_ratio=best_params["elasticnet_l1_ratio"],
#             max_iter=5000, random_state=42
#         )),
#         ("xgb", XGBRegressor(n_jobs=-1, random_state=42)),
#         ("lgb", LGBMRegressor(n_jobs=-1, random_state=42))
#     ],
#     final_estimator=Ridge(
#         alpha=best_params["ridge_alpha"],
#         max_iter=5000, random_state=42
#     ),
#     passthrough=True,
#     n_jobs=-1
# )
# stack.fit(X_train, y_train)

# # EVALUATE
# train_rmse, test_rmse, train_mae, test_mae, train_r2, test_r2 = evaluate_model(
#     stack, X_train, X_test, y_train, y_test
# )

# # INTERPRET
# explain_model(stack, X_test.sample(50, random_state=42))

# # SAVE EXPERIMENT
# results = {
#     "best_params": best_params,
#     "train_rmse": train_rmse,
#     "test_rmse": test_rmse,
#     "train_mae": train_mae,
#     "test_mae": test_mae,
#     "train_r2": train_r2,
#     "test_r2": test_r2
# }

# # Tạo preprocessor metadata đầy đủ để lưu
# from datetime import datetime

# from datetime import datetime

# # Preprocessor metadata đầy đủ
# preprocessor_full = {
#     "encoder": encoder,
#     "imputer": imputer,
#     "scaler": scaler,
#     "num_cols": list(num_cols),
#     "cat_cols": list(cat_cols),
#     "feature_order": list(X_train.columns),
#     "imputer_feature_names": (
#         list(imputer.feature_names_in_)
#         if hasattr(imputer, "feature_names_in_") else list(num_cols)
#     ),
#     "yj_transformed_cols": transformed_cols if 'transformed_cols' in locals() else [],
#     "feature_engineering_params": {
#         "poly_degree": 2,
#         "apply_pca": False,
#         "n_pca_components": 0.95
#     },
#     "pipeline_version": "v1.0",
#     "trained_columns_count": X_train.shape[1],
#     "trained_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     "target_column": TARGET_COL,
#     "random_state": 42,
#     "notes": "Final production-ready preprocessor"
# }



# # Lưu model + preprocessor + log (tự động lưu feature_order.pkl)
# save_results(
#     "house_price_stacking",
#     results,
#     model=stack,
#     preprocessor=preprocessor_full
# )

# # Cập nhật summary tổng hợp
# append_to_summary("house_price_stacking", results)
