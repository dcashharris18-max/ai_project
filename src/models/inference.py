"""Model inference module"""

import torch


def run_inference(model, input_data, device="cpu"):
    """
    Run inference on input data.
    
    Args:
        model: Trained PyTorch model
        input_data: Input tensor or data
        device (str): Device to run inference on (cpu/cuda)
    
    Returns:
        torch.Tensor: Model predictions
    """
    model.eval()
    device = torch.device(device)
    model.to(device)
    
    with torch.no_grad():
        if isinstance(input_data, torch.Tensor):
            input_data = input_data.to(device)
        else:
            input_data = torch.tensor(input_data, dtype=torch.float32).to(device)
        
        predictions = model(input_data) if hasattr(model, "__call__") else input_data
    
    return predictions


if __name__ == "__main__":
    print("Inference module loaded successfully")
