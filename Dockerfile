# Usa una imagen oficial de Python
FROM python:3.11-slim

# Evita que Python genere archivos .pyc y buffers
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crea y usa el directorio del proyecto
WORKDIR /usr/src/app


# Install System Dependencies (including netcat)
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    pkg-config \
    libpq-dev \
    gcc \
    default-libmysqlclient-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*


# Upgrade pip (Needs a new RUN instruction)
RUN pip install --upgrade pip 
# Install Python Dependencies (from requirements.txt, usually done here)
RUN pip install --no-cache-dir -r requirements.txt


# Copies the script to the WORKDIR & grant execution permission
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh


# Finalmente copiar el resto del código del proyecto django.
# Si el código django cambia, solo se invalida esta capa (y las siguientes).
# El 1r  '.' es el origen (directorio actual en la máquina local)
# El 2do '.' es el destino (el WORKDIR, que es /usr/src/app)
COPY . .


# Define la ruta absoluta del entrypoint
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]


# Expone el puerto donde corre Django
EXPOSE 8000


# CMD es el comando ejecutado por 'exec "$@"' en entrypoint.sh: arranca servidor web
# gunicorn es mejor que runserver en producción:
# CMD ["gunicorn", "mi_proyecto.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]