"""
AI Multi-Domain Trading System
Main orchestration module
"""
import yaml
import logging
from typing import Dict, Any, Optional
import numpy as np

from ai_model import AIModel
from crypto_trading import CryptoTrader
from international_trade import InternationalTrader
from marketplace import Marketplace
from social_media import SocialMediaManager
from construction import ConstructionManager
from marketing import MarketingManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AITradingSystem:
    """
    Main AI Trading System that orchestrates all modules
    """
    
    def __init__(self, config_path: str = 'config.yaml'):
        """
        Initialize the AI Trading System
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.ai_model = AIModel(self.config.get('ai_model', {}))
        
        # Initialize modules
        self.crypto_trader = None
        self.international_trader = None
        self.marketplace = None
        self.social_media = None
        self.construction = None
        self.marketing = None
        
        self._initialize_modules()
        logger.info("AI Trading System initialized")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from YAML file
        
        Args:
            config_path: Path to config file
            
        Returns:
            Configuration dictionary
        """
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return {}
    
    def _initialize_modules(self):
        """Initialize all enabled modules"""
        
        if self.config.get('crypto_trading', {}).get('enabled', True):
            self.crypto_trader = CryptoTrader(
                self.config.get('crypto_trading', {}),
                self.ai_model
            )
            logger.info("Cryptocurrency trading module enabled")
        
        if self.config.get('international_trade', {}).get('enabled', True):
            self.international_trader = InternationalTrader(
                self.config.get('international_trade', {}),
                self.ai_model
            )
            logger.info("International trade module enabled")
        
        if self.config.get('marketplace', {}).get('enabled', True):
            self.marketplace = Marketplace(
                self.config.get('marketplace', {}),
                self.ai_model
            )
            logger.info("Marketplace module enabled")
        
        if self.config.get('social_media', {}).get('enabled', True):
            self.social_media = SocialMediaManager(
                self.config.get('social_media', {}),
                self.ai_model
            )
            logger.info("Social media module enabled")
        
        if self.config.get('construction', {}).get('enabled', True):
            self.construction = ConstructionManager(
                self.config.get('construction', {}),
                self.ai_model
            )
            logger.info("Construction module enabled")
        
        if self.config.get('marketing', {}).get('enabled', True):
            self.marketing = MarketingManager(
                self.config.get('marketing', {}),
                self.ai_model
            )
            logger.info("Marketing module enabled")
    
    def train_ai_model(self, training_data: np.ndarray, labels: np.ndarray) -> Dict[str, Any]:
        """
        Train the core AI model
        
        Args:
            training_data: Training dataset
            labels: Training labels
            
        Returns:
            Training metrics
        """
        logger.info("Training AI model across all domains...")
        return self.ai_model.train(training_data, labels)
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get overall system status
        
        Returns:
            System status information
        """
        status = {
            'ai_model_trained': self.ai_model.is_trained,
            'modules': {}
        }
        
        if self.crypto_trader:
            status['modules']['crypto_trading'] = self.crypto_trader.get_portfolio_status()
        
        if self.international_trader:
            status['modules']['international_trade'] = self.international_trader.get_trade_statistics()
        
        if self.marketplace:
            status['modules']['marketplace'] = self.marketplace.get_performance_metrics()
        
        if self.social_media:
            status['modules']['social_media'] = self.social_media.get_analytics_summary()
        
        if self.construction:
            status['modules']['construction'] = self.construction.get_project_summary()
        
        if self.marketing:
            status['modules']['marketing'] = self.marketing.get_marketing_summary()
        
        return status
    
    def run_automated_cycle(self):
        """
        Run one automated cycle across all modules
        """
        logger.info("Running automated cycle...")
        
        # Crypto trading
        if self.crypto_trader:
            for symbol in self.config.get('crypto_trading', {}).get('trading_pairs', ['BTC/USDT']):
                analysis = self.crypto_trader.analyze_market(symbol)
                logger.info(f"Crypto analysis for {symbol}: {analysis.get('ai_signal')}")
        
        # International trade
        if self.international_trader:
            analysis = self.international_trader.analyze_trade_opportunity(
                'Electronics', 'Asia', 'North America'
            )
            logger.info(f"Trade opportunity: {analysis.get('recommendation')}")
        
        # Marketplace
        if self.marketplace:
            metrics = self.marketplace.get_performance_metrics()
            logger.info(f"Marketplace metrics: {metrics}")
        
        # Social media
        if self.social_media:
            trends = self.social_media.monitor_trends('twitter')
            logger.info(f"Social media trends: {len(trends)} topics monitored")
        
        # Construction
        if self.construction:
            summary = self.construction.get_project_summary()
            logger.info(f"Construction projects: {summary.get('total_projects')}")
        
        # Marketing
        if self.marketing:
            summary = self.marketing.get_marketing_summary()
            logger.info(f"Marketing campaigns: {summary.get('active_campaigns')}")
        
        logger.info("Automated cycle completed")


def main():
    """Main entry point"""
    print("=" * 60)
    print("AI Multi-Domain Trading System")
    print("=" * 60)
    
    # Initialize system
    system = AITradingSystem()
    
    # Train AI model with sample data
    print("\n[1] Training AI Model...")
    sample_data = np.random.randn(100, 3)
    sample_labels = np.random.randn(100, 1)
    metrics = system.train_ai_model(sample_data, sample_labels)
    print(f"Training completed: {metrics}")
    
    # Run automated cycle
    print("\n[2] Running Automated Cycle...")
    system.run_automated_cycle()
    
    # Get system status
    print("\n[3] System Status:")
    status = system.get_system_status()
    print(f"AI Model Trained: {status['ai_model_trained']}")
    print(f"Active Modules: {len(status['modules'])}")
    
    for module_name, module_status in status['modules'].items():
        print(f"\n{module_name.upper()}:")
        for key, value in module_status.items():
            print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("System initialized and ready for operation")
    print("=" * 60)


if __name__ == '__main__':
    main()
