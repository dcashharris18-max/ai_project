#!/usr/bin/env pwsh
<#
.SYNOPSIS
    AI Marketplace Platform - Quick Start Script for Windows (PowerShell)
    
.DESCRIPTION
    Starts all required services for local development:
    - Docker Compose (PostgreSQL + Redis)
    - Backend API server (FastAPI)
    - Frontend development server (React)
    
.EXAMPLE
    .\start-dev.ps1
#>

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  AI MARKETPLACE PLATFORM - LOCAL STARTUP" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$services = @(
    @{ Name = "Docker Compose"; Command = "docker-compose up -d"; Port = "5432/6379" },
    @{ Name = "Backend (FastAPI)"; Command = "cd backend; uvicorn app.main:app --reload"; Port = "8000" },
    @{ Name = "Frontend (React)"; Command = "cd frontend; npm start"; Port = "3000" }
)

Write-Host "[1/3] Starting Docker Compose services..." -ForegroundColor Yellow
Write-Host "This will start PostgreSQL (5432) and Redis (6379)" -ForegroundColor Gray

try {
    docker-compose up -d -q
    Start-Sleep -Seconds 2
    Write-Host "✅ Docker Compose started" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Docker Compose failed. Make sure Docker Desktop is running." -ForegroundColor Yellow
    Write-Host "   You can start manually with: docker-compose up -d" -ForegroundColor Gray
}

Write-Host ""
Write-Host "[2/3] Starting Backend API server..." -ForegroundColor Yellow
Write-Host "This will start FastAPI on http://localhost:8000" -ForegroundColor Gray

$backendProcess = Start-Process pwsh -ArgumentList "-NoExit", "-Command", "cd backend; uvicorn app.main:app --reload" -PassThru
Write-Host "✅ Backend process started (PID: $($backendProcess.Id))" -ForegroundColor Green

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "[3/3] Starting Frontend development server..." -ForegroundColor Yellow
Write-Host "This will start React on http://localhost:3000" -ForegroundColor Gray

$frontendProcess = Start-Process pwsh -ArgumentList "-NoExit", "-Command", "cd frontend; npm start" -PassThru
Write-Host "✅ Frontend process started (PID: $($frontendProcess.Id))" -ForegroundColor Green

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   SERVICES STARTING..." -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Backend:     " -ForegroundColor Gray -NoNewline; Write-Host "http://localhost:8000" -ForegroundColor Green
Write-Host "  API Docs:    " -ForegroundColor Gray -NoNewline; Write-Host "http://localhost:8000/docs" -ForegroundColor Green
Write-Host "  Frontend:    " -ForegroundColor Gray -NoNewline; Write-Host "http://localhost:3000" -ForegroundColor Green
Write-Host "  PostgreSQL:  " -ForegroundColor Gray -NoNewline; Write-Host "localhost:5432" -ForegroundColor Green
Write-Host "  Redis:       " -ForegroundColor Gray -NoNewline; Write-Host "localhost:6379" -ForegroundColor Green
Write-Host ""
Write-Host "  Services will be ready in 10-15 seconds" -ForegroundColor Gray
Write-Host "  Check service status with: docker-compose ps" -ForegroundColor Gray
Write-Host ""
Write-Host "  To stop a service:" -ForegroundColor Gray
Write-Host "    - Close the command window, or" -ForegroundColor Gray
Write-Host "    - Press Ctrl+C in the service window" -ForegroundColor Gray
Write-Host ""
Write-Host "  To stop all services:" -ForegroundColor Gray
Write-Host "    docker-compose down" -ForegroundColor Gray
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan

# Keep the script running
Write-Host ""
Write-Host "Press Ctrl+C to exit and stop all services" -ForegroundColor Yellow
Write-Host ""

try {
    while ($true) {
        Start-Sleep -Seconds 10
        
        # Optional: Check if services are still running
        $backendRunning = Get-Process | Where-Object { $_.Id -eq $backendProcess.Id } -ErrorAction SilentlyContinue
        $frontendRunning = Get-Process | Where-Object { $_.Id -eq $frontendProcess.Id } -ErrorAction SilentlyContinue
        
        if (-not $backendRunning) {
            Write-Host "⚠️  Backend process stopped unexpectedly" -ForegroundColor Yellow
        }
        if (-not $frontendRunning) {
            Write-Host "⚠️  Frontend process stopped unexpectedly" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host ""
    Write-Host "Stopping services..." -ForegroundColor Yellow
    
    # Kill processes
    Stop-Process -Id $backendProcess.Id -Force -ErrorAction SilentlyContinue
    Stop-Process -Id $frontendProcess.Id -Force -ErrorAction SilentlyContinue
    
    Write-Host "✅ Services stopped" -ForegroundColor Green
}
