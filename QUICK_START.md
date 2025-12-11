# ⚡ Quick Start Reference Guide

**Platform:** AI Marketplace  
**Status:** Ready for Development  
**Version:** 1.0.0

---

## 🚀 Start Development (2 Options)

### Option 1: PowerShell Script (Recommended)

```powershell
# From project root
.\start-dev.ps1
```

This automatically starts:
- ✅ Docker Compose (PostgreSQL + Redis)
- ✅ Backend API server (port 8000)
- ✅ Frontend dev server (port 3000)

### Option 2: Manual (3 Terminal Windows)

**Terminal 1: Database**
```bash
docker-compose up -d
```

**Terminal 2: Backend**
```bash
cd backend
uvicorn app.main:app --reload
```

**Terminal 3: Frontend**
```bash
cd frontend
npm start
```

---

## 🌐 Access Points

After starting, services available at:

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | React app |
| Backend | http://localhost:8000 | API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| API ReDoc | http://localhost:8000/redoc | Alternative docs |
| PostgreSQL | localhost:5432 | Database |
| Redis | localhost:6379 | Cache |

---

## 📦 Dependencies Installed

### Backend (23 packages)
✅ fastapi, uvicorn, sqlalchemy, psycopg2, jwt, stripe, ccxt, web3, pytest, etc.

### Frontend (9 packages)
⏳ React, React Router, Axios, TailwindCSS, Zustand, etc. (installing now)

---

## 🧪 Run Tests

```bash
cd backend

# Run all tests
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_api.py::TestAuthEndpoints -v
```

---

## 📝 Environment Setup

### Create `backend/.env`

```env
DATABASE_URL=postgresql://user:password@localhost:5432/ai_marketplace
REDIS_URL=redis://localhost:6379
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DEBUG=true
ENVIRONMENT=development
```

### Create `frontend/.env.local`

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_TIMEOUT=30000
```

---

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend

# Reset database
docker-compose down -v
docker-compose up postgres redis

# Check status
docker-compose ps
```

---

## 🔍 Useful Commands

```bash
# Check Python packages
pip list | findstr fastapi

# Check Node packages
npm list --depth=0

# Frontend build
cd frontend && npm run build

# Backend migrations
alembic upgrade head
alembic downgrade -1

# Check what's listening on ports
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Kill process on port
taskkill /PID <PID> /F
```

---

## 📚 Key Files

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI app entry |
| `backend/app/models/` | Database models |
| `backend/app/api/` | Route handlers |
| `backend/app/security.py` | Security middleware |
| `frontend/src/App.js` | React entry |
| `frontend/src/pages/` | Page components |
| `docker-compose.yml` | Local services |
| `.env` | Environment config |

---

## 🔧 API Endpoints (Examples)

```bash
# Register
POST /auth/register
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

# Login
POST /auth/login
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

# Get current user
GET /users/me
Authorization: Bearer <token>

# Health check
GET /health

# API docs
GET /docs
GET /redoc
```

---

## 🆘 Troubleshooting

### Services won't start

```bash
# Check docker
docker ps

# Check ports in use
netstat -ano

# Kill and restart
docker-compose down
docker-compose up
```

### Python/npm issues

```bash
# Clear caches
pip cache purge
npm cache clean --force

# Reinstall
pip install -r requirements.txt
npm install --legacy-peer-deps
```

### Database issues

```bash
# Reset database
docker-compose down -v
docker-compose up postgres

# Apply migrations
alembic upgrade head
```

---

## 📖 Documentation

- **README_COMPLETE.md** - Full project overview
- **SETUP.md** - Detailed setup guide
- **DEPLOYMENT.md** - Production deployment
- **SECURITY.md** - Security hardening
- **TESTING.md** - Testing strategies
- **ARCHITECTURE.md** - System design
- **INDEX.md** - Documentation index

---

## ✅ Checklist for First Run

- [ ] Docker installed and running
- [ ] Backend .env created
- [ ] Frontend .env.local created
- [ ] `docker-compose up -d` successful
- [ ] Backend server running (check http://localhost:8000/health)
- [ ] Frontend server running (check http://localhost:3000)
- [ ] Can access API docs (http://localhost:8000/docs)
- [ ] Tests passing (`pytest -v`)
- [ ] Can register new user
- [ ] Can login with credentials

---

## 🚀 Common Tasks

### Add New API Endpoint

1. Create model in `backend/app/models/`
2. Create route in `backend/app/api/`
3. Add to `backend/app/main.py` router
4. Write tests
5. Restart backend

### Add New Frontend Page

1. Create component in `frontend/src/pages/`
2. Add route in `frontend/src/App.js`
3. Style with TailwindCSS
4. Test in browser

### Run Database Migrations

```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Deploy to Production

See `DEPLOYMENT.md` for:
- AWS setup
- GCP setup
- Azure setup
- CI/CD pipeline

---

## 📞 Need Help?

1. Check documentation files
2. Review test cases for usage examples
3. Check API docs at `/docs`
4. Check logs in terminal windows
5. Review `SECURITY.md` for security questions

---

## 🎉 You're All Set!

**All dependencies installed and ready to go.**

Start developing with:
```bash
.\start-dev.ps1
```

Then visit http://localhost:3000

Happy coding! 🚀

