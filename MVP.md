# MVP Definition

Core features for initial deployable product:

1. User accounts & KYC
   - Registration, login (JWT)
   - KYC submission with document upload

2. Marketplace
   - Stores and listings
   - Create/list products with media
   - Orders and basic checkout

3. Wallets & Payments
   - User wallets (records), deposit/withdraw flow placeholders
   - Fiat checkout via Stripe (skeleton)
   - Crypto payment flow (on-chain placeholder)

4. Trading Service
   - CCXT integration for market data and optional trade execution (demo keys)

5. Social
   - Posts with media and feed

6. Admin & Compliance
   - KYC review workflow (manual)
   - Logging and audit trails

Non-functional:
- Dockerized services
- Basic tests and docs
- Local storage for media (S3 in future)
