#!/bin/bash

# Pfizer AI Brand Planning - Docker Start Script
# Starts the application in Docker containers

echo "🚀 Starting Pfizer AI Brand Planning Platform with Docker..."
echo ""

# Check if .env exists, if not use .env.docker
if [ ! -f .env ]; then
    echo "📝 No .env file found. Using .env.docker defaults (DEMO_MODE=true)"
    cp .env.docker .env
fi

echo "Building and starting containers..."
echo ""

# Build and start containers
docker-compose up --build -d

# Wait for services to be healthy
echo ""
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check service health
echo ""
echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "✅ Services started!"
echo ""
echo "Access the application:"
echo "  Frontend: http://localhost"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "View logs:"
echo "  All services: docker-compose logs -f"
echo "  Backend only: docker-compose logs -f backend"
echo "  Frontend only: docker-compose logs -f frontend"
echo ""
echo "Stop services:"
echo "  docker-compose down"
echo ""
