#!/bin/bash
echo "🚀 ILUMINATE Full Deploy Script"
echo "================================"

# 1. Clear all caches
echo "🧹 Clearing caches..."
rm -rf frontend/node_modules/.cache
rm -rf backend/__pycache__
rm -rf .pytest_cache
npm cache clean --force 2>/dev/null || true
pip cache purge 2>/dev/null || true

# 2. Stop existing containers
echo "🛑 Stopping existing services..."
# docker-compose down --volumes --remove-orphans

# 3. Build and start services
echo "🔨 Building and starting services..."
# docker-compose up --build -d

# Alternative: Start services manually
echo "🔄 Starting backend..."
cd backend
source ../.venv/Scripts/activate
python main.py &
BACKEND_PID=$!
cd ..

echo "🔄 Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# 4. Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 15

# 5. Health checks
echo "🏥 Running health checks..."
if curl -s --max-time 10 http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ Backend API: OK"
else
    echo "❌ Backend API: FAILED"
fi

if curl -s --max-time 10 http://localhost:5173 > /dev/null 2>&1; then
    echo "✅ Frontend: OK"
else
    echo "❌ Frontend: FAILED"
fi

echo ""
echo "🎉 Deploy complete!"
echo "📱 Frontend: http://localhost:5173"
echo "🔗 API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Processes running in background:"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"