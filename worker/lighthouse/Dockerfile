FROM zenika/alpine-chrome:with-node
# Using https://github.com/Zenika/alpine-chrome

# Set working directory
USER root
WORKDIR /app

# Copy package files with proper permissions
COPY --chmod=644 package*.json ./

# Install dependencies
RUN npm install

# Copy application files
COPY index.js ./
COPY run.sh ./

# Make run.sh executable
RUN chmod +x run.sh

# Set the default command
CMD ["./run.sh"]