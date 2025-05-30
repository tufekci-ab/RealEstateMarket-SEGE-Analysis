

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor
import joblib
import matplotlib.pyplot as plt

df = pd.read_csv("detailed-listings-cleaned.csv")

numeric_features = [
    "metrekare", "bina_yasi", "kat_sayisi_encoded",
    "oda_sayisi_yeni", "salon_sayisi",
    "banyo_sayisi", "kat_sayisi",
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
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
])

best_model = XGBRegressor(
    tree_method='hist',
    device='cuda',
    random_state=42,
    colsample_bytree=0.9447,
    gamma=3.6390,
    learning_rate=0.0372,
    max_depth=10,
    min_child_weight=1,
    n_estimators=400,
    reg_alpha=3.2243,
    reg_lambda=1.4682,
    subsample=0.8187,
)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", best_model)
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MAE: {mae:,.0f} TL/m²")
print(f"R² Score: {r2:.3f}")

joblib.dump(pipeline, "trained_model.pkl")

model = pipeline.named_steps["model"]
feature_names = (
    list(preprocessor.transformers_[0][2]) +
    list(pipeline.named_steps["preprocessor"]
         .transformers_[1][1]
         .get_feature_names_out(categorical_features))
)
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

print("\nTop 10 Önemli Özellik:")
for i in indices[:10]:
    print(f"{feature_names[i]}: {importances[i]:.4f}")

plt.figure(figsize=(10,6))
plt.bar([feature_names[i] for i in indices[:10]], importances[indices[:10]])
plt.xticks(rotation=45, ha='right')
plt.title("Özellik Önem Dereceleri (Top 10)")
plt.tight_layout()
plt.savefig("feature_importance.png")
