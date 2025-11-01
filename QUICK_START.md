# Quick Start Guide

Get the Pfizer AI Brand Planning Platform running in **under 5 minutes**!

## 🚀 Super Quick Demo (No API Keys Required)

Perfect for your first run or live demos.

### 1. Backend (Terminal 1)
```bash
cd backend
./run_demo.sh
```

**That's it!** The backend starts in DEMO_MODE with instant cached responses.

### 2. Frontend (Terminal 2)
```bash
cd frontend
npm install    # Only needed first time
npm run dev
```

### 3. Open Browser
Navigate to **http://localhost:5173**

### 4. Try the Demo
1. Click "Analyze Brand" on Paxlovid
2. Watch the AI work its magic ✨
3. See animated confidence scores count up
4. Click "View AI Reasoning" on any insight
5. Go back and click "Create Plan" on Eliquis
6. Watch the confetti celebration! 🎉

**Total time: ~2 minutes to running demo**

---

## 🔧 Production Setup (With Real AI)

For actual use with OpenAI API.

### 1. Configure Environment
```bash
cd backend
cp .env.example .env
# Edit .env and add your API keys:
# - OPENAI_API_KEY
# - SUPABASE_URL
# - SUPABASE_KEY
```

### 2. Setup Database
```bash
# Run migrations
psql -h your-supabase-host -U postgres -f db/migrations/001_initial_schema.sql

# Seed demo data
uv run python db/seeds/seed_data.py
```

### 3. Start Backend
```bash
./run_production.sh
```

### 4. Start Frontend
```bash
cd frontend
npm run dev
```

---

## 🎯 What Each Mode Does

| Mode | Speed | Requires API Keys | Use Case |
|------|-------|-------------------|----------|
| **Demo** (`./run_demo.sh`) | ⚡ <1s | ❌ No | Live demos, first run |
| **Production** (`./run_production.sh`) | 🐢 5-10s | ✅ Yes | Real usage with AI |

---

## 📖 Next Steps

- **For demos:** Read [DEMO_SCRIPT.md](./DEMO_SCRIPT.md) for a 2-minute walkthrough
- **For development:** Read [README.md](./README.md) for full documentation
- **For API details:** Read [API_GUIDE.md](./backend/API_GUIDE.md)

---

## 🆘 Troubleshooting

### Backend won't start
```bash
# Install uv if missing
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
cd backend
uv sync
```

### Frontend won't start
```bash
cd frontend
npm install
```

### No brands showing on dashboard
```bash
# Re-run seed script
cd backend
uv run python db/seeds/seed_data.py
```

### Port already in use
```bash
# Backend on different port
uv run uvicorn main:app --reload --port 8001

# Frontend on different port
npm run dev -- --port 5174
```

---

## 🎉 You're Ready!

The platform should now be running with:
- ✅ Backend API at http://localhost:8000
- ✅ Frontend UI at http://localhost:5173
- ✅ API docs at http://localhost:8000/docs

**Enjoy the demo!** 🚀
