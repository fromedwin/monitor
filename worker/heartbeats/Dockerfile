# Start with an official Python image
FROM python:latest

# Set the PYTHONUNBUFFERED environment variable
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /etc/fromedwin_heartbeats/worker/heartbeats

# Copy the requirements file and Python scripts into the container
COPY ./worker/heartbeats/requirements.txt /etc/fromedwin_heartbeats/worker/heartbeats/requirements.txt
COPY ./worker/heartbeats/heartbeats.py /etc/fromedwin_heartbeats/worker/heartbeats/heartbeats.py
COPY ./worker/heartbeats/load_config.py /etc/fromedwin_heartbeats/worker/heartbeats/load_config.py
COPY ./worker/heartbeats/register.py /etc/fromedwin_heartbeats/worker/heartbeats/register.py

# Update pip and install dependencies
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt
