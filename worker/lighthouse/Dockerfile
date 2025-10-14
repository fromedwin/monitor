FROM zenika/alpine-chrome:with-node
# Using https://github.com/Zenika/alpine-chrome

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Fix permissions for npm to work properly
RUN chown -R node:node /app && chmod -R 755 /app

# Install dependencies
RUN npm install

# Copy application files
COPY index.js ./
COPY run.sh ./

# Make run.sh executable
RUN chmod +x run.sh

# Set the default command
CMD ["./run.sh"]