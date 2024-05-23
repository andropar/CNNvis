# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Install Node.js
RUN apt-get update && apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Install OpenCV dependencies
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-dev \
    libglib2.0-0

RUN apt-get update && apt-get install -y procps

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r /app/backend/requirements.txt

WORKDIR /app/backend/scripts
RUN python download_alexnet.py

# Install frontend dependencies
WORKDIR /app/frontend
RUN npm install
RUN npm run build
RUN npm install -g serve

# Make port 8005 available to the world outside this container
EXPOSE 8005

# Make port 3000 available to the world outside this container (for React dev server)
EXPOSE 3000

# Run app.py when the container launches
WORKDIR /app
RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]

