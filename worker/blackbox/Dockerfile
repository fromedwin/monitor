# Start with the official Blackbox Exporter image
FROM prom/blackbox-exporter:v0.25.0

# Copy configuration file into the container
COPY ./worker/blackbox/blackbox.yml /etc/prometheus/blackbox.yml
