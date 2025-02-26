
echo "Waiting for MySQL to be ready..."

while ! nc -z mysql_container 3306; do
  sleep 1
done

echo "MySQL is up - Running migrations..."
alembic upgrade head

echo "Starting Backend API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8001
