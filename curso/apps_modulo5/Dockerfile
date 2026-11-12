FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Generar el modelo con las mismas librerías que tendrá el contenedor.
RUN python entrenar_modelo.py \
    && useradd --create-home dashboard \
    && chown -R dashboard:dashboard /app
USER dashboard

EXPOSE 8080
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:server"]
