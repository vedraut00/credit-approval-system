FROM python:3.9-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
# Install system dependencies
RUN apt-get update && apt-get install -y \
postgresql-client \
gcc \
python3-dev \
&& rm -rf /var/lib/apt/lists/*
# Copy project
COPY . .
# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Create directories
RUN mkdir -p /app/static /app/media
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "credit_system.wsgi:application"]