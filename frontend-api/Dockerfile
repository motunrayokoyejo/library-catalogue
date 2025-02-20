# FROM python:3.11-slim

# WORKDIR /app
# COPY requirements.txt .
# RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# RUN pip install -r requirements.txt

# COPY . .

# RUN sleep 10
# RUN python /app/configure_alembic.py 

# EXPOSE 8000
# RUN chmod +x /app/entrypoint.sh
# ENV PYTHONPATH=/app:$PYTHONPATH
# ENTRYPOINT ["/app/entrypoint.sh"]
# #CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

COPY . .

RUN sleep 10
RUN python /app/configure_alembic.py 

# RUN alembic upgrade head

EXPOSE 8000

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

ENTRYPOINT ["/app/entrypoint.sh"]