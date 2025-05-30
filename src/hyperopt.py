import pandas as pd
import numpy as np

from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
from hyperopt import fmin, tpe, hp, Trials, STATUS_OK

df = pd.read_csv("detailed-listings-cleaned.csv")

numeric_features = [
    "metrekare", "bina_yasi", "kat_sayisi_encoded",
    "oda_sayisi_yeni", "salon_sayisi", "banyo_sayisi", "kat_sayisi",
    "cephe_kuzey", "cephe_guney", "cephe_dogu", "cephe_bati"
]

categorical_features = ["isinma_tipi", "kullanim_durumu", "kademe", "il"]
target = "fiyat_per_m2"

df[numeric_features + [target]] = df[numeric_features + [target]].apply(pd.to_numeric, errors="coerce")
df = df.dropna(subset=numeric_features + categorical_features + [target])

X = df[numeric_features + categorical_features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(), numeric_features),
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features)
])

def objective(params):
    model = XGBRegressor(
        tree_method='hist',
        device='cuda',
        random_state=42,
        n_estimators=int(params['n_estimators']),
        max_depth=int(params['max_depth']),
        learning_rate=float(params['learning_rate']),
        subsample=float(params['subsample']),
        colsample_bytree=float(params['colsample_bytree']),
        gamma=float(params['gamma']),
        reg_alpha=float(params['reg_alpha']),
        reg_lambda=float(params['reg_lambda']),
        min_child_weight=int(params['min_child_weight']),
        verbosity=0
    )

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    score = -np.mean(cross_val_score(pipeline, X_train, y_train, scoring="neg_mean_absolute_error", cv=3, n_jobs=-1))
    return {'loss': score, 'status': STATUS_OK}

space = {
    'n_estimators': hp.quniform('n_estimators', 100, 500, 50),
    'max_depth': hp.quniform('max_depth', 3, 10, 1),
    'learning_rate': hp.loguniform('learning_rate', np.log(0.01), np.log(0.3)),
    'subsample': hp.uniform('subsample', 0.6, 1.0),
    'colsample_bytree': hp.uniform('colsample_bytree', 0.6, 1.0),
    'gamma': hp.uniform('gamma', 0, 5),
    'reg_alpha': hp.uniform('reg_alpha', 0, 5),
    'reg_lambda': hp.uniform('reg_lambda', 0, 5),
    'min_child_weight': hp.quniform('min_child_weight', 1, 10, 1)
}

trials = Trials()
best = fmin(fn=objective,
            space=space,
            algo=tpe.suggest,
            max_evals=250,
            trials=trials,
            rstate=np.random.default_rng(42))

print("Best parameters found:", best)
