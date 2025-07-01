
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from fastapi.responses import HTMLResponse
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
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

    # Predicción de plusvalía anual
    pct = float(model.predict(df)[0])
    valor_actual = float(d["valor_actual"])
    plusvalia_total = valor_actual * pct
    plusvalia_mensual = plusvalia_total / 12

    # Renta mensual proyectada con 10.09% de aumento
    renta_mensual = d["renta_actual"] * 1.1009
    renta_mensual_total = renta_mensual * 12
    renta_mensual_estimada = [round(renta_mensual * (i + 1), 2) for i in range(12)]

    # Plusvalía acumulada mes a mes
    plusvalia_estimada = [round(plusvalia_mensual * (i + 1), 2) for i in range(12)]

    return {
        "renta": {
            "cambio_en_renta_mensual": 10.09,
            "renta_mensual_estimada": round(renta_mensual_total, 2),
            "renta_estimada": renta_mensual_estimada,
            "renta_real": renta_mensual_estimada[:2]
        },
        "plusvalia": {
            "plusvalia_pct": round(pct * 100, 2),
            "valor_estimado_de_venta": int(valor_actual),
            "cambio_estimado_de_venta": 5,
            "plusvalia_total": round(plusvalia_total, 2),
            "plusvalia_estimada": plusvalia_estimada,
            "plusvalia_real": plusvalia_estimada[:2]
        }
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