FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
RUN python -u -m  database.migrations.main
EXPOSE 8000
#CMD ["uvicorn", "src.service:app", "--host", "0.0.0.0", "--port", "80"]