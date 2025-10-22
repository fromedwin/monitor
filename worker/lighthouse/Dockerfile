FROM zenika/alpine-chrome:with-node
# Using https://github.com/Zenika/alpine-chrome

# Set working directory
USER root
WORKDIR /app

# Copy package files with proper permissions
COPY --chmod=644 worker/lighthouse/package*.json ./
COPY worker/lighthouse/index.js ./

# Install dependencies
RUN npm install