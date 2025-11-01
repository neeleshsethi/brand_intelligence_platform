# Docker & Makefile Guide

Complete guide to running the Pfizer AI Brand Planning Platform with Docker and Make.

---

## 🚀 Quick Start

### Option 1: Makefile (Recommended)

The Makefile provides simple commands for all operations:

```bash
# See all available commands
make help

# Install dependencies (local dev)
make install

# Start locally (no Docker, DEMO_MODE)
make start

# Start with Docker (production build)
make start-docker

# Check status
make status

# Stop services
make stop          # Local
make stop-docker   # Docker
```

### Option 2: Manual Docker Compose

```bash
# Start services
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 📋 Makefile Commands

### General
| Command | Description |
|---------|-------------|
| `make help` | Display all available commands |

### Installation
| Command | Description |
|---------|-------------|
| `make install` | Install frontend + backend dependencies |

### Local Development (No Docker)
| Command | Description |
|---------|-------------|
| `make start` | Start app locally in DEMO_MODE |
| `make stop` | Stop local services |
| `make restart` | Restart local services |
| `make check-ports` | Check if ports 8000, 5173 are available |

### Docker
| Command | Description |
|---------|-------------|
| `make start-docker` | Build and start Docker containers |
| `make stop-docker` | Stop all Docker containers |
| `make restart-docker` | Restart Docker containers |
| `make build` | Build Docker images without starting |
| `make logs` | View all container logs |
| `make logs-backend` | View backend logs only |
| `make logs-frontend` | View frontend logs only |
| `make check-ports-docker` | Check if ports 80, 8000 are available |

### Cleanup
| Command | Description |
|---------|-------------|
| `make clean` | Stop services and clean generated files |
| `make clean-all` | Deep clean (remove node_modules, Docker images) |

### Database
| Command | Description |
|---------|-------------|
| `make db-setup` | Run migrations and seed data |

### Utilities
| Command | Description |
|---------|-------------|
| `make status` | Show status of all services |
| `make demo` | Install deps + start in DEMO_MODE |
| `make test` | Run tests (placeholder) |

---

## 🐳 Docker Architecture

### Services

#### Backend
- **Image**: Python 3.11-slim + uv
- **Port**: 8000
- **Environment**: DEMO_MODE=true, MOCK_MODE=true by default
- **Health Check**: HTTP GET /docs every 30s

#### Frontend
- **Build**: Node 18 + Vite
- **Runtime**: Nginx Alpine
- **Port**: 80 (production) or 3000 (dev)
- **Proxy**: Routes /api → backend:8000
- **Health Check**: HTTP GET / every 30s

### Networks
- **Network Name**: pfizer-brand-planning-network
- **Driver**: bridge
- **Services**: Backend ↔ Frontend

---

## 🔧 Configuration

### Environment Variables

The Docker Compose setup uses a `.env` file at the project root.

**Create from template:**
```bash
cp .env.docker .env
```

**Available variables:**
```bash
# Demo Modes
DEMO_MODE=true          # Cache responses for instant results
MOCK_MODE=true          # Use hardcoded responses (no API calls)

# OpenAI (only if MOCK_MODE=false)
OPENAI_API_KEY=your_key

# LangSmith (optional)
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=
LANGCHAIN_PROJECT=pfizer-brand-planning

# Supabase (only if MOCK_MODE=false)
SUPABASE_URL=
SUPABASE_KEY=
```

### Port Configuration

**Local Development:**
- Backend: http://localhost:8000
- Frontend: http://localhost:5173

**Docker Production:**
- Frontend: http://localhost (port 80)
- Backend: http://localhost:8000

---

## 📝 Common Workflows

### First Time Setup

```bash
# 1. Clone repo
git clone <repo-url>
cd brand-intelligence-platform

# 2. Start with Docker (easiest)
make start-docker

# Wait ~30 seconds for services to build and start
# Open http://localhost in browser
```

### Daily Development

```bash
# Start local dev (faster reload)
make start

# Make changes to code
# Changes auto-reload on both frontend and backend

# Stop when done
make stop
```

### Production Demo

```bash
# Start with Docker (production build)
make start-docker

# View logs if needed
make logs

# Check service health
make status

# Stop when done
make stop-docker
```

### Troubleshooting

```bash
# Clean everything and start fresh
make clean-all
make start-docker

# View container status
make status
docker ps

# View logs for errors
make logs-backend
make logs-frontend

# Rebuild images from scratch
make build
```

---

## 🔍 Port Conflict Resolution

The Makefile automatically checks for port conflicts before starting.

### If Port is Busy

**Local Dev (Port 8000 or 5173):**
```bash
# Check what's using the port
lsof -i :8000

# Kill the process
kill -9 $(lsof -t -i:8000)

# Or let Makefile tell you
make check-ports
```

**Docker (Port 80 or 8000):**
```bash
# Check what's using the port
lsof -i :80

# Kill the process (may need sudo for port 80)
sudo kill -9 $(lsof -t -i:80)

# Or let Makefile tell you
make check-ports-docker
```

---

## 🐛 Debugging

### View Container Logs

```bash
# All logs
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend

# Or use Makefile
make logs
make logs-backend
make logs-frontend
```

### Inspect Container

```bash
# Open shell in backend container
docker-compose exec backend /bin/bash

# Open shell in frontend container
docker-compose exec frontend /bin/sh

# Check Python packages
docker-compose exec backend pip list

# Check running processes
docker-compose exec backend ps aux
```

### Check Health Status

```bash
# All services
docker-compose ps

# Detailed health info
docker inspect pfizer-brand-planning-backend
docker inspect pfizer-brand-planning-frontend

# Or use Makefile
make status
```

---

## 🧪 Testing in Docker

```bash
# Start services
make start-docker

# Run backend tests in container
docker-compose exec backend uv run pytest

# Run frontend tests in container
docker-compose exec frontend npm test

# Or build test image separately
docker build -t pfizer-backend-test ./backend
docker run pfizer-backend-test uv run pytest
```

---

## 📦 Docker Image Management

### Build Images

```bash
# Build all images
make build

# Build specific service
docker-compose build backend
docker-compose build frontend
```

### Image Size Optimization

Our multi-stage builds minimize image size:

**Backend:**
- Base: python:3.11-slim (~130MB)
- Final: ~400MB (with dependencies)

**Frontend:**
- Build stage: node:18-alpine (~150MB)
- Runtime: nginx:alpine (~40MB)
- Final: ~45MB (static assets only)

### Clean Up Images

```bash
# Remove all project images
make clean-all

# Remove unused Docker resources
docker system prune -a

# Remove specific image
docker rmi pfizer-brand-planning-backend
docker rmi pfizer-brand-planning-frontend
```

---

## 🔒 Security Notes

### Production Deployment

For production deployments, update:

1. **Environment Variables**
   - Set strong API keys
   - Disable DEMO_MODE and MOCK_MODE
   - Use secrets management (not .env file)

2. **Nginx Configuration**
   - Add SSL/TLS termination
   - Update CORS origins
   - Add rate limiting
   - Enable access logs

3. **Docker Compose**
   - Remove volume mounts (use built images)
   - Set resource limits (CPU, memory)
   - Use specific image tags (not :latest)
   - Enable Docker secrets

4. **Network**
   - Use Docker networks for isolation
   - Expose only necessary ports
   - Add firewall rules

---

## 🎯 Performance Tips

### Local Development

```bash
# Use local dev for faster iterations
make start  # Hot reload enabled

# Docker has slower file sync
make start-docker  # No hot reload
```

### Docker Build Cache

```bash
# Clear build cache if issues
docker-compose build --no-cache

# Or use Makefile
make clean-all
make build
```

### Volume Performance (Mac/Windows)

For better performance on Mac/Windows, consider:
- Using named volumes instead of bind mounts
- Enabling Docker Desktop file sharing optimization
- Using `:cached` or `:delegated` mount options

---

## 📊 Monitoring

### Health Checks

Services have built-in health checks:

**Backend:**
- Endpoint: http://localhost:8000/docs
- Interval: 30s
- Timeout: 10s
- Retries: 3

**Frontend:**
- Endpoint: http://localhost/
- Interval: 30s
- Timeout: 10s
- Retries: 3

### View Health Status

```bash
# Check health
docker inspect --format='{{.State.Health.Status}}' pfizer-brand-planning-backend

# Or use status command
make status
```

---

## 🆘 FAQ

**Q: How do I switch between DEMO_MODE and production?**
```bash
# Edit .env file
DEMO_MODE=false
MOCK_MODE=false
OPENAI_API_KEY=your_real_key

# Restart
make restart-docker
```

**Q: Frontend can't reach backend**
```bash
# Check network
docker network inspect pfizer-brand-planning-network

# Check nginx config
docker-compose exec frontend cat /etc/nginx/conf.d/default.conf
```

**Q: How do I update dependencies?**
```bash
# Backend
cd backend
uv sync

# Frontend
cd frontend
npm install

# Rebuild Docker
make build
```

**Q: How do I run without Makefile?**
```bash
# Docker Compose directly
docker-compose up --build -d
docker-compose down

# Local dev directly
cd backend && ./scripts/run_demo.sh &
cd frontend && npm run dev &
```

---

## 🔗 Related Documentation

- [README.md](./README.md) - Main documentation
- [QUICK_START.md](./QUICK_START.md) - Getting started guide
- [DEMO_SCRIPT.md](./DEMO_SCRIPT.md) - Demo walkthrough
- [API_GUIDE.md](./backend/API_GUIDE.md) - API documentation

---

**Happy Dockerizing! 🐳**
