# Architecture Overview

High-level architecture for the AI Marketplace platform.

- Frontend: React SPA (i18n, multi-currency), connects to backend APIs.
- Backend: FastAPI microservice (this repo's `backend/app`) handling auth, marketplace, social, trading, payments, KYC, wallets.
- Database: PostgreSQL for transactional data (users, stores, listings, orders, wallets).
- Cache/Workers: Redis for background jobs and websockets/notifications.
- Storage: Object storage (S3) for media & KYC documents (local storage used for dev).
- Blockchain integrations: CCXT for exchange trading; RPC providers and key management for non-custodial wallets.
- Payments: Stripe (fiat) + on-chain crypto payments (monitoring, confirmations).
- AI Assistant: LLM orchestration service (separate microservice) for recommendations, automation, content generation.

Deployment: Docker + Docker Compose for local; Kubernetes for production with CI/CD pipelines.
