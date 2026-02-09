"""
Simple and effective training script for multimodal price prediction.
"""
import os
import time
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import ReduceLROnPlateau
import numpy as np
from tqdm import tqdm

from config import *
from transformer import MultimodalPriceTransformer, SimplePricePredictor
from dataloader import load_data
from evaluate import evaluate_model

class EarlyStopping:
    """Simple early stopping."""
    
    def __init__(self, patience=8, min_delta=1e-4):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = float('inf')
        self.early_stop = False
        self.best_state = None
    
    def __call__(self, val_loss, model):
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
            self.best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            print(f"✅ New best validation loss: {val_loss:.6f}")
        else:
            self.counter += 1
            print(f"⏳ No improvement: {self.counter}/{self.patience}")
            
        if self.counter >= self.patience:
            self.early_stop = True
            if self.best_state:
                model.load_state_dict({k: v.to(next(model.parameters()).device) 
                                     for k, v in self.best_state.items()})
                print("🔄 Restored best model weights")

def train_epoch(model, dataloader, criterion, optimizer, device):
    """Train for one epoch."""
    model.train()
    total_loss = 0.0
    num_batches = 0
    
    for token_sequences, targets in tqdm(dataloader, desc="Training"):
        # Move to device
        token_sequences = token_sequences.to(device)
        targets = targets.to(device)
        
        # Forward pass
        optimizer.zero_grad()
        predictions = model(token_sequences)
        loss = criterion(predictions, targets)
        
        # Backward pass
        loss.backward()
        
        # Gradient clipping for stability
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        optimizer.step()
        
        total_loss += loss.item()
        num_batches += 1
    
    return total_loss / num_batches

def validate(model, dataloader, criterion, device):
    """Validate model."""
    model.eval()
    total_loss = 0.0
    num_batches = 0
    
    with torch.no_grad():
        for token_sequences, targets in dataloader:
            token_sequences = token_sequences.to(device)
            targets = targets.to(device)
            
            predictions = model(token_sequences)
            loss = criterion(predictions, targets)
            
            total_loss += loss.item()
            num_batches += 1
    
    return total_loss / num_batches

def main():
    """Main training function."""
    print("🚀 Starting simple multimodal price prediction training")
    print("=" * 60)
    
    # Setup
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    
    # Create directories
    os.makedirs(RESULTS_PATH, exist_ok=True)
    os.makedirs(MODEL_SAVE_PATH, exist_ok=True)
    
    # Load data
    try:
        train_loader, val_loader, test_loader, transform_info = load_data(
            DATA_PATH, TRAINING_CONFIG['batch_size']
        )
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    # Create model
    try:
        model = MultimodalPriceTransformer(**MODEL_CONFIG)
        model = model.to(device)
        
        total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        print(f"Model parameters: {total_params:,}")
        
    except Exception as e:
        print(f"❌ Error creating model: {e}")
        print("🔄 Using simple fallback model...")
        model = SimplePricePredictor().to(device)
    
    # Training setup
    criterion = nn.MSELoss()  # Simple MSE loss
    optimizer = optim.AdamW(
        model.parameters(),
        lr=TRAINING_CONFIG['learning_rate'],
        weight_decay=TRAINING_CONFIG['weight_decay']
    )
    
    # 🔧 FIXED: Removed verbose parameter for PyTorch compatibility
    scheduler = ReduceLROnPlateau(optimizer, mode='min', patience=3, factor=0.7)
    
    # Custom verbose printing for scheduler
    class VerboseScheduler:
        def __init__(self, scheduler):
            self.scheduler = scheduler
            self.last_lr = None
        
        def step(self, val_loss):
            old_lr = self.scheduler.optimizer.param_groups[0]['lr']
            self.scheduler.step(val_loss)
            new_lr = self.scheduler.optimizer.param_groups[0]['lr']
            
            if new_lr != old_lr:
                print(f"📉 Learning rate reduced: {old_lr:.2e} → {new_lr:.2e}")
    
    verbose_scheduler = VerboseScheduler(scheduler)
    early_stopping = EarlyStopping(patience=TRAINING_CONFIG['patience'])
    
    # Training loop
    history = {'train_loss': [], 'val_loss': [], 'lr': []}
    best_val_loss = float('inf')
    
    print(f"\n🏁 Training for {TRAINING_CONFIG['num_epochs']} epochs...")
    
    for epoch in range(TRAINING_CONFIG['num_epochs']):
        start_time = time.time()
        
        # Train
        train_loss = train_epoch(model, train_loader, criterion, optimizer, device)
        
        # Validate
        val_loss = validate(model, val_loader, criterion, device)
        
        # Update scheduler (with verbose output)
        verbose_scheduler.step(val_loss)
        current_lr = optimizer.param_groups[0]['lr']
        
        # Record history
        history['train_loss'].append(train_loss)
        history['val_loss'].append(val_loss)
        history['lr'].append(current_lr)
        
        # Print progress
        epoch_time = time.time() - start_time
        print(f"\nEpoch {epoch+1}/{TRAINING_CONFIG['num_epochs']}")
        print(f"Train Loss: {train_loss:.6f}")
        print(f"Val Loss:   {val_loss:.6f}")
        print(f"LR: {current_lr:.2e}")
        print(f"Time: {epoch_time:.1f}s")
        
        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), 
                      os.path.join(MODEL_SAVE_PATH, 'best_model.pth'))
            print("💾 New best model saved!")
        
        # Early stopping
        early_stopping(val_loss, model)
        if early_stopping.early_stop:
            print(f"\n⏹️  Early stopping at epoch {epoch+1}")
            break
        
        # Stop if learning rate becomes too small
        if current_lr < TRAINING_CONFIG.get('min_lr', 1e-6):
            print(f"\n⏹️  Learning rate too small ({current_lr:.2e}), stopping training")
            break
    
    print(f"\n🎯 Training completed!")
    print(f"Best validation loss: {best_val_loss:.6f}")
    
    # Save training history
    with open(os.path.join(RESULTS_PATH, 'training_history.json'), 'w') as f:
        json.dump(history, f, indent=2)
    print(f"💾 Training history saved to {RESULTS_PATH}/training_history.json")
    
    # Save final model
    torch.save(model.state_dict(), os.path.join(MODEL_SAVE_PATH, 'final_model.pth'))
    print(f"💾 Final model saved to {MODEL_SAVE_PATH}/final_model.pth")
    
    # Evaluate on test set
    print("\n🧪 Evaluating on test set...")
    try:
        results = evaluate_model(model, test_loader, transform_info, device)
        
        if results:
            print(f"\n📊 Final Results:")
            print(f"RMSE: ₹{results['rmse']:.2f}")
            print(f"MAE:  ₹{results['mae']:.2f}")
            print(f"R²:   {results['r2']:.4f}")
            print(f"MAPE: {results['mape']:.2f}%")
            
            # Save evaluation results
            with open(os.path.join(RESULTS_PATH, 'final_results.json'), 'w') as f:
                json.dump(results, f, indent=2)
            print(f"💾 Results saved to {RESULTS_PATH}/final_results.json")
        
        return results
        
    except Exception as e:
        print(f"❌ Error in evaluation: {e}")
        return None

if __name__ == "__main__":
    try:
        results = main()
        if results:
            print("\n🎉 Training and evaluation completed successfully!")
        else:
            print("\n❌ Training completed but evaluation failed")
    except KeyboardInterrupt:
        print("\n⏹️ Training interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()