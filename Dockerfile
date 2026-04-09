FROM python:3.11-slim-bookworm

# Crear un usuario no root por seguridad
RUN groupadd -r botgroup && useradd -r -g botgroup botuser

# Establecer la carpeta de trabajo
WORKDIR /app

# Copiar el archivo de dependencias primero para aprovechar cache
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Cambiar los permisos de la aplicación al usuario botuser
RUN chown -R botuser:botgroup /app

# Cambiar al usuario no root
USER botuser

# El puerto interno definido en WEBHOOK_PORT
EXPOSE 8080

# Comando para ejecutar la app
CMD ["python", "main.py"]
