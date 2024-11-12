FROM python:3.10-slim

WORKDIR /app

# Copy source modules first
COPY backend /app/backend
COPY utils /app/utils

# Install curl untuk testing di dalam container
RUN apt-get update && apt-get install -y curl

RUN pip install --no-cache-dir -r backend/requirements.txt


# Set environment variables
ENV FLASK_APP=backend.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Use Flask development server
# CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
CMD ["python", "-m", "backend.backend"]