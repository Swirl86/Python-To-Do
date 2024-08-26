# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy only requirements.txt and install dependencies
# This allows for better cache usage for pip installation
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app
ENV FLASK_ENV=development

# Start the application
CMD ["flask", "run", "--host=0.0.0.0"]
