# Imagen base oficial de Python
FROM python:3.11

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar todos los archivos al contenedor
COPY . .

# Instalar dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 8000 (usado por FastAPI)
EXPOSE 8000

# Comando para correr la API con recarga automática en dev
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
