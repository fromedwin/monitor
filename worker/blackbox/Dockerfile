# Start with the official Blackbox Exporter image
FROM prom/blackbox-exporter:v0.25.0

# Copy configuration file into the container
COPY ./worker/blackbox/blackbox.template.yml /etc/prometheus/blackbox.yml
