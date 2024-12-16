# Use the Python slim image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /meditrack/notification

# Copy the current directory contents into the container
COPY . .

# Install system dependencies required for pyodbc
RUN apt-get update && apt-get install -y \
    g++ \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the port the service runs on
EXPOSE 5000

# Define the command to run the service
# CMD ["python", "patients.py"]
CMD ["python", "doctors.py"]
# CMD ["python", "notification.py"]
# CMD ["python", "appointment.py"]
