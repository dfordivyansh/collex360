# Base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies required for psycopg2 and Pillow
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt /app/

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Explicitly install psycopg2-binary (PostgreSQL driver)
RUN pip install psycopg2-binary

# Copy project files
COPY . /app/

# Collect static files (WhiteNoise will serve them)
RUN python manage.py collectstatic --noinput

# Expose port for Railway
EXPOSE 8000

# Run Gunicorn server
CMD ["gunicorn", "collex360.wsgi:application", "--bind", "0.0.0.0:8000"]
