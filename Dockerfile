# Use an official Python runtime as the parent image
FROM python:3.11.6-bookworm

ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    texlive \
    pandoc \
    libpq-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary psycopg2

# Copy the current directory (where your Django project is) into the container
COPY . /app/

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE ebook_convert.settings
ENV PYTHONUNBUFFERED 1

# Start the application
CMD ["gunicorn", "ebook-convert.wsgi:application", "--bind", "0.0.0.0:8000"]
