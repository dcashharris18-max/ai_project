@echo off
REM AI Marketplace Platform - Quick Start Script for Windows
REM This script starts all required services for local development

echo.
echo ============================================
echo   AI MARKETPLACE PLATFORM - LOCAL STARTUP
echo ============================================
echo.

REM Set color
color 0A

echo [1/4] Starting Docker Compose services...
cd docker-compose up -d 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Docker Compose failed. Make sure Docker is installed.
    echo You can start manually with: docker-compose up -d
)
timeout /t 3 /nobreak

echo.
echo [2/4] Starting Backend server...
echo Starting on http://localhost:8000
start cmd /k "cd backend && uvicorn app.main:app --reload"
timeout /t 2 /nobreak

echo.
echo [3/4] Starting Frontend server...
echo Starting on http://localhost:3000
start cmd /k "cd frontend && npm start"
timeout /t 2 /nobreak

echo.
echo ============================================
echo   SERVICES STARTING...
echo ============================================
echo.
echo Backend:     http://localhost:8000
echo API Docs:    http://localhost:8000/docs
echo Frontend:    http://localhost:3000
echo PostgreSQL:  localhost:5432
echo Redis:       localhost:6379
echo.
echo Services will be ready in 10-15 seconds
echo Press CTRL+C in any window to stop a service
echo.
echo ============================================
