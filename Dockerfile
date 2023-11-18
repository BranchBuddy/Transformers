# Use the official Python image as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /

# Copy the requirements file into the container at /app
COPY . .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask-restx
RUN pip install flasgger


# Specify the command to run on container start
CMD ["python", "/app.py"]
