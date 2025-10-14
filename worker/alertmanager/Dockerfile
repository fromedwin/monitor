# Start with the official Alertmanager image
FROM quay.io/prometheus/alertmanager:v0.27.0

# Copy initial configuration file into the container
# This will be overridden by the heartbeats service via shared volume
COPY ./worker/alertmanager/alertmanager.yml /etc/alertmanager/alertmanager.yml
