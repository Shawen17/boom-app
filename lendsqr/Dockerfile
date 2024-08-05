# FROM node:18-alpine

# # Set the working directory in the container
# WORKDIR /app


# # Copy package.json and yarn.lock to the working directory
# COPY package.json yarn.lock ./


# # Install project dependencies
# RUN yarn install

# # Copy the entire project to the working directory
# COPY . .

# # Build the React app for production
# RUN yarn build

# # Expose the port the app runs on
# EXPOSE 3000

# # Start the React app
# CMD ["yarn", "start"]


# First stage: Build the React app
FROM node:18-alpine AS build-stage

# Set working directory
WORKDIR /app

# Copy package.json and yarn.lock to the working directory
COPY package.json yarn.lock ./

# Install project dependencies
RUN yarn install

# Copy the entire project to the working directory
COPY . .

# Build the app
RUN yarn build

# Second stage: Serve the React app with Nginx
FROM nginx:1.15

# Copy custom Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the build output to Nginx's html directory
COPY --from=build-stage /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
