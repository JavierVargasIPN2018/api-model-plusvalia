
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from fastapi.responses import HTMLResponse
import pandas as pd
import numpy as np

app = FastAPI()

# Cargar modelo y columnas
model = pickle.load(open("model.pkl", "rb"))
columns = pickle.load(open("features.pkl", "rb"))

class PredictionRequest(BaseModel):
    alcaldia: str
    habitaciones: int
    baños: int
    metros: float
    renta_actual: float
    valor_actual: float
    tasa_ocupacion: float
    evento_mundial: bool
    fecha: str

@app.post("/predict")
def predict(req: PredictionRequest):
    d = req.dict()
    df = pd.DataFrame([d])
    df = pd.get_dummies(df, columns=["alcaldia"])
    for col in columns:
        if col not in df.columns:
            df[col] = 0
    df = df[columns]
    pct = float(model.predict(df)[0])  # <-- forzar a float
    total = float(d["valor_actual"]) * pct
    mensual = total / 12
    return {
        "plusvalia_pct": round(pct * 100, 2),
        "plusvalia_total": round(total, 2),
        "plusvalia_acumulada": list(np.cumsum([mensual]*12)),
        "months": list(range(1, 13))
    }

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>API Plusvalía</title>
            <style>
                body { font-family: sans-serif; text-align: center; padding-top: 100px; background: #f5f5f5; }
                h1 { font-size: 2.5rem; color: #333; }
                p { font-size: 1.2rem; color: #666; }
            </style>
        </head>
        <body>
            <h1>Bienvenido a la API de Predicción de Plusvalía</h1>
            <p>Usa el endpoint <code>/predict</code> para obtener predicciones.</p>
            <p>Documentación: <a href="/docs">/docs</a></p>
        </body>
    </html>
    """