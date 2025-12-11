# AI Marketplace - Setup & Deployment Guide

## Quick Start (Local Development)

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+

### Backend Setup

1. **Clone & enter project**
```bash
cd c:\Users\DEll\Desktop\ai_project
```

2. **Start backend services**
```bash
docker compose up --build
```
This starts:
- FastAPI backend on `http://localhost:8000`
- PostgreSQL on `localhost:5432`
- Redis on `localhost:6379`

3. **Verify backend is running**
```bash
curl http://localhost:8000/
# Expected: {"status": "ok", "message": "AI Marketplace API"}
```

### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Configure API endpoint**
Create `.env.local` in `frontend/`:
```
REACT_APP_API_URL=http://localhost:8000
```

3. **Start frontend dev server**
```bash
npm start
```
Frontend opens at `http://localhost:3000`

### First Steps

1. **Register**: Navigate to `/register` and create an account
2. **Login**: Use credentials to sign in (redirects to dashboard)
3. **Dashboard Features**:
   - View balance (toggle visibility)
   - Manage wallets
   - Send funds to other users by ID
   - View AI activity logs (Eye icon shows all transactions)

## API Endpoints Overview

### Auth
- `POST /auth/register` - Register user
- `POST /auth/token` - Obtain JWT token (use email as username)

### Users
- `GET /users/me` - Get current user profile
- `POST /users/me/kyc` - Submit KYC info + document (multipart form)
- `GET /users/me/wallets` - List user wallets
- `POST /users/me/wallets` - Add wallet

### Marketplace
- `POST /marketplace/stores` - Create store
- `GET /marketplace/stores` - List your stores
- `POST /marketplace/stores/{store_id}/listings` - Create listing with image
- `GET /marketplace/stores/{store_id}/listings` - List store listings

### Social
- `POST /social/posts` - Create post with optional media
- `GET /social/feed` - View feed (latest 50 posts)

### Wallets & Transfers
- `POST /wallets/transfer` - Send funds to user by ID (Binance-style)
- `GET /ai/logs` - Get activity logs for current user

### Orders
- `POST /orders/` - Create order from store listings
  - Backend auto-creates payment intent (Stripe/Crypto placeholder)

## Configuration

### Backend (.env)
Located at `backend/.env`:
```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/ai_project
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALGORITHM=HS256

# Optional: Stripe
STRIPE_API_KEY=sk_test_...

# Optional: CCXT Trading
CCXT_EXCHANGE=binance
CCXT_API_KEY=...
CCXT_SECRET=...
```

### Frontend (.env.local)
```
REACT_APP_API_URL=http://localhost:8000
```

## Docker Compose Services

| Service | URL | Purpose |
|---------|-----|---------|
| backend | http://localhost:8000 | FastAPI server |
| db | localhost:5432 | PostgreSQL database |
| redis | localhost:6379 | Cache & message broker |

## Deployment (Production)

### Docker Build
```bash
docker build -t ai-marketplace-backend ./backend
```

### Kubernetes Example (helm values)
```yaml
backend:
  image: ai-marketplace-backend:latest
  replicas: 3
  env:
    DATABASE_URL: postgresql://user:pass@postgres-service:5432/ai_project
    SECRET_KEY: <strong-secret>
    
postgres:
  persistence:
    size: 100Gi
```

### Environment Variables for Production
- Set strong `SECRET_KEY` (use: `openssl rand -hex 32`)
- Use managed database (AWS RDS, Azure Database)
- Configure S3 for media storage (update `crud.py` file upload paths)
- Set `STRIPE_API_KEY` if using Stripe
- Configure CORS for frontend domain
- Use HTTPS everywhere

## Database Migrations

Currently using SQLAlchemy `create_all()` on startup. For production, use Alembic:

```bash
# Generate migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head
```

## Testing the API

### Using curl (get token first)
```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Login
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=test123"

# Use token (replace TOKEN)
curl -X GET http://localhost:8000/users/me \
  -H "Authorization: Bearer TOKEN"
```

### Using Postman
1. Register user
2. Login and copy access_token
3. Set auth header: `Authorization: Bearer <token>`
4. Test endpoints

## Troubleshooting

**Backend won't start**
- Check port 8000 is free: `lsof -i :8000`
- Verify Docker daemon is running
- Check logs: `docker logs <container_id>`

**Frontend can't connect to backend**
- Verify `REACT_APP_API_URL` in `.env.local`
- Check backend is running: `curl http://localhost:8000/`
- Check CORS headers in backend logs

**Database connection errors**
- Verify postgres container is running: `docker ps`
- Check credentials in `backend/.env`
- Ensure wait-for-db logic (consider using health checks)

## Next Steps

1. **Implement wallet blockchain integration**
   - Add HD wallet generation
   - Integrate with RPC providers (Infura, Alchemy)
   - Implement transaction signing

2. **Complete Stripe integration**
   - Return client secret in order endpoint
   - Add webhook handler for payment confirmations
   - Implement refund flow

3. **Add construction & betting modules**
   - Define domain models
   - Create API routes
   - Integrate with compliance/KYC

4. **Production hardening**
   - Add unit and integration tests
   - Implement rate limiting
   - Add comprehensive logging
   - Security audit (OWASP top 10)
   - Performance tuning (caching, indexing)

5. **Advanced AI features**
   - Chat interface (integrate LLM)
   - Automated recommendations
   - Trading signals
   - Content generation for marketplace

## Support & Resources

- Backend docs: Swagger UI at `http://localhost:8000/docs`
- Architecture: See `ARCHITECTURE.md`
- MVP features: See `MVP.md`
