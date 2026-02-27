# ==============================
# Stage 1: Build React Frontend
# ==============================
FROM node:18-alpine AS frontend-builder

WORKDIR /frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ .

ENV VITE_API_URL=""
RUN npm run build

# ==============================
# Stage 2: Python Backend + Frontend
# ==============================
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (git for cloning assets repo)
RUN apt-get update && apt-get install -y \
    gcc \
    ca-certificates \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy frontend build into static/frontend
COPY --from=frontend-builder /frontend/dist /app/static/frontend

# Create directories
RUN mkdir -p uploads static/models static/thumbnails

# Make entrypoint executable
RUN chmod +x entrypoint.sh

EXPOSE 5000

CMD ["./entrypoint.sh"]
