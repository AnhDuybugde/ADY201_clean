import numpy as np
import pandas as pd
import random
import os
import optuna

from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import ElasticNet, Ridge, HuberRegressor
from sklearn.ensemble import StackingRegressor, ExtraTreesRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.model_selection import cross_val_score, KFold
from catboost import CatBoostRegressor
from optuna.pruners import MedianPruner

# --- Seed cố định ---
seed = 42
np.random.seed(seed)
random.seed(seed)
os.environ["PYTHONHASHSEED"] = str(seed)


class BalancedStackingRegressor(BaseEstimator, RegressorMixin):
    def __init__(self, cv=5, n_trials=100):
        self.cv = cv
        self.n_trials = n_trials
        self.model_ = None
        self.feature_types_ = None
        self.best_params_ = None

    def _identify_features(self, X, y):
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)
        X_num = X.select_dtypes(include=[np.number])
        self.feature_types_ = {'all': X_num.columns.tolist()}

    def _build_preprocessor(self):
        return 'passthrough'


    def _objective(self, trial, X, y):
        # --- Hyperparameter search space ---
        elastic_alpha = trial.suggest_float('elastic_alpha', 0.001, 0.2)
        elastic_l1 = trial.suggest_float('elastic_l1', 0.1, 0.9)
        et_depth = trial.suggest_int('et_depth', 3, 8)
        et_estimators = trial.suggest_int('et_estimators', 100, 300)

        cat_depth = trial.suggest_int('cat_depth', 4, 8)
        cat_lr = trial.suggest_float('cat_lr', 0.01, 0.05)
        cat_iter = trial.suggest_int('cat_iterations', 300, 800)

        ridge_alpha = trial.suggest_float("ridge_alpha", 0.1, 10.0)

        # --- Define base models ---
        estimators = [
            ('elastic', ElasticNet(alpha=elastic_alpha, l1_ratio=elastic_l1,
                                   max_iter=5000, random_state=seed)),
            ('huber', HuberRegressor()),
            ('et', ExtraTreesRegressor(n_estimators=et_estimators, max_depth=et_depth,
                                       random_state=seed, n_jobs=-1)),
            ('cat', CatBoostRegressor(iterations=cat_iter, depth=cat_depth,
                                      learning_rate=cat_lr, random_seed=seed, verbose=0)),
        ]   

        model = Pipeline([
            ('preprocess', self._build_preprocessor()),
            ('stack', StackingRegressor(
                estimators=estimators,
                final_estimator=Ridge(alpha=ridge_alpha, random_state=seed),
                passthrough=False,   # chỉ dùng output từ base models
                n_jobs=-1
            ))
        ])


        # --- Cross-validation ---
        kf = KFold(n_splits=self.cv, shuffle=True, random_state=seed)
        scores = -cross_val_score(model, X, y, cv=kf,
                                  scoring=make_scorer(mean_squared_error, greater_is_better=False),
                                  n_jobs=-1)
        return np.mean(scores)

    def fit(self, X, y):
        self._identify_features(X, y)

        # --- Optuna study ---
        sampler = optuna.samplers.TPESampler(seed=seed, n_startup_trials=10)
        pruner = MedianPruner(n_startup_trials=5)

        study = optuna.create_study(
            direction="minimize",
            sampler=sampler,
            pruner=pruner,
            study_name="balanced_stack_search",
            storage="sqlite:///optuna_studies.db",
            load_if_exists=True
        )

        # --- Run optimization ---
        study.optimize(lambda trial: self._objective(trial, X, y),
                       n_trials=self.n_trials,
                       show_progress_bar=True)

        self.best_params_ = study.best_params
        bp = self.best_params_

        # --- Build final model with best params ---
        estimators = [
            ('elastic', ElasticNet(alpha=bp['elastic_alpha'], l1_ratio=bp['elastic_l1'],
                                   max_iter=5000, random_state=seed)),
            ('huber', HuberRegressor()),
            ('et', ExtraTreesRegressor(n_estimators=bp['et_estimators'], max_depth=bp['et_depth'],
                                       random_state=seed, n_jobs=-1)),
            ('cat', CatBoostRegressor(iterations=bp['cat_iterations'], depth=bp['cat_depth'],
                                      learning_rate=bp['cat_lr'], random_seed=seed, verbose=0)),
        ]

        self.model_ = Pipeline([
            ('preprocess', self._build_preprocessor()),
            ('stack', StackingRegressor(
                estimators=estimators,
                final_estimator=Ridge(alpha=bp['ridge_alpha'], random_state=seed),
                passthrough=False,   # chỉ dùng output từ base models
                n_jobs=-1
            ))
        ])

        self.model_.fit(X, y)
        return self

    def predict(self, X):
        return self.model_.predict(X)
