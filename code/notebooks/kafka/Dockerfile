FROM python:3.10-slim

WORKDIR /app

COPY .requirements.txt .
COPY ./src/producer.py .
COPY ./src/admin.py .
COPY ./src/utils.py

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "producer.py"]
