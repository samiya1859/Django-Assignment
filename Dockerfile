FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (needed for Django, PostgreSQL, GDAL, etc.)
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    libpq-dev \
    binutils \
    libproj-dev \
    python3-gdal \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for GDAL to work correctly
ENV GDAL_VERSION=3.6.2  
ENV GDAL_CONFIG=/usr/local/bin/gdal-config  

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project into the container
COPY . /app/

# Expose the port Django will run on (default is 8000)
EXPOSE 8000

# Command to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
