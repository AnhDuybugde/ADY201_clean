import pandas as pd
import numpy as np
import random
import os

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import PolynomialFeatures, StandardScaler, OneHotEncoder
from sklearn.decomposition import PCA

# --- Cố định seed ---
seed = 42
np.random.seed(seed)
random.seed(seed)
os.environ["PYTHONHASHSEED"] = str(seed)

class FeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(self, poly_degree=2, n_pca_components=50):
        self.poly_degree = poly_degree
        self.n_pca_components = n_pca_components  # 0 nghĩa là không dùng PCA
        self.scaler = StandardScaler()
        self.poly = PolynomialFeatures(degree=poly_degree, include_bias=False)
        self.pca = None
        self.numeric_cols = None

    def fit(self, df, y=None):
        df = df.copy()
        # --- Tạo feature mới ---
        df["camera_total"] = df["camera_primary"] + df["camera_secondary"]
        df["performance_score"] = df["ram"] * df["watt"]
        df["battery_performance"] = df["battery"] / (df["watt"] + 1e-6)
        df["is_dual_camera"] = (df["camera_secondary"] > 0).astype(int)
        df["is_high_end"] = ((df["ram"] >= 8) & (df["rom"] >= 128)).astype(int)
        df["is_large_screen"] = (df["display_size"] >= 6.5).astype(int)

        self.numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

        # Scale numeric
        self.scaler.fit(df[self.numeric_cols])

        # Poly
        self.poly.fit(df[self.numeric_cols])
        X_poly = self.poly.transform(df[self.numeric_cols])

        # PCA (nếu n_pca_components > 0)
        if self.n_pca_components > 0:
            self.pca = PCA(n_components=self.n_pca_components, random_state=42)
            self.pca.fit(X_poly)
        return self

    def transform(self, df):
        df = df.copy()
        # --- Tạo feature mới ---
        df["camera_total"] = df["camera_primary"] + df["camera_secondary"]
        df["performance_score"] = df["ram"] * df["watt"]
        df["battery_performance"] = df["battery"] / (df["watt"] + 1e-6)
        df["is_dual_camera"] = (df["camera_secondary"] > 0).astype(int)
        df["is_high_end"] = ((df["ram"] >= 8) & (df["rom"] >= 128)).astype(int)
        df["is_large_screen"] = (df["display_size"] >= 6.5).astype(int)

        # Scale numeric
        df[self.numeric_cols] = self.scaler.transform(df[self.numeric_cols])

        # Poly
        X_poly = self.poly.transform(df[self.numeric_cols])
        if self.pca is not None:
            X_poly = self.pca.transform(X_poly)
            poly_cols = [f"PCA_{i}" for i in range(X_poly.shape[1])]
        else:
            poly_cols = self.poly.get_feature_names_out(self.numeric_cols)

        df_poly = pd.DataFrame(X_poly, columns=poly_cols, index=df.index)

        # Kết hợp tất cả
        df_final = pd.concat([df_poly, df.drop(columns=self.numeric_cols)], axis=1)
        return df_final
