#!/bin/sh

# Establecer la ubicación y el puerto de la base de datos a partir de variables de entorno
DB_HOST=$MYSQL_HOST
DB_PORT=$MYSQL_PORT # (Será 3306 para MySQL o 5432 para PostgreSQL)

echo "Waiting for database host ($DB_HOST:$DB_PORT) to be available..."

# --- 1. SOLUCIÓN AL ERROR DE CONEXIÓN (Race Condition) ---
# Usa netcat (nc) para verificar si el puerto está abierto y aceptando conexiones.
# Este bucle previene errores de timeout (código 2002/115) al inicio.
while ! nc -z $MYSQL_HOST $MYSQL_PORT; do
  sleep 0.5 # Esperar medio segundo antes de reintentar
done

echo "Database port is open. Proceeding with Django setup..."

# --- 2. COMANDOS DE PREPARACIÓN DE DJANGO ---
# Ejecutar la recolección de archivos estáticos
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Aplicar migraciones
echo "Applying database migrations..."
python manage.py migrate

# Crear superusuario por primera vez (solo si es necesario y seguro)
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ] ; then
  echo "Creating superuser..."
  python manage.py createsuperuser --noinput \
    --username "$DJANGO_SUPERUSER_USERNAME" \
    --email "$DJANGO_SUPERUSER_EMAIL"
fi

# --- 3. INICIO DEL SERVIDOR PRINCIPAL ---
# La instrucción 'exec "$@"' pasa el control al CMD definido en el Dockerfile 
# (python manage.py runserver 0.0.0.0:8000)
echo "Starting runserver server..."
exec "$@"