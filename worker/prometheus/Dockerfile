# Start with the official Prometheus image
FROM prom/prometheus:v2.54.1

# Create directories for configuration files
RUN mkdir -p /etc/prometheus/alerts

# Copy initial configuration files into the container
# These will be overridden by the heartbeats service via shared volume
COPY ./worker/prometheus/prometheus.template.yml /etc/prometheus/prometheus.yml
COPY ./worker/prometheus/alerts/alerts.template.yml /etc/prometheus/alerts/alerts.yml
