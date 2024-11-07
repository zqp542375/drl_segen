# Use an official Python runtime as a parent image
FROM python:3.10.13-slim

# Set the working directory in the container


# Copy the current directory contents into the container at /app
COPY . /opt/segen/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenmpi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip


# Copy the requirements file
COPY requirements.txt .

# If you have a requirements.txt file
RUN pip install -r requirements.txt


# # Install the dependencies specified in requirements.txt
# # If you don't have a requirements.txt, you can list the packages directly in the Dockerfile
# RUN pip install shimmy sb3-contrib
#
# # If you have a requirements.txt file, uncomment the next line and ensure it contains the necessary packages
# # COPY requirements.txt ./
# # RUN pip install --no-cache-dir -r requirements.txt

RUN cd /opt/segen \
  && python setup.py install

WORKDIR /home/segen/

# # Expose port 5000 for the Flask app
# EXPOSE 5000
#
# # Define environment variable
# ENV NAME World


# # Run app.py when the container launches
# CMD ["python", "app.py"]

ENTRYPOINT ["/usr/local/bin/gen"]