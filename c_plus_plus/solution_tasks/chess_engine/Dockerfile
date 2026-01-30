FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements_fastapi.txt .
RUN pip install --no-cache-dir -r requirements_fastapi.txt

# Copy application code
COPY chess_engine_wrapper.py .
COPY optimized_move_generator.py .
COPY enhanced_chess_ai.py .
COPY fastapi_chess.py .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "fastapi_chess:app", "--host", "0.0.0.0", "--port", "8000"]