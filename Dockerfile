# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file first (if you have one)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your code into the container
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the port (if using HTTP transport)
EXPOSE 10000

# Command to start your MCP server
CMD ["python", "server.py"]
