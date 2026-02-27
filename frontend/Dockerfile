# Use official Node.js for build
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Use empty API URL so frontend uses relative URLs (nginx proxies /api to backend)
ENV VITE_API_URL=""

# Build application
RUN npm run build

# Production stage - use nginx
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy SSL certificates
COPY certs/ /etc/nginx/certs/

# Expose ports (HTTP + HTTPS)
EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
