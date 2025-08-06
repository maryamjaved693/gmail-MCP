FROM python:3.11-slim

WORKDIR /app

# Install pip dependencies directly
RUN pip install --no-cache-dir resend fastmcp

# Copy your application code
COPY . .

ENV PYTHONUNBUFFERED=1

# Expose port if needed (for HTTP transport)
EXPOSE 10000

# Start your MCP server
CMD ["python", "server.py"]
