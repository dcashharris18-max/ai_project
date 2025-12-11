"""Model management and utilities"""

import os
import torch
from pathlib import Path


class ModelManager:
    """Manage model loading, saving, and configuration"""
    
    def __init__(self, model_dir="Models"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
    
    def save_model(self, model, name, metadata=None):
        """Save model to disk"""
        model_path = self.model_dir / name / "model.pt"
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        checkpoint = {
            "model_state": model.state_dict() if hasattr(model, "state_dict") else model,
            "metadata": metadata or {}
        }
        
        torch.save(checkpoint, model_path)
        print(f"Model saved: {model_path}")
        return model_path
    
    def load_model(self, name):
        """Load model from disk"""
        model_path = self.model_dir / name / "model.pt"
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        checkpoint = torch.load(model_path, weights_only=False)
        print(f"Model loaded: {model_path}")
        return checkpoint
    
    def list_models(self):
        """List all available models"""
        models = [d.name for d in self.model_dir.iterdir() if d.is_dir()]
        return models


if __name__ == "__main__":
    manager = ModelManager()
    print("Available models:", manager.list_models())
