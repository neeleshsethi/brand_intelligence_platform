.PHONY: help install start start-docker stop stop-docker clean check-ports test build logs status

# Default target
.DEFAULT_GOAL := help

# Colors for output
CYAN := \033[0;36m
GREEN := \033[0;32m
RED := \033[0;31m
YELLOW := \033[1;33m
NC := \033[0m # No Color

##@ General

help: ## Display this help message
	@echo "$(CYAN)╔══════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(CYAN)║   Pfizer AI Brand Planning Platform - Make Commands     ║$(NC)"
	@echo "$(CYAN)╚══════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf ""} /^[a-zA-Z_-]+:.*?##/ { printf "  $(CYAN)%-20s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(YELLOW)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@echo ""

##@ Installation

install: ## Install all dependencies (frontend + backend)
	@echo "$(CYAN)📦 Installing dependencies...$(NC)"
	@echo "$(GREEN)→ Installing backend dependencies with uv...$(NC)"
	@cd backend && uv sync
	@echo "$(GREEN)→ Installing frontend dependencies with npm...$(NC)"
	@cd frontend && npm install
	@echo "$(GREEN)✓ Dependencies installed successfully!$(NC)"

##@ Development (Local)

check-ports: ## Check if required ports (8000, 5173) are available
	@echo "$(CYAN)🔍 Checking port availability...$(NC)"
	@if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then \
		echo "$(RED)✗ Port 8000 is already in use!$(NC)"; \
		echo "$(YELLOW)  Kill process: kill -9 $$(lsof -t -i:8000)$(NC)"; \
		exit 1; \
	fi
	@if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null 2>&1 ; then \
		echo "$(RED)✗ Port 5173 is already in use!$(NC)"; \
		echo "$(YELLOW)  Kill process: kill -9 $$(lsof -t -i:5173)$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)✓ Ports 8000 and 5173 are available!$(NC)"

start: check-ports ## Start the app locally (DEMO_MODE, no Docker)
	@echo "$(CYAN)🚀 Starting Pfizer AI Brand Planning Platform (Local)...$(NC)"
	@echo ""
	@echo "$(GREEN)Starting backend (DEMO_MODE) on http://localhost:8000$(NC)"
	@cd backend && ../scripts/run_demo.sh & echo $$! > ../.backend.pid
	@sleep 3
	@echo "$(GREEN)Starting frontend on http://localhost:5173$(NC)"
	@cd frontend && npm run dev & echo $$! > ../.frontend.pid
	@echo ""
	@echo "$(GREEN)✅ Application started!$(NC)"
	@echo ""
	@echo "$(CYAN)Access points:$(NC)"
	@echo "  🌐 Frontend:  $(GREEN)http://localhost:5173$(NC)"
	@echo "  ⚡ Backend:   $(GREEN)http://localhost:8000$(NC)"
	@echo "  📚 API Docs:  $(GREEN)http://localhost:8000/docs$(NC)"
	@echo ""
	@echo "$(YELLOW)Commands:$(NC)"
	@echo "  Stop:   $(CYAN)make stop$(NC)"
	@echo "  Status: $(CYAN)make status$(NC)"
	@echo ""

stop: ## Stop the locally running app
	@echo "$(CYAN)🛑 Stopping local services...$(NC)"
	@if [ -f .backend.pid ]; then \
		echo "$(GREEN)→ Stopping backend (PID: $$(cat .backend.pid))...$(NC)"; \
		kill $$(cat .backend.pid) 2>/dev/null || true; \
		rm .backend.pid; \
	fi
	@if [ -f .frontend.pid ]; then \
		echo "$(GREEN)→ Stopping frontend (PID: $$(cat .frontend.pid))...$(NC)"; \
		kill $$(cat .frontend.pid) 2>/dev/null || true; \
		rm .frontend.pid; \
	fi
	@pkill -f "uvicorn main:app" 2>/dev/null || true
	@pkill -f "vite" 2>/dev/null || true
	@echo "$(GREEN)✓ Local services stopped!$(NC)"

##@ Docker

check-ports-docker: ## Check if Docker ports (3000, 8000) are available
	@echo "$(CYAN)🔍 Checking Docker port availability...$(NC)"
	@if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then \
		echo "$(RED)✗ Port 3000 is already in use!$(NC)"; \
		echo "$(YELLOW)  Kill process: kill -9 $$(lsof -t -i:3000)$(NC)"; \
		exit 1; \
	fi
	@if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then \
		echo "$(RED)✗ Port 8000 is already in use!$(NC)"; \
		echo "$(YELLOW)  Kill process: kill -9 $$(lsof -t -i:8000)$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)✓ Ports 3000 and 8000 are available!$(NC)"

start-docker: check-ports-docker ## Start with Docker Compose (production build)
	@echo "$(CYAN)🐳 Starting with Docker Compose...$(NC)"
	@echo "$(GREEN)Building and starting containers...$(NC)"
	@docker-compose up --build -d
	@echo "$(GREEN)Waiting for services to initialize...$(NC)"
	@sleep 5
	@echo ""
	@echo "$(GREEN)✅ Docker containers started!$(NC)"
	@echo ""
	@echo "$(CYAN)Access points:$(NC)"
	@echo "  🌐 Frontend:  $(GREEN)http://localhost:3000$(NC)"
	@echo "  ⚡ Backend:   $(GREEN)http://localhost:8000$(NC)"
	@echo "  📚 API Docs:  $(GREEN)http://localhost:8000/docs$(NC)"
	@echo ""
	@echo "$(YELLOW)Commands:$(NC)"
	@echo "  View logs:  $(CYAN)make logs$(NC)"
	@echo "  Stop:       $(CYAN)make stop-docker$(NC)"
	@echo "  Status:     $(CYAN)make status$(NC)"
	@echo ""

stop-docker: ## Stop all Docker containers
	@echo "$(CYAN)🛑 Stopping Docker containers...$(NC)"
	@docker-compose down
	@echo "$(GREEN)✓ Docker containers stopped!$(NC)"

logs: ## View all Docker container logs
	@echo "$(CYAN)📋 Viewing Docker logs (Ctrl+C to exit)...$(NC)"
	@docker-compose logs -f

logs-backend: ## View backend Docker logs only
	@echo "$(CYAN)📋 Viewing backend logs (Ctrl+C to exit)...$(NC)"
	@docker-compose logs -f backend

logs-frontend: ## View frontend Docker logs only
	@echo "$(CYAN)📋 Viewing frontend logs (Ctrl+C to exit)...$(NC)"
	@docker-compose logs -f frontend

build: ## Build Docker images without starting
	@echo "$(CYAN)🔨 Building Docker images...$(NC)"
	@docker-compose build
	@echo "$(GREEN)✓ Docker images built!$(NC)"

##@ Cleanup

clean: stop stop-docker ## Clean generated files and stop all services
	@echo "$(CYAN)🧹 Cleaning up...$(NC)"
	@echo "$(GREEN)→ Stopping all services...$(NC)"
	@docker-compose down -v 2>/dev/null || true
	@rm -f .backend.pid .frontend.pid
	@echo "$(GREEN)→ Removing Python cache...$(NC)"
	@find backend -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find backend -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete!$(NC)"

clean-all: clean ## Deep clean (remove node_modules, build artifacts, Docker images)
	@echo "$(CYAN)🧹 Deep cleaning...$(NC)"
	@echo "$(GREEN)→ Removing node_modules...$(NC)"
	@rm -rf frontend/node_modules
	@echo "$(GREEN)→ Removing build artifacts...$(NC)"
	@rm -rf frontend/dist frontend/build
	@echo "$(GREEN)→ Removing Docker images...$(NC)"
	@docker-compose down -v --rmi all 2>/dev/null || true
	@echo "$(GREEN)✓ Deep cleanup complete!$(NC)"

##@ Database

db-setup: ## Setup database (run migrations and seed data)
	@echo "$(CYAN)🗄️  Setting up database...$(NC)"
	@echo "$(YELLOW)⚠️  Make sure Supabase credentials are in .env$(NC)"
	@echo "$(GREEN)→ Testing connection...$(NC)"
	@cd backend && uv run python -c "from db.supabase_client import SupabaseClient; client = SupabaseClient.get_client(); print('✓ Connected to Supabase!')"
	@echo "$(GREEN)→ Seeding data...$(NC)"
	@cd backend && uv run python db/seeds/seed_data.py
	@echo "$(GREEN)✓ Database setup complete!$(NC)"

##@ Utilities

status: ## Show status of all services
	@echo "$(CYAN)📊 Service Status$(NC)"
	@echo ""
	@echo "$(YELLOW)Local Services:$(NC)"
	@if [ -f .backend.pid ] && kill -0 $$(cat .backend.pid) 2>/dev/null; then \
		echo "  Backend:  $(GREEN)●$(NC) Running (PID: $$(cat .backend.pid))"; \
	else \
		echo "  Backend:  $(RED)●$(NC) Stopped"; \
	fi
	@if [ -f .frontend.pid ] && kill -0 $$(cat .frontend.pid) 2>/dev/null; then \
		echo "  Frontend: $(GREEN)●$(NC) Running (PID: $$(cat .frontend.pid))"; \
	else \
		echo "  Frontend: $(RED)●$(NC) Stopped"; \
	fi
	@echo ""
	@echo "$(YELLOW)Docker Containers:$(NC)"
	@docker-compose ps 2>/dev/null || echo "  $(RED)●$(NC) No containers running"
	@echo ""

restart: stop start ## Restart local services

restart-docker: stop-docker start-docker ## Restart Docker containers

demo: install start ## Quick demo setup (install deps + start in demo mode)

test: ## Run all tests (placeholder)
	@echo "$(CYAN)🧪 Running tests...$(NC)"
	@echo "$(YELLOW)Tests not yet implemented$(NC)"
