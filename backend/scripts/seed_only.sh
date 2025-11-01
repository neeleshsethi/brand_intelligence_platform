#!/bin/bash
# Quick script to re-seed data without running migrations

set -e

echo "Re-seeding database with demo data..."
echo ""

# Check if we're in the backend directory
if [ -d "backend" ]; then
    cd backend
fi

# Run the seed script
python -m db.seeds.seed_data

echo ""
echo "Done! Database re-seeded successfully."
