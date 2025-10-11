# Start with an official Python image
FROM python:latest

# Set the PYTHONUNBUFFERED environment variable
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /etc/fromedwin_heartbeats/worker/heartbeats

# Copy the requirements file into the container
COPY ./worker/heartbeats/requirements.txt /etc/fromedwin_heartbeats/worker/heartbeats/requirements.txt

# Update pip and install dependencies
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt
