# Documentación Técnica - MVP API de Predicción de Plusvalía

## 🧠 Objetivo
Montar una API con FastAPI que predice la plusvalía proyectada de inmuebles Airbnb en CDMX utilizando un modelo de Machine Learning (XGBoost) entrenado con datos sintéticos.

---

## 📦 1. Generación de Datos Sintéticos

Se generó un dataset con 300 registros simulados que incluyen:

- `alcaldia`: [Coyoacán, Benito Juárez, Cuauhtémoc, Miguel Hidalgo, Álvaro Obregón]
- `habitaciones`, `baños`, `metros`
- `renta_actual`, `valor_actual`, `tasa_ocupacion`
- `evento_mundial` (booleano)
- `plusvalia_objetivo`: generada como fórmula:
  ```
  0.03 + 0.005 * habitaciones + 0.001 * metros + 0.01 * evento_mundial + ruido
  ```

---


---

## 🧠 2. Entrenamiento del Modelo (detallado)

### ¿Por qué usamos XGBoost?

XGBoost (`XGBRegressor`) es un modelo de boosting basado en árboles de decisión, ideal para problemas de regresión con datos tabulares. Ventajas:

- Maneja bien relaciones no lineales
- Robusto contra outliers
- Soporta features categóricos (tras codificación)
- Fácil de entrenar, rápido y preciso para un MVP

### Preprocesamiento con One-Hot Encoding

`alcaldia` es una variable categórica (texto). Los modelos como XGBoost necesitan que todas las columnas sean numéricas.

Por eso usamos **One-Hot Encoding**, que transforma:

```text
alcaldia = "Coyoacán"
```

En columnas binarias:

```text
alcaldia_Coyoacán = 1
alcaldia_Benito Juárez = 0
alcaldia_Cuauhtémoc = 0
...
```

Esto permite que el modelo aprenda diferencias entre zonas sin asumir orden numérico.

### Variables de entrada (`X`)

Después del encoding, las columnas que usamos como input son:

- `habitaciones`, `baños`, `metros`
- `renta_actual`, `valor_actual`
- `tasa_ocupacion`
- `evento_mundial`
- `alcaldia_*` (una columna por cada valor posible)

### Variable objetivo (`y`)

La variable que queremos predecir es:

```text
plusvalia_objetivo = porcentaje de incremento estimado en el valor del inmueble durante el siguiente año
```

Ejemplo: `0.1369` → 13.69%

### Entrenamiento

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = xgb.XGBRegressor()
model.fit(X_train, y_train)
```

Este modelo luego se guarda como `model.pkl` y se usa en producción para hacer predicciones realistas basadas en los inputs enviados por el usuario.


- Se usó `XGBRegressor` de `xgboost`
- Se realizó `one-hot encoding` de alcaldías
- Se dividió el dataset en 80/20 (train/test)
- Se guardaron dos archivos:

  - `model.pkl`: el modelo serializado
  - `features.pkl`: lista de columnas que espera el modelo

Script de entrenamiento:

```
python train_model.py
```

---

## 🌐 3. API con FastAPI

- Se creó `app.py` con dos endpoints:

  - `POST /predict`: recibe un JSON con datos del inmueble y devuelve:

    ```json
    {
      "plusvalia_pct": 13.69,
      "plusvalia_total": 444913.35,
      "plusvalia_acumulada": [...],
      "months": [1, 2, ..., 12]
    }
    ```

  - `GET /`: devuelve HTML con bienvenida

---

## 🐳 4. Dockerización

### `Dockerfile`
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### `docker-compose.yml`
```yaml
services:
  api:
    image: python:3.11
    ports:
      - "3016:8000"
    volumes:
      - .:/app
    working_dir: /app
    command: bash -c "pip install -r requirements.txt && uvicorn app:app --host 0.0.0.0 --port 8000 --reload"
```

---

## ☁️ 5. Despliegue en VPS

### Pasos:

```bash
# Conectarse
ssh usuario@IP

# Clonar repo
git clone https://github.com/JavierVargasIPN2018/api-model-plusvalia.git
cd api-model-plusvalia

# Levantar con Docker
docker compose up -d --build
```

---

## 🧪 6. Pruebas

- Swagger docs: `http://TU_IP:3016/docs`
- HTML de bienvenida: `http://TU_IP:3016/`
- Peticiones válidas con campos como:

```json
{
  "alcaldia": "Coyoacán",
  "habitaciones": 3,
  "baños": 2,
  "metros": 80,
  "renta_actual": 18500,
  "valor_actual": 3250000,
  "tasa_ocupacion": 0.75,
  "evento_mundial": false,
  "fecha": "2025-06-28"
}
```

---

## ✅ Resultado

API funcional, portable, y escalable para MVP académico/profesional.