# AI Marketplace Platform

An enterprise-grade AI-powered marketplace platform combining cryptocurrency trading, e-commerce, social networking, and construction project management. Built with FastAPI backend, React frontend, and PostgreSQL.

## Features

### 🏪 Marketplace
- Multi-currency stores and listings
- Image uploads and product management
- Order management and checkout flow
- Seller ratings and reviews (planned)

### 💰 Trading & Payments
- Cryptocurrency trading via CCXT (40+ exchanges)
- Fiat payments via Stripe
- Non-custodial wallets (planned)
- Binance-style peer-to-peer transfers
- Transaction history and AI activity logs

### 👥 Social & Collaboration
- Social posts with media uploads
- Real-time feed
- User profiles and KYC verification
- Messaging (planned)

### 🏗️ Construction (Planned)
- Project management
- 2D/3D drawings and blueprints
- Contractor bidding system
- Project timeline tracking

### 🎰 Betting & Gaming (Planned)
- Casino games
- Sports betting
- Live odds
- Secure transaction handling

### 🤖 AI Features
- Smart recommendations
- Trading signals
- Content generation for sellers
- Automated customer support
- Activity logging with "AI Eye"

## Tech Stack

**Backend**:
- FastAPI 0.100+
- PostgreSQL 15
- SQLAlchemy ORM
- JWT authentication
- CCXT for trading
- Stripe for payments

**Frontend**:
- React 18+
- React Router
- TailwindCSS
- Axios
- Lucide Icons

**Infrastructure**:
- Docker & Docker Compose
- Redis for caching
- Kubernetes ready
- AWS/GCP/Azure compatible

## Quick Start

### Prerequisites
- Docker Desktop
- Node.js 18+

### Local Setup

```bash
# Start backend services
docker compose up --build

# In another terminal, setup frontend
cd frontend
npm install
npm start
```

Backend: `http://localhost:8000`
Frontend: `http://localhost:3000`

See [SETUP.md](./SETUP.md) for detailed instructions.

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## File Structure

```
ai_project/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── api/
│   │   ├── services/
│   │   └── main.py
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── context/
│   │   └── App.js
│   └── package.json
├── docker-compose.yml
├── ARCHITECTURE.md
├── MVP.md
├── SETUP.md
└── DEPLOYMENT.md
```

## Core Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/auth/register` | POST | Register |
| `/auth/token` | POST | Login |
| `/users/me` | GET | Profile |
| `/users/me/kyc` | POST | KYC |
| `/marketplace/stores` | POST/GET | Stores |
| `/marketplace/stores/{id}/listings` | POST/GET | Listings |
| `/orders/` | POST | Orders |
| `/social/posts` | POST | Posts |
| `/social/feed` | GET | Feed |
| `/wallets/transfer` | POST | Transfer (Binance-style) |
| `/ai/logs` | GET | Activity logs |

## Next Steps

### Immediate (This Week)
1. Run `docker compose up --build` to start services
2. Navigate to `http://localhost:3000` to test frontend
3. Review `SETUP.md` for detailed API testing

### Short Term (Next 2 Weeks)
1. Implement non-custodial wallet key management
2. Complete Stripe checkout flow
3. Add construction project scaffold
4. Write unit tests

### Medium Term (Next 4 Weeks)
1. Implement betting/casino module
2. Add AI chat assistant
3. Enhance KYC workflow
4. Production hardening

### Long Term (Production)
1. Deploy to cloud (AWS/GCP/Azure)
2. Scale to handle millions of transactions
3. Regulatory compliance (crypto, betting)
4. Mobile apps (iOS, Android)
5. Advanced AI features

## Configuration

### Backend (.env)
```
DATABASE_URL=postgresql://postgres:postgres@db:5432/ai_project
SECRET_KEY=<strong-secret>
STRIPE_API_KEY=<key>
CCXT_API_KEY=<key>
```

### Frontend (.env.local)
```
REACT_APP_API_URL=http://localhost:8000
```

## Development

```bash
# Backend tests
cd backend && pytest tests/

# Frontend tests
cd frontend && npm test

# Code style
black backend/app
npm run lint --prefix frontend
```

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for:
- AWS/GCP/Azure setup
- CI/CD pipelines
- Monitoring & logging
- Security hardening

## Support

- Documentation: [SETUP.md](./SETUP.md), [DEPLOYMENT.md](./DEPLOYMENT.md)
- Issues: GitHub Issues
- Email: support@example.com

## License

MIT License
