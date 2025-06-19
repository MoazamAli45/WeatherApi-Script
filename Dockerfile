# Use official Python runtime as base image
FROM python:3.13-slim

# Set timezone to Asia/Karachi
RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/Asia/Karachi /etc/localtime && \
    echo "Asia/Karachi" > /etc/timezone && \
    apt-get clean



    
# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose port 8000
EXPOSE 8000

# No CMD here, letting docker-compose override it