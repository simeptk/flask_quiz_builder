# Use a lightweight Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (important for Docker layer caching)
# COPY requirements.txt .

# Install dependencies from requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir Flask markdown

# Copy the rest of the application code, data, and schema into the container
COPY app.py .
COPY quiz_data.json .
COPY CheatSheet-set001.md .
COPY schema.sql .
COPY templates/ templates/

# Expose the port the Flask app runs on
EXPOSE 5000

# Initialize the database when the container starts building
# Running init-db during build ensures the schema is set up in the image
# This is okay for a single-user SQLite app, but for multi-user/persistent DB,
# you'd handle initialization differently (e.g., entrypoint script, migrations).
# RUN flask --app app init-db

# Command to run the Flask development server
# In production, you would use a production WSGI server like Gunicorn:
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
# For development, use Flask's built-in server (debug=False in production!)
CMD ["python", "app.py"]

# Note: debug=True should ideally be False in a production Docker image
# Consider setting FLASK_ENV=production or similar if you have env-specific config
