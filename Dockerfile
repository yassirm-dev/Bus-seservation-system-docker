# Use the official Python image from the Docker Hub
FROM python:3.9-slim


# Set the working directory
WORKDIR .

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose the port the app runs on
EXPOSE 80

# Start the application using Django's runserver
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]

