FROM python:3.8

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory to /app
WORKDIR /app

# Make port 80 available
# Define environment variable

# Run app.py when the container launches
CMD ["python", "app.py"]