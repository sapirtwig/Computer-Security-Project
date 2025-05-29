# # Use the official Python image
# FROM python:3.11-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Copy the application code to the working directory
# COPY . .

# # Install dependencies
# RUN pip install -r requirements.txt

# # Expose the application port
# EXPOSE 5000

# RUN sleep 25

# CMD ["python", "main.py"]

# Use a minimal official Python base image
FROM python:3.11-slim

# Set environment variables to improve behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy only what we need first (better layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary application files (explicit is safer)
COPY . .

# Set a non-root user for improved security
RUN adduser --disabled-password --no-create-home appuser
USER appuser

# Expose port used by the FastAPI/Flask app
EXPOSE 5000

# Start the application
CMD ["python", "main.py"]
