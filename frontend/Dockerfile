FROM python:3.10-slim

WORKDIR /app

# Copy source modules first
COPY frontend /app/frontend
COPY utils /app/utils

# Install curl untuk testing di dalam container
RUN apt-get update && apt-get install -y curl

RUN pip install --no-cache-dir -r frontend/requirements.txt


# Set environment variables
ENV STREAMLIT_SERVER_PORT=8501

EXPOSE 5000

# Use Flask development server
# CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
# CMD ["python", "-m", "backend.backend"]
CMD ["python", "-m" ,"streamlit.web.cli", "run", "frontend/frontend.py"]