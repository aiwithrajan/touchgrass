#!/bin/bash
set -e

echo "🌱 Starting TOUCHGRASS: AI that gives you a reason to leave the screen."

# Build frontend if needed
if [ ! -d "frontend/dist" ]; then
  echo "Building frontend bundle..."
  cd frontend
  npm run build
  cd ..
fi

echo "Launching TouchGrass FastAPI & Unified App on http://localhost:8000..."
.venv/bin/uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
