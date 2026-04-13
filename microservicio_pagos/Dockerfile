# Imagen base ligera de Python
FROM python:3.11-alpine

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar Flask y Gunicorn (sin archivos .pyc innecesarios)
RUN pip install --no-cache-dir flask gunicorn

# Copiar el codigo del microservicio
COPY . .

# Exponer el puerto que usara Gunicorn
EXPOSE 5000

# Arrancar con Gunicorn en produccion
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
