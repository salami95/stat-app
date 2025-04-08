# Use an official lightweight Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg gcc && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --upgrade openai==1.17.0 langchain==0.1.16


# Copy project files
COPY . /app/

# Expose the port
EXPOSE 8080

# Start the app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
