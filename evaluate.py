"""
Simple evaluation for price prediction model.
"""
import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os

def evaluate_model(model, dataloader, transform_info, device):
    """Evaluate model and return metrics."""
    
    print("🧪 Evaluating model...")
    
    model.eval()
    all_predictions = []
    all_targets = []
    
    # Collect predictions
    with torch.no_grad():
        for token_sequences, targets in dataloader:
            token_sequences = token_sequences.to(device)
            predictions = model(token_sequences)
            
            all_predictions.extend(predictions.cpu().numpy())
            all_targets.extend(targets.numpy())
    
    predictions = np.array(all_predictions)
    targets = np.array(all_targets)
    
    print(f"Collected {len(predictions)} predictions")
    print(f"Log space - Predictions: {predictions.min():.3f} to {predictions.max():.3f}")
    print(f"Log space - Targets: {targets.min():.3f} to {targets.max():.3f}")
    
    # Convert back to original price scale (inverse log transform)
    try:
        # Our targets are in log1p space, so use expm1 to get original prices
        pred_original = np.expm1(np.clip(predictions, 0, 15))
        target_original = np.expm1(np.clip(targets, 0, 15))
        
        print(f"Original prices - Predictions: ₹{pred_original.min():.2f} to ₹{pred_original.max():.2f}")
        print(f"Original prices - Targets: ₹{target_original.min():.2f} to ₹{target_original.max():.2f}")
        
    except Exception as e:
        print(f"❌ Error in inverse transform: {e}")
        pred_original = predictions
        target_original = targets
    
    # Calculate metrics on original scale
    try:
        rmse = np.sqrt(mean_squared_error(target_original, pred_original))
        mae = mean_absolute_error(target_original, pred_original)
        r2 = r2_score(target_original, pred_original)
        
        # MAPE with protection against division by zero
        mape = np.mean(np.abs((target_original - pred_original) / np.maximum(target_original, 1))) * 100
        
        metrics = {
            'rmse': rmse,
            'mae': mae,
            'r2': r2,
            'mape': mape,
            'num_samples': len(predictions)
        }
        
        # Create simple visualization
        create_simple_plot(target_original, pred_original, metrics)
        
        return metrics
        
    except Exception as e:
        print(f"❌ Error calculating metrics: {e}")
        return None

def create_simple_plot(targets, predictions, metrics):
    """Create a simple scatter plot of predictions vs targets."""
    
    try:
        plt.figure(figsize=(10, 8))
        
        # Scatter plot
        plt.scatter(targets, predictions, alpha=0.6, s=20)
        
        # Perfect prediction line
        min_val = min(targets.min(), predictions.min())
        max_val = max(targets.max(), predictions.max())
        plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')
        
        plt.xlabel('Actual Price (₹)')
        plt.ylabel('Predicted Price (₹)')
        plt.title(f'Price Prediction Results\nR² = {metrics["r2"]:.4f}, RMSE = ₹{metrics["rmse"]:.2f}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Save plot
        from config import RESULTS_PATH
        save_path = os.path.join(RESULTS_PATH, 'prediction_results.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Saved plot to {save_path}")
        
    except Exception as e:
        print(f"❌ Error creating plot: {e}")

def load_and_evaluate(model_path=None):
    """Load model and evaluate."""
    
    from config import MODEL_SAVE_PATH, DATA_PATH, MODEL_CONFIG
    from transformer import MultimodalPriceTransformer
    from dataloader import load_data
    
    # Setup
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Load data
    _, _, test_loader, transform_info = load_data(DATA_PATH, batch_size=64)
    
    # Load model
    if model_path is None:
        model_path = os.path.join(MODEL_SAVE_PATH, 'best_model.pth')
    
    model = MultimodalPriceTransformer(**MODEL_CONFIG)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    
    print(f"Loaded model from {model_path}")
    
    # Evaluate
    results = evaluate_model(model, test_loader, transform_info, device)
    
    if results:
        print(f"\n📊 Evaluation Results:")
        print(f"RMSE: ₹{results['rmse']:.2f}")
        print(f"MAE:  ₹{results['mae']:.2f}")
        print(f"R²:   {results['r2']:.4f}")
        print(f"MAPE: {results['mape']:.2f}%")
    
    return results

if __name__ == "__main__":
    load_and_evaluate()