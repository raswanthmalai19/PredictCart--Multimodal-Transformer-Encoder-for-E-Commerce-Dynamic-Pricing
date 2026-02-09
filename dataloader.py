"""
Simple and reliable data loader for multimodal price prediction.
"""
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import pickle
import os

class PricePredictionDataset(Dataset):
    """Simple dataset for price prediction."""
    
    def __init__(self, token_sequences, targets, split_name="train"):
        # Convert to tensors and validate
        self.token_sequences = torch.tensor(token_sequences, dtype=torch.float32)
        self.targets = torch.tensor(targets, dtype=torch.float32)
        self.split_name = split_name
        
        # Basic validation
        assert len(self.token_sequences) == len(self.targets), "Length mismatch!"
        assert self.token_sequences.shape[1] == 3, f"Expected 3 tokens, got {self.token_sequences.shape[1]}"
        
        # Clean data
        self._clean_data()
        
        print(f"✅ {split_name} dataset: {len(self)} samples")
        print(f"   Token shape: {self.token_sequences.shape}")
        print(f"   Target range: {self.targets.min():.2f} to {self.targets.max():.2f}")
    
    def _clean_data(self):
        """Remove invalid samples."""
        # Find valid samples
        valid_tokens = torch.isfinite(self.token_sequences).all(dim=(1, 2))
        valid_targets = torch.isfinite(self.targets) & (self.targets > 0) & (self.targets < 20)
        valid_mask = valid_tokens & valid_targets
        
        if valid_mask.sum() < len(valid_mask):
            removed = len(valid_mask) - valid_mask.sum()
            print(f"   Removed {removed} invalid samples")
            
            self.token_sequences = self.token_sequences[valid_mask]
            self.targets = self.targets[valid_mask]
    
    def __len__(self):
        return len(self.targets)
    
    def __getitem__(self, idx):
        return self.token_sequences[idx], self.targets[idx]

def load_data(data_path, batch_size=32):
    """Load and prepare data for training."""
    
    print(f"Loading data from {data_path}")
    
    # Load prepared data
    with open(os.path.join(data_path, 'prepared_tokens.pkl'), 'rb') as f:
        data = pickle.load(f)
    
    with open(os.path.join(data_path, 'transform_info.pkl'), 'rb') as f:
        transform_info = pickle.load(f)
    
    print("✅ Data files loaded successfully")
    
    # Create datasets
    datasets = {}
    dataloaders = {}
    
    for split_name, split_data in data.items():
        dataset = PricePredictionDataset(
            split_data['token_sequences'],
            split_data['targets'],
            split_name
        )
        datasets[split_name] = dataset
        
        # Create dataloader
        dataloader = DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=(split_name == 'train'),
            num_workers=0,  # Avoid multiprocessing issues
            pin_memory=torch.cuda.is_available(),
            drop_last=False
        )
        dataloaders[split_name] = dataloader
    
    # Ensure we have required splits
    train_loader = dataloaders['train']
    val_loader = dataloaders.get('val', dataloaders.get('test'))
    test_loader = dataloaders['test']
    
    print(f"✅ Created dataloaders:")
    print(f"   Training: {len(train_loader)} batches")
    print(f"   Validation: {len(val_loader)} batches") 
    print(f"   Test: {len(test_loader)} batches")
    
    return train_loader, val_loader, test_loader, transform_info