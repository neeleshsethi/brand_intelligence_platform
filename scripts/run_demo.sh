#!/bin/bash

# Pfizer AI Brand Planning - Demo Mode Launcher
# This script starts the backend in DEMO_MODE for impressive live demos

echo "🚀 Starting Pfizer AI Brand Planning Platform in DEMO MODE..."
echo ""
echo "Features enabled:"
echo "  ✅ DEMO_MODE - Instant cached responses (1-2 seconds)"
echo "  ✅ MOCK_MODE - Works without API keys"
echo ""
echo "Access the API at: http://localhost:8000"
echo "API docs at: http://localhost:8000/docs"
echo ""

# Set demo environment variables
export DEMO_MODE=true
export MOCK_MODE=true

# Start the server
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
