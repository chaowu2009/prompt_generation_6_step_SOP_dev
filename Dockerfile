FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install build deps (kept minimal)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app

EXPOSE 8501
ENV PORT=8501

CMD ["streamlit", "run", "app.py","--server.baseUrlPath","ai-dev","--server.port", "8501", "--server.address", "0.0.0.0"]
