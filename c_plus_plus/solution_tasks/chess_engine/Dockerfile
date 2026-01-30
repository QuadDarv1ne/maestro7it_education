FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements_fastapi.txt .
RUN pip install --no-cache-dir -r requirements_fastapi.txt

# Copy application code with correct paths
COPY core/ ./core/
COPY interfaces/ ./interfaces/
COPY web/ ./web/

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "interfaces.fastapi_chess:app", "--host", "0.0.0.0", "--port", "8000"]