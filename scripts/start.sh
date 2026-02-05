#!/bin/bash
# 教室预约系统 - 启动脚本

echo "Starting Classroom Reservation System..."

# 启动后端 (端口 8000)
echo "Starting Django backend on port 8000..."
.venv/bin/python backend/manage.py runserver 8000 &
BACKEND_PID=$!

# 等待后端启动
sleep 2

# 启动前端 (端口 8081)
echo "Starting Vue frontend on port 8081..."
cd frontend && npm run serve &
FRONTEND_PID=$!

echo ""
echo "=========================================="
echo "System started successfully!"
echo "=========================================="
echo "Frontend: http://localhost:8081/"
echo "Backend:  http://localhost:8000/api/"
echo "Admin:    http://localhost:8000/admin/"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=========================================="

# 等待用户中断
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM

wait
