import pandas as pd
import xgboost as xgb
import pickle
from sklearn.model_selection import train_test_split

# Cargar dataset
df = pd.read_csv("dataset_sintetico.csv")

# One-hot encoding para la alcaldía
df = pd.get_dummies(df, columns=["alcaldia"])

# Separar features y target
X = df.drop(columns=["plusvalia_objetivo"])
y = df["plusvalia_objetivo"]

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar modelo
model = xgb.XGBRegressor()
model.fit(X_train, y_train)

# Guardar modelo entrenado
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

# Guardar lista de columnas (ordenadas)
with open("features.pkl", "wb") as f:
    pickle.dump(list(X.columns), f)

print("Modelo y columnas guardadas como model.pkl y features.pkl")
