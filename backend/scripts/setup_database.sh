#!/bin/bash
# Database setup script for Pfizer AI Brand Planning

set -e

echo "========================================="
echo "Pfizer AI Brand Planning - Database Setup"
echo "========================================="
echo ""

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "Error: backend/.env file not found!"
    echo "Please copy backend/.env.example to backend/.env and configure your Supabase credentials."
    exit 1
fi

echo "Step 1: Apply SQL migrations to Supabase"
echo "-----------------------------------------"
echo ""
echo "Please manually run the migration in your Supabase SQL Editor:"
echo "  1. Go to your Supabase project: https://app.supabase.com"
echo "  2. Navigate to SQL Editor"
echo "  3. Copy and paste the contents of: backend/db/migrations/001_initial_schema.sql"
echo "  4. Click 'Run' to execute the migration"
echo ""
read -p "Press Enter once you've completed the migration..."

echo ""
echo "Step 2: Seed the database with demo data"
echo "-----------------------------------------"
echo ""

# Check if we're in the backend directory
if [ -d "backend" ]; then
    cd backend
fi

# Run the seed script
echo "Running seed script..."
python -m db.seeds.seed_data

echo ""
echo "========================================="
echo "Database setup completed!"
echo "========================================="
echo ""
echo "Next steps:"
echo "  1. Start the application: docker-compose up"
echo "  2. Access the API at: http://localhost:8000/docs"
echo ""
