# Use an official lightweight Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg gcc && rm -rf /var/lib/apt/lists/*

# Force clean reinstall
ARG CACHEBUSTER=5

# Install Python dependencies and dump dependency tree
COPY requirements.txt /app/
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --trusted-host pypi.org -r requirements.txt || true && \
    pip install pipdeptree && \
    python -m pipdeptree | tee /tmp/deps.log && \
    python -c "import pydantic; print('Using Pydantic:', pydantic.__version__)"

# ✅ Preload HuggingFace model *after* installing packages
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-mpnet-base-v2')"

# Copy project files
COPY . /app/

# Expose the port
EXPOSE 8080

# Start the app
CMD ["pipdeptree", "--warn", "fail"]

