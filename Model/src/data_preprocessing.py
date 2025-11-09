import pandas as pd
import numpy as np
import random 
import os
from sklearn.experimental import enable_iterative_imputer  # phải có dòng này trước
from sklearn.impute import SimpleImputer, IterativeImputer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler, PowerTransformer
from sklearn.ensemble import ExtraTreesRegressor
from scipy.stats.mstats import winsorize

# --- Đặt seed cố định ---
seed = 42
np.random.seed(seed)
random.seed(seed)
os.environ['PYTHONHASHSEED'] = str(seed)

class Preprocessor:
    def __init__(self, yeo_threshold=0.5):
        self.yeo_threshold = yeo_threshold

        # Lưu danh sách cột
        self.numeric_features = ["ram", "rom", "battery", "camera_primary", "camera_secondary",
                                 "display_size", "screen", "sensor", "watt"]
        self.categorical_features = ["brand", "os", "chipset", "gpu"]
        self.binary_features = ["nfc", "jack_support"]

        # Khởi tạo transformer (để reuse cho transform)
        self.num_imputer = IterativeImputer(estimator=ExtraTreesRegressor(random_state=42), random_state=42)
        self.cat_imputer = SimpleImputer(strategy='most_frequent')
        self.bin_imputer = SimpleImputer(strategy='most_frequent')
        self.pt = PowerTransformer(method='yeo-johnson')
        self.scaler = StandardScaler()
        self.ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        self.oe = OrdinalEncoder()

        # Lưu danh sách cột được biến đổi
        self.skewed_cols = None
        self.onehot_cols = ['brand']
        self.ordinal_cols = [c for c in self.categorical_features if c not in self.onehot_cols]

    def _cast_types(self, df):
        df = df.copy()
        for col in self.numeric_features:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df[self.categorical_features] = df[self.categorical_features].astype(str)
        df[self.binary_features] = df[self.binary_features].apply(pd.to_numeric, errors='coerce')
        return df

    def fit_transform(self, df, y=None):
        df = self._cast_types(df)

        # Numeric impute
        df[self.numeric_features] = self.num_imputer.fit_transform(df[self.numeric_features])
        # Cat + bin impute
        df[self.categorical_features] = self.cat_imputer.fit_transform(df[self.categorical_features])
        df[self.binary_features] = self.bin_imputer.fit_transform(df[self.binary_features]).astype(int)

        # Winsorize
        for col in self.numeric_features:
            df[col] = winsorize(df[col], limits=[0.01, 0.01])

        # Skewed + yeo-johnson
        self.skewed_cols = [col for col in self.numeric_features if abs(df[col].skew()) > self.yeo_threshold]
        if self.skewed_cols:
            df[self.skewed_cols] = self.pt.fit_transform(df[self.skewed_cols])

        # Scale
        df[self.numeric_features] = self.scaler.fit_transform(df[self.numeric_features])

        # Encode
        encoded_df = self._encode_fit_transform(df)
        return pd.concat([df[self.numeric_features], df[self.binary_features],
                          encoded_df], axis=1)

    def transform(self, df, y=None):
        df = self._cast_types(df)

        # Impute
        df[self.numeric_features] = self.num_imputer.transform(df[self.numeric_features])
        df[self.categorical_features] = self.cat_imputer.transform(df[self.categorical_features])
        df[self.binary_features] = self.bin_imputer.transform(df[self.binary_features]).astype(int)

        # Winsorize
        for col in self.numeric_features:
            df[col] = winsorize(df[col], limits=[0.01, 0.01])

        # Yeo-Johnson (chỉ cột skewed của train)
        if self.skewed_cols:
            df[self.skewed_cols] = self.pt.transform(df[self.skewed_cols])

        # Scale
        df[self.numeric_features] = self.scaler.transform(df[self.numeric_features])

        # Encode (chỉ transform)
        encoded_df = self._encode_transform(df)
        return pd.concat([df[self.numeric_features], df[self.binary_features],
                          encoded_df], axis=1)

    def _encode_fit_transform(self, df):
        brand_encoded = self.ohe.fit_transform(df[self.onehot_cols])
        df_brand = pd.DataFrame(brand_encoded, columns=self.ohe.get_feature_names_out(self.onehot_cols),
                                index=df.index)
        df_ordinal = df[self.ordinal_cols].copy()
        df_ordinal[self.ordinal_cols] = self.oe.fit_transform(df_ordinal[self.ordinal_cols])
        return pd.concat([df_brand, df_ordinal], axis=1)

    def _encode_transform(self, df):
        brand_encoded = self.ohe.transform(df[self.onehot_cols])
        df_brand = pd.DataFrame(brand_encoded, columns=self.ohe.get_feature_names_out(self.onehot_cols),
                                index=df.index)
        df_ordinal = df[self.ordinal_cols].copy()
        df_ordinal[self.ordinal_cols] = self.oe.transform(df_ordinal[self.ordinal_cols])
        return pd.concat([df_brand, df_ordinal], axis=1)
