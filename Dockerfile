# Usamos una imagen oficial de Python
FROM python:3.13-slim
# Directorio de trabajo dentro del contenedor
WORKDIR /app
# Copiamos requirements.txt
COPY requirements.txt .
# Instalamos dependencias
RUN pip install -r requirements.txt
# Copiamos el código de la aplicación dentro de /app/src
COPY ./src /app/src
# Exponemos el puerto de la app
EXPOSE 8000
# Ejecutamos la app FastAPI con uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]


