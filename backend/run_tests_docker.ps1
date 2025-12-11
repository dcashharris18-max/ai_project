# Build and run tests in a Docker container using python:3.11-slim base
# Usage: .\run_tests_docker.ps1
$tag = "ai_project_backend_test:latest"

Write-Host "Building Docker image: $tag"
docker build -t $tag -f Dockerfile ..

Write-Host "Running tests inside Docker"
docker run --rm -v ${PWD}:C:/app $tag pwsh -Command "cd /app && python -m pytest backend/tests -q" 
