# Base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the requirements
RUN pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port used by the application
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
