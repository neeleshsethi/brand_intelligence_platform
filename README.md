# Pfizer AI Brand Planning Platform

> **A 2-day rapid prototype** showcasing AI-powered competitive intelligence and strategic brand planning for pharmaceutical companies.

![Status](https://img.shields.io/badge/status-prototype-yellow)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## 🎯 Overview

This platform demonstrates how AI agents can transform pharmaceutical brand planning from **weeks of manual work into minutes of automated analysis**. Built for brand managers, strategic planners, and pharmaceutical executives.

### Key Features

✅ **Competitive Intelligence Analysis**
- Multi-agent AI analysis of competitive landscape
- SWOT analysis with color-coded quadrants
- 2x2 positioning matrix (price vs efficacy)
- AI-generated insights with confidence scores
- Interactive validation/rejection workflow

✅ **Brand Plan Generator**
- Complete 12-month strategic plans in seconds
- Budget allocation ($5M breakdown)
- KPIs and market share projections
- Timeline and risk mitigation strategies
- Export to PDF functionality

✅ **AI Transparency**
- Animated confidence scores (0-100%)
- Expandable AI reasoning for every insight
- Multi-step loading showing what AI is doing
- Validation workflow for human-in-the-loop

✅ **Demo Polish**
- Confetti celebrations on plan completion
- Smooth animations and transitions
- Pfizer blue branding throughout
- DEMO_MODE for instant cached responses

---

## 🚀 Quick Start

> **Want to run this in 2 minutes?** See [QUICK_START.md](./QUICK_START.md) for the fastest path!
>
> **Using Docker or Make?** See [DOCKER_GUIDE.md](./DOCKER_GUIDE.md) for complete Docker + Makefile documentation!

### Prerequisites

- Python 3.11+
- Node.js 18+
- Supabase account (or local PostgreSQL)
- OpenAI API key (optional for DEMO_MODE)

### 1. Backend Setup

```bash
cd backend

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
```

### 2. Database Setup

```bash
# Run migrations
psql -h <your-supabase-host> -U postgres -f db/migrations/001_initial_schema.sql

# Seed demo data
uv run python db/seeds/seed_data.py
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. Run the Application

**Option A: Using Makefile (Recommended)**
```bash
# See all commands
make help

# Start locally (DEMO_MODE, no Docker)
make start

# Or start with Docker (production build)
make start-docker

# Check status
make status

# Stop
make stop              # Local
make stop-docker       # Docker
```

**Option B: Manual Scripts**
```bash
# Terminal 1 - Backend
cd backend
./scripts/run_demo.sh

# Terminal 2 - Frontend
cd frontend
npm run dev
```

**Option C: Docker Compose**
```bash
docker-compose up --build -d
```

### 5. Access the App

**Local Development:**
- Frontend: **http://localhost:5173**
- Backend: **http://localhost:8000**

**Docker:**
- Frontend: **http://localhost**
- Backend: **http://localhost:8000**

---

## 🎬 Demo Guide

👉 **See [DEMO_SCRIPT.md](./DEMO_SCRIPT.md) for a complete 2-minute walkthrough!**

### Quick Demo Flow:

1. **Dashboard** → Click "Analyze Brand" on Paxlovid
2. **Watch AI Processing** → Multi-step loading animation
3. **View Results:**
   - Positioning matrix (2x2 chart)
   - SWOT analysis (4 quadrants)
   - 3 AI insights with animated confidence scores
   - Click "View AI Reasoning" on any insight
   - Click "Validate" to approve an insight
4. **Generate Plan** → Back to Dashboard → "Create Plan" on Eliquis
5. **Watch Plan Generation** → 4-step loading
6. **View Plan:**
   - Market share projection chart
   - 8 expandable sections
   - Click "Export to PDF" → Confetti celebration! 🎉

---

## 🎨 Key "Wow" Moments

### 1. Animated Confidence Scores
Confidence bars count up from 0% to final value with color coding

### 2. Expandable AI Reasoning
Every insight shows why the AI made this recommendation

### 3. Confetti Celebration
50 colorful confetti particles fall when plan is generated

### 4. Multi-Step Loading
Shows exactly what the AI is doing in real-time

---

## 🔧 Configuration

### Demo Modes

| Mode | Use Case | Speed | API Calls | LLM Calls |
|------|----------|-------|-----------|-----------|
| **Production** | Real usage | 5-10s | ✅ | ✅ |
| **DEMO_MODE** | Fast demos | 1-2s | ✅ (cached) | ✅ (cached) |
| **MOCK_MODE** | No API keys | <1s | ❌ | ❌ |

**Recommendation:** Use `DEMO_MODE=true MOCK_MODE=true` for first demo

---

## 📂 Project Structure

```
brand-intelligence-platform/
├── backend/
│   ├── agents/              # 6 AI agents
│   ├── api/                 # FastAPI endpoints
│   ├── core/                # Configuration
│   ├── db/                  # Database migrations & seeds
│   └── main.py              # App entry point
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # 3 main pages
│   │   └── lib/             # API client & utilities
│   └── package.json
├── DEMO_SCRIPT.md           # 2-minute demo guide
└── README.md                # This file
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/brands` | List all brands |
| POST | `/api/analyze/{brand_id}` | Run competitive analysis |
| POST | `/api/generate-plan/{brand_id}` | Generate strategic plan |
| POST | `/api/scenario` | Analyze what-if scenario |
| POST | `/api/validate` | Validate AI content |

👉 **See [API_GUIDE.md](./backend/API_GUIDE.md) for complete docs**

---

## 🚧 Known Limitations (Prototype)

This is a **2-day rapid prototype**. For production:

- [ ] User authentication
- [ ] Real-time data integration
- [ ] Custom LLM fine-tuning
- [ ] PDF export (real generation)
- [ ] Mobile responsive design
- [ ] Comprehensive tests
- [ ] Security hardening

---

## 📝 Tech Stack

**Backend:** FastAPI + OpenAI GPT-4 + Supabase
**Frontend:** React + TypeScript + Tailwind + Recharts
**Package Managers:** uv (Python) + npm (JavaScript)

---

## 📄 License

MIT License

---

## 📧 Contact

For questions or demo requests, open a GitHub issue.

**Let's transform pharmaceutical brand planning together! 🚀**
