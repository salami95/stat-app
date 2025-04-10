FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY topic_processor.py .

CMD ["python", "topic_processor.py"]
