# Use Python 3.12 as base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY app/requirements.txt .

# Install the necessary dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the Flask app source code into the container
COPY app .

# Expose the port the app will run on
EXPOSE 8080

# Set environment variable for Flask app
ENV FLASK_APP=main.py

# Set Flask to run on port 8080 (optional, since we expose port 8080)
ENV FLASK_RUN_PORT=8080

# Command to run the Flask app
CMD ["python", "main.py"]