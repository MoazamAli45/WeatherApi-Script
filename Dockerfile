# Use official Python runtime as base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Set timezone to Asia/Karachi
RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/Asia/Karachi /etc/localtime && \
    echo "Asia/Karachi" > /etc/timezone && \
    apt-get clean

# Copy the rest of the application
COPY . .

# Expose port 8000
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]