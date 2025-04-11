FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn for running the app in production mode
RUN pip install gunicorn

COPY . .

EXPOSE 5000

# Run the app with Gunicorn in production mode
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
