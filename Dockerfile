FROM python:3.11-slim

# Install system dependencies needed for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy only requirements first (to leverage Docker cache)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Ensure wait-for-it.py is executable (if you’re using it)
RUN chmod +x wait-for-it.py

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]