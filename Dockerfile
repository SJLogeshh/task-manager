FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Run migrations + start server (PRODUCTION STYLE FOR AZURE)
CMD sh -c "python manage.py migrate && gunicorn demo_project.wsgi:application --bind 0.0.0.0:8000"