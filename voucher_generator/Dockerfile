FROM python:3.10-slim

WORKDIR /app

# Install system dependencies if required (e.g., for Pillow)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port and run Gunicorn
EXPOSE 5000
CMD ["gunicorn", "app:app"]