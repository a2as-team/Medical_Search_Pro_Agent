# Use the official Python image
FROM python:3.13-slim

WORKDIR /app

# Install build tools and PostgreSQL client library
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Create a non-privileged user
RUN adduser --disabled-password --gecos "" myuser

# Copy dependency files and install dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application code
COPY . .

# Give our user ownership of the app directory
RUN chown -R myuser:myuser /app

# Switch to the non-privileged user
USER myuser

# Expose the port the app runs on
EXPOSE 8080

# Run the application directly with python
CMD ["python", "main.py"]