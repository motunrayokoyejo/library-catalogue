FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

COPY . .

RUN sleep 10
RUN python /app/configure_alembic.py 

# RUN alembic upgrade head

EXPOSE 8001

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]

ENTRYPOINT ["/app/entrypoint.sh"]