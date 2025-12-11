# AI Multi-Domain Trading System

An advanced AI-powered system that integrates multiple business domains including cryptocurrency trading, international trade, marketplace management, social media, construction project management, and comprehensive marketing functions.

## Features

### 🤖 Core AI Model
- Machine learning-based decision making
- Predictive analytics across all domains
- Continuous learning and optimization
- Model persistence and loading capabilities

### 💰 Cryptocurrency Trading
- Multi-exchange support (Binance, Coinbase, etc.)
- AI-powered market analysis
- Automated trading signals
- Risk management and portfolio tracking
- Real-time price analysis

### 🌍 International Trade
- Global trade opportunity analysis
- Compliance checking
- Tariff and duty calculations
- Shipment tracking
- Multi-region support (North America, Europe, Asia)

### 🛒 Marketplace Management
- Multi-platform integration (Amazon, eBay, Etsy)
- AI-powered pricing optimization
- Inventory tracking
- Competition analysis
- Product recommendations

### 📱 Social Media Management
- Multi-platform support (Twitter, Facebook, Instagram, LinkedIn)
- AI-generated content
- Optimal posting time recommendations
- Engagement tracking and analytics
- Influencer identification
- Trend monitoring

### 🏗️ Construction Project Management
- Project planning and tracking
- AI-powered cost estimation
- Resource planning
- Risk identification
- Schedule optimization
- Progress monitoring

### 📈 Full Marketing Function
- Multi-channel campaign management
- AI-powered audience segmentation
- Content optimization
- A/B testing
- Lead generation and scoring
- SEO performance analysis
- Customer lifetime value prediction
- ROI tracking

## Installation

1. Clone the repository:
```bash
git clone https://github.com/dcashharris18-max/ai_project.git
cd ai_project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the system:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

4. Edit `config.yaml` to customize module settings

## Usage

### Web Application (Hosted)

Run the web application:
```bash
python app.py
```

The web interface will be available at `http://localhost:5000`

You can also use the REST API endpoints:
```bash
# Check system status
curl http://localhost:5000/status

# Analyze cryptocurrency market
curl -X POST http://localhost:5000/crypto/analyze \
     -H "Content-Type: application/json" \
     -d '{"symbol":"BTC/USDT"}'

# Run automated cycle
curl -X POST http://localhost:5000/run-cycle
```

### Command Line Interface

Run the system directly:
```bash
python main.py
```

### Using Individual Modules

```python
from ai_model import AIModel
from crypto_trading import CryptoTrader
import numpy as np

# Initialize AI model
config = {'learning_rate': 0.001, 'epochs': 100}
ai_model = AIModel(config)

# Train the model
training_data = np.random.randn(100, 3)
labels = np.random.randn(100, 1)
ai_model.train(training_data, labels)

# Use crypto trading module
crypto_config = {
    'max_position_size': 1000,
    'stop_loss_percentage': 5.0,
    'risk_level': 'medium'
}
trader = CryptoTrader(crypto_config, ai_model)

# Analyze market
analysis = trader.analyze_market('BTC/USDT')
print(f"AI Signal: {analysis['ai_signal']}")
print(f"Confidence: {analysis['confidence']}")
```

### Advanced Configuration

Customize `config.yaml` to enable/disable modules and adjust settings:

```yaml
crypto_trading:
  enabled: true
  exchanges:
    - binance
    - coinbase
  trading_pairs:
    - BTC/USDT
    - ETH/USDT

marketing:
  enabled: true
  channels:
    - email
    - social
    - seo
```

## System Architecture

```
AI Trading System
├── Core AI Model (ai_model.py)
│   ├── Data preprocessing
│   ├── Model training
│   ├── Predictions
│   └── Model persistence
├── Cryptocurrency Trading (crypto_trading.py)
├── International Trade (international_trade.py)
├── Marketplace (marketplace.py)
├── Social Media (social_media.py)
├── Construction (construction.py)
├── Marketing (marketing.py)
└── Main Orchestration (main.py)
```

## Configuration

All modules can be configured via `config.yaml`. Key configuration options:

- **AI Model**: Learning rate, epochs, batch size, validation split
- **Crypto Trading**: Exchanges, trading pairs, risk level, position limits
- **International Trade**: Regions, trade types, compliance settings
- **Marketplace**: Platforms, categories, pricing strategy
- **Social Media**: Platforms, posting frequency, engagement tracking
- **Construction**: Project types, cost estimation, resource planning
- **Marketing**: Channels, campaign optimization, analytics

## API Keys Required

To use all features, you'll need API keys for:
- Cryptocurrency exchanges (Binance, Coinbase)
- Social media platforms (Twitter, Facebook, Instagram, LinkedIn)
- Marketing services (Google Analytics, SendGrid)

Add these to your `.env` file (see `.env.example` for template).

## Deployment

### Deploy to Render / Railway / Heroku

This project includes deployment configuration files for easy hosting on cloud platforms:

1. **Render.com** (Recommended - Free tier available)
   - Connect your GitHub repository
   - Render will automatically detect the `Procfile`
   - Set environment variables in the Render dashboard
   - Deploy!

2. **Railway.app**
   - Connect your GitHub repository
   - Railway will automatically detect and deploy
   - Configure environment variables if needed

3. **Heroku**
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku config:set LOG_LEVEL=INFO
   ```

### Deploy with Docker

Build and run using Docker:
```bash
# Build the image
docker build -t ai-trading-system .

# Run the container
docker run -p 5000:5000 ai-trading-system
```

Or use Docker Compose:
```bash
docker-compose up
```

### Environment Variables for Production

Set these environment variables on your hosting platform:
- `PORT` - Port number (automatically set by most platforms)
- `LOG_LEVEL` - Logging level (INFO, DEBUG, etc.)
- API keys from `.env.example` as needed

## Requirements

- Python 3.8+
- TensorFlow 2.13+
- See `requirements.txt` for full list

## Example Output

```
AI Multi-Domain Trading System
============================================================

[1] Training AI Model...
Training completed: {'accuracy': 0.85, 'loss': 0.15}

[2] Running Automated Cycle...
Crypto analysis for BTC/USDT: BUY
Trade opportunity: PROCEED
Marketplace metrics: {'total_listings': 5, 'active_listings': 5}

[3] System Status:
AI Model Trained: True
Active Modules: 6
```

## API Endpoints

When running the web application (`python app.py`), the following REST API endpoints are available:

### General
- `GET /` - Web interface with API documentation
- `GET /health` - Health check endpoint
- `GET /status` - Get overall system status

### Cryptocurrency Trading
- `POST /crypto/analyze` - Analyze market for a trading pair
  ```json
  {"symbol": "BTC/USDT"}
  ```
- `GET /crypto/portfolio` - Get portfolio status

### International Trade
- `POST /trade/analyze` - Analyze trade opportunity
  ```json
  {"product": "Electronics", "from_region": "Asia", "to_region": "North America"}
  ```

### Marketplace
- `GET /marketplace/metrics` - Get performance metrics

### Social Media
- `GET /social/analytics` - Get analytics summary
- `POST /social/trends` - Monitor trends for a platform
  ```json
  {"platform": "twitter"}
  ```

### Construction
- `GET /construction/projects` - Get project summary

### Marketing
- `GET /marketing/summary` - Get campaigns summary

### Automation
- `POST /run-cycle` - Run automated cycle across all modules

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

See LICENSE file for details.

## Disclaimer

This system is for educational and research purposes. Always conduct your own research and consult with professionals before making financial, trading, or business decisions.
