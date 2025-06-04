# Use Node.js for building and running the application
FROM node:16-alpine

WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Expose port 3000 for React development server
EXPOSE 3000

# Start the React development server
CMD ["npm", "start"]
