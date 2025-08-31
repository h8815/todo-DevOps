# Stage 1: Build stage for installing dependencies (large image: ~1.1 GB)
FROM python:3.13 AS builder   

# Set working directory inside the container
WORKDIR /app

# Copies only requirements.txt from the host to /app in the container
COPY requirements.txt .        

# Install dependencies in the builder image without caching to reduce layer size
RUN pip install --no-cache-dir -r requirements.txt

# ------------------------------------

# Stage 2: Slim image for runtime to reduce image size (slim image: ~133 MB) 
FROM python:3.13-slim  

# Set working directory inside the runtime container
WORKDIR /app

# Copy installed dependencies from builder stage to runtime image
COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13/

# Copy application source code into the runtime image
COPY . .

# Expose port 5000 for the application
EXPOSE 5000

# Command to start the application
CMD ["python", "run.py"]
