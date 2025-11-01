#!/bin/bash

# Pfizer AI Brand Planning - Production Mode Launcher
# This script starts the backend with real API calls

echo "🚀 Starting Pfizer AI Brand Planning Platform in PRODUCTION MODE..."
echo ""
echo "Features enabled:"
echo "  ✅ Real OpenAI API calls (requires OPENAI_API_KEY)"
echo "  ✅ LangSmith tracing (optional)"
echo "  ✅ Supabase database integration"
echo ""
echo "⚠️  Make sure your .env file is configured with API keys!"
echo ""
echo "Access the API at: http://localhost:8000"
echo "API docs at: http://localhost:8000/docs"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "   Copy .env.example to .env and add your API keys:"
    echo "   cp .env.example .env"
    exit 1
fi

# Start the server (will load from .env)
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
