"""
Simple configuration for multimodal price prediction transformer.
Updated to support both original and quantized models.
"""
import os

# Get the directory where this config file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data paths - now using relative paths
DATA_PATH = os.path.join(BASE_DIR, "Transformer_Ready_Input")
RESULTS_PATH = os.path.join(BASE_DIR, "simple_results")
MODEL_SAVE_PATH = os.path.join(BASE_DIR, "simple_models")

# Model configuration - SIMPLE & EFFECTIVE
MODEL_CONFIG = {
    'd_model': 128,
    'nhead': 4,
    'num_layers': 2,
    'dropout': 0.2,
    'max_price_log': 13.0,  # ~₹400k max
    'min_price_log': 2.0    # ~₹7 min
}

# Training configuration - BALANCED
TRAINING_CONFIG = {
    'batch_size': 32,
    'learning_rate': 3e-4,      # Good starting point
    'num_epochs': 30,
    'weight_decay': 1e-5,       # Light regularization
    'patience': 8,
    'min_lr': 1e-6
}

# 🆕 Quantization configuration
QUANTIZATION_CONFIG = {
    'enabled': True,
    'compare_models': True,
    'save_quantized_model': True,
    'quantized_model_path': os.path.join(MODEL_SAVE_PATH, 'quantized_model.pth'),
    'comparison_results_path': os.path.join(RESULTS_PATH, 'quantization_comparison.json')
}

# Model selection
MODEL_TYPES = {
    'original': 'transformer.MultimodalPriceTransformer',
    'quantized': 'quantized_model.QuantizedMultimodalPriceTransformer'
}

# Default model type
DEFAULT_MODEL_TYPE = 'original'  # Change to 'quantized' to use quantized model by default

print("✅ Simple configuration loaded")