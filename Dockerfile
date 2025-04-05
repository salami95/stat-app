# Use slim version of Python to keep image size down
FROM python:3.12-slim

# Install system dependencies (add others like gcc if needed)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files into container
COPY . /app

# Install Python dependencies (no cache for speed)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 8080

# Start your app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
