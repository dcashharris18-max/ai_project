# AI Marketplace Platform

Complete full-stack cryptocurrency and e-commerce marketplace with AI integration, trading capabilities, social features, construction projects, and betting/casino. Production-ready with security hardening, comprehensive testing, and automated CI/CD.

## 🚀 Features

### Core Platform
- **Authentication** - JWT-based auth with bcrypt password hashing
- **User Management** - Profile, KYC verification with document upload
- **Wallets** - Both custodial and non-custodial (HD wallet, BIP44)
- **Marketplace** - Store creation, product listings, image uploads
- **Social** - User posts, social feed, media sharing
- **Orders** - E-commerce order management, Stripe integration
- **Trading** - CCXT integration with 40+ crypto exchanges
- **Activity Logging** - "AI Eye" transaction tracking

### Advanced Features
- **Construction Projects** - Project management, drawing uploads, contractor bidding
- **Betting & Casino** - Games with provably fair verification, responsible gambling controls
- **Security** - CORS, rate limiting, input validation, HTTPS, security headers
- **Testing** - Comprehensive unit/integration tests with >80% coverage
- **CI/CD** - GitHub Actions pipeline with automated testing, building, security scanning

## Project Structure

```
ai_project/
├── backend/
│   ├── app/
│   │   ├── main.py (FastAPI app)
│   │   ├── security.py (hardening)
│   │   ├── auth_utils.py
│   │   ├── crud.py
│   │   ├── schemas.py
│   │   ├── api/ (routes)
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── marketplace.py
│   │   │   ├── social.py
│   │   │   ├── orders.py
│   │   │   ├── wallets.py
│   │   │   ├── ai.py
│   │   │   ├── construction.py (NEW)
│   │   │   └── betting.py (NEW)
│   │   ├── models/ (database)
│   │   │   ├── user.py
│   │   │   ├── wallet.py
│   │   │   ├── store.py
│   │   │   ├── listing.py
│   │   │   ├── post.py
│   │   │   ├── order.py
│   │   │   ├── transaction.py
│   │   │   ├── construction.py (NEW)
│   │   │   └── betting.py (NEW)
│   │   ├── services/
│   │   │   ├── trading.py (CCXT)
│   │   │   ├── payments.py (Stripe)
│   │   │   └── wallet_manager.py (HD wallet) (NEW)
│   │   └── db/
│   │       └── session.py
│   ├── tests/ (NEW)
│   │   ├── test_api.py
│   │   └── conftest.py
│   ├── storage/ (media, KYC docs, construction drawings)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── context/AuthContext.js
│   │   └── pages/
│   │       ├── Login.js
│   │       ├── Register.js
│   │       └── Dashboard.js
│   ├── public/index.html
│   └── package.json
├── .github/
│   └── workflows/ (NEW)
│       └── ci-cd.yml
├── docker-compose.yml
├── .gitignore
├── IMPLEMENTATION_COMPLETE.md (NEW)
├── ARCHITECTURE.md
├── MVP.md
├── SETUP.md
├── DEPLOYMENT.md
├── SECURITY.md (NEW)
├── TESTING.md (NEW)
└── README.md (this file)
```

## Quick Start

**CI**

This repository includes a GitHub Actions workflow that runs linting and backend tests on push and pull requests. After you add a remote, the CI badge will display build status.

CI badge (replace <user> and <repo> with your values):

![CI](https://github.com/<user>/<repo>/actions/workflows/ci.yml/badge.svg)


1. **Create virtual environment:**
   ```bash
   python -m venv ai.env
   ai.env\Scripts\activate  # On Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

## Usage

### Run Complete Pipeline
```bash
python main.py
```

### Run Individual Steps

**Fetch Data:**
```python
from src.data import fetch_crypto_data, fetch_blockchain_data
fetch_crypto_data(symbol="BTC/USDT", limit=500)
fetch_blockchain_data(network="ethereum", limit=100)
```

**Clean Data:**
```python
from src.data import clean_data
clean_data()
```

**Tokenize Data:**
```python
from src.data import tokenize_data
tokenize_data()
```

**Manage Models:**
```python
from src.models import ModelManager
manager = ModelManager()
manager.list_models()
```

## Data Flow

1. **Fetch** → Raw data from multiple sources
2. **Clean** → Remove nulls, duplicates, standardize
3. **Tokenize** → Convert to tensor format for ML
4. **Train** → Use tokenized data for model training
5. **Inference** → Make predictions with trained models

## Supported Data Sources

- **Blockchain**: Ethereum, Bitcoin, and other networks
- **Cryptocurrency**: Real-time OHLCV data via CCXT (Binance, Coinbase, etc.)
- **Social Media**: Reddit, Twitter, and other platforms
- **E-commerce**: Product data from various retailers

## Features

✅ Modular data pipeline architecture  
✅ Multiple data source integration  
✅ Automatic data cleaning and preprocessing  
✅ PyTorch tensor tokenization  
✅ Model management utilities  
✅ Configuration management  
✅ Error handling and logging  

## Dependencies

- **ccxt** - Cryptocurrency exchange data
- **torch** - Deep learning framework
- **numpy** - Numerical computing
- **pandas** - Data manipulation
- **scikit-learn** - ML utilities
- **jupyter** - Interactive notebooks

## Configuration

Edit `config.py` to customize:
- Data source settings
- Model parameters
- Processing options
- Directory paths

## Logs

Logs are saved to `logs/project.log` for debugging and monitoring.

## License

MIT License

## Support

For issues or questions, check the documentation or submit an issue.

## Developer Notes

- To run linters/formatters locally:

```bash
pip install -r backend/requirements_dev.txt
black .
isort .
flake8 .
```

 - To run backend tests locally:

```bash
python -m pytest backend/tests -q
```
