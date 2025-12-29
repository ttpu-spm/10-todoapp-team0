FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

EXPOSE 3310

# Use gunicorn for production-ready serving on port 3310 ...
CMD ["gunicorn", "--bind", "0.0.0.0:3310", "--chdir", "src", "app:app"]

