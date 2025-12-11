"""
Flask Web Application for AI Multi-Domain Trading System
Provides REST API endpoints to interact with the system
"""
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import logging
import numpy as np
from typing import Dict, Any

from main import AITradingSystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize AI Trading System
system = None

def get_system():
    """Get or create the AI Trading System instance"""
    global system
    if system is None:
        system = AITradingSystem()
        # Train with sample data on startup (using seed for consistency)
        np.random.seed(42)
        sample_data = np.random.randn(100, 3)
        sample_labels = np.random.randn(100, 1)
        system.train_ai_model(sample_data, sample_labels)
        logger.info("AI Trading System initialized and trained")
    return system


# HTML template for the home page
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Multi-Domain Trading System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        .endpoint {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #4CAF50;
        }
        .endpoint h3 {
            margin-top: 0;
            color: #4CAF50;
        }
        .method {
            display: inline-block;
            padding: 3px 8px;
            background: #2196F3;
            color: white;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
        }
        .post {
            background: #ff9800;
        }
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
        }
        .status {
            background: #e8f5e9;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .button {
            background: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        .button:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <h1>🤖 AI Multi-Domain Trading System</h1>
    <div class="status">
        <strong>Status:</strong> System is running and ready to accept requests
    </div>
    
    <h2>Available API Endpoints</h2>
    
    <div class="endpoint">
        <h3><span class="method">GET</span> /</h3>
        <p>This page - API documentation and system information</p>
    </div>
    
    <div class="endpoint">
        <h3><span class="method">GET</span> /status</h3>
        <p>Get overall system status including all modules</p>
        <p><strong>Example:</strong> <code>curl http://localhost:5000/status</code></p>
    </div>
    
    <div class="endpoint">
        <h3><span class="method">GET</span> /health</h3>
        <p>Health check endpoint</p>
        <p><strong>Example:</strong> <code>curl http://localhost:5000/health</code></p>
    </div>
    
    <div class="endpoint">
        <h3><span class="method">POST</span> /crypto/analyze</h3>
        <p>Analyze cryptocurrency market for a given trading pair</p>
        <p><strong>Body:</strong> <code>{"symbol": "BTC/USDT"}</code></p>
        <p><strong>Example:</strong> <code>curl -X POST http://localhost:5000/crypto/analyze -H "Content-Type: application/json" -d '{"symbol":"BTC/USDT"}'</code></p>
    </div>
    
    <div class="endpoint">
        <h3><span class="method">GET</span> /crypto/portfolio</h3>
        <p>Get cryptocurrency portfolio status</p>
        <p><strong>Example:</strong> <code>curl http://localhost:5000/crypto/portfolio</code></p>
    </div>
    
    <div class="endpoint">
        <h3><span class="method">POST</span> /trade/analyze</h3>
        <p>Analyze international trade opportunity</p>
        <p><strong>Body:</strong> <code>{"product": "Electronics", "from_region": "Asia", "to_region": "North America"}</code></p>
    </div>
    
    <div class="endpoint">
        <h3><span class="method">GET</span> /marketplace/metrics</h3>
        <p>Get marketplace performance metrics</p>
    </div>
    
    <div class="endpoint">
        <h3><span class="method">GET</span> /social/analytics</h3>
        <p>Get social media analytics summary</p>
    </div>
    
    <div class="endpoint">
        <h3><span class="method">POST</span> /social/trends</h3>
        <p>Monitor social media trends for a platform</p>
        <p><strong>Body:</strong> <code>{"platform": "twitter"}</code></p>
    </div>
    
    <div class="endpoint">
        <h3><span class="method">GET</span> /construction/projects</h3>
        <p>Get construction project summary</p>
    </div>
    
    <div class="endpoint">
        <h3><span class="method">GET</span> /marketing/summary</h3>
        <p>Get marketing campaigns summary</p>
    </div>
    
    <div class="endpoint">
        <h3><span class="method">POST</span> /run-cycle</h3>
        <p>Run one automated cycle across all modules</p>
        <p><strong>Example:</strong> <code>curl -X POST http://localhost:5000/run-cycle</code></p>
    </div>
    
    <h2>Quick Start</h2>
    <p>Try these commands to test the API:</p>
    <pre>
# Check system status
curl http://localhost:5000/status

# Analyze BTC market
curl -X POST http://localhost:5000/crypto/analyze \\
     -H "Content-Type: application/json" \\
     -d '{"symbol":"BTC/USDT"}'

# Run automated cycle
curl -X POST http://localhost:5000/run-cycle
    </pre>
    
    <div style="margin-top: 30px; padding: 15px; background: #fff3cd; border-radius: 5px;">
        <strong>Note:</strong> This is an educational and research system. Always conduct your own research before making financial decisions.
    </div>
</body>
</html>
"""


@app.route('/')
def home():
    """Home page with API documentation"""
    return render_template_string(HOME_TEMPLATE)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Multi-Domain Trading System'
    }), 200


@app.route('/status', methods=['GET'])
def get_status():
    """Get overall system status"""
    try:
        trading_system = get_system()
        status = trading_system.get_system_status()
        return jsonify({
            'success': True,
            'data': status
        }), 200
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/crypto/analyze', methods=['POST'])
def analyze_crypto():
    """Analyze cryptocurrency market"""
    try:
        trading_system = get_system()
        if not trading_system.crypto_trader:
            return jsonify({
                'success': False,
                'error': 'Cryptocurrency trading module not enabled'
            }), 400
        
        data = request.get_json()
        symbol = data.get('symbol', 'BTC/USDT')
        
        analysis = trading_system.crypto_trader.analyze_market(symbol)
        return jsonify({
            'success': True,
            'data': analysis
        }), 200
    except Exception as e:
        logger.error(f"Error analyzing crypto: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/crypto/portfolio', methods=['GET'])
def get_crypto_portfolio():
    """Get cryptocurrency portfolio status"""
    try:
        trading_system = get_system()
        if not trading_system.crypto_trader:
            return jsonify({
                'success': False,
                'error': 'Cryptocurrency trading module not enabled'
            }), 400
        
        portfolio = trading_system.crypto_trader.get_portfolio_status()
        return jsonify({
            'success': True,
            'data': portfolio
        }), 200
    except Exception as e:
        logger.error(f"Error getting portfolio: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/trade/analyze', methods=['POST'])
def analyze_trade():
    """Analyze international trade opportunity"""
    try:
        trading_system = get_system()
        if not trading_system.international_trader:
            return jsonify({
                'success': False,
                'error': 'International trade module not enabled'
            }), 400
        
        data = request.get_json()
        product = data.get('product', 'Electronics')
        from_region = data.get('from_region', 'Asia')
        to_region = data.get('to_region', 'North America')
        
        analysis = trading_system.international_trader.analyze_trade_opportunity(
            product, from_region, to_region
        )
        return jsonify({
            'success': True,
            'data': analysis
        }), 200
    except Exception as e:
        logger.error(f"Error analyzing trade: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/marketplace/metrics', methods=['GET'])
def get_marketplace_metrics():
    """Get marketplace performance metrics"""
    try:
        trading_system = get_system()
        if not trading_system.marketplace:
            return jsonify({
                'success': False,
                'error': 'Marketplace module not enabled'
            }), 400
        
        metrics = trading_system.marketplace.get_performance_metrics()
        return jsonify({
            'success': True,
            'data': metrics
        }), 200
    except Exception as e:
        logger.error(f"Error getting marketplace metrics: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/social/analytics', methods=['GET'])
def get_social_analytics():
    """Get social media analytics summary"""
    try:
        trading_system = get_system()
        if not trading_system.social_media:
            return jsonify({
                'success': False,
                'error': 'Social media module not enabled'
            }), 400
        
        analytics = trading_system.social_media.get_analytics_summary()
        return jsonify({
            'success': True,
            'data': analytics
        }), 200
    except Exception as e:
        logger.error(f"Error getting social analytics: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/social/trends', methods=['POST'])
def monitor_social_trends():
    """Monitor social media trends"""
    try:
        trading_system = get_system()
        if not trading_system.social_media:
            return jsonify({
                'success': False,
                'error': 'Social media module not enabled'
            }), 400
        
        data = request.get_json()
        platform = data.get('platform', 'twitter')
        
        trends = trading_system.social_media.monitor_trends(platform)
        return jsonify({
            'success': True,
            'data': trends
        }), 200
    except Exception as e:
        logger.error(f"Error monitoring trends: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/construction/projects', methods=['GET'])
def get_construction_projects():
    """Get construction project summary"""
    try:
        trading_system = get_system()
        if not trading_system.construction:
            return jsonify({
                'success': False,
                'error': 'Construction module not enabled'
            }), 400
        
        summary = trading_system.construction.get_project_summary()
        return jsonify({
            'success': True,
            'data': summary
        }), 200
    except Exception as e:
        logger.error(f"Error getting construction projects: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/marketing/summary', methods=['GET'])
def get_marketing_summary():
    """Get marketing campaigns summary"""
    try:
        trading_system = get_system()
        if not trading_system.marketing:
            return jsonify({
                'success': False,
                'error': 'Marketing module not enabled'
            }), 400
        
        summary = trading_system.marketing.get_marketing_summary()
        return jsonify({
            'success': True,
            'data': summary
        }), 200
    except Exception as e:
        logger.error(f"Error getting marketing summary: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/run-cycle', methods=['POST'])
def run_automated_cycle():
    """Run one automated cycle across all modules"""
    try:
        trading_system = get_system()
        trading_system.run_automated_cycle()
        return jsonify({
            'success': True,
            'message': 'Automated cycle completed successfully'
        }), 200
    except Exception as e:
        logger.error(f"Error running cycle: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    # For local development
    app.run(host='0.0.0.0', port=5000, debug=False)
