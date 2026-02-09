"""
Simple but effective multimodal transformer for price prediction.
Specialized for 3-token sequences: [text, category, numeric]
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class MultimodalPriceTransformer(nn.Module):
    """
    Simple multimodal transformer specialized for price prediction.
    Handles 3 tokens: text embedding, category embedding, numeric features.
    """
    
    def __init__(self, d_model=128, nhead=4, num_layers=2, dropout=0.2, 
                 max_price_log=13.0, min_price_log=2.0):
        super().__init__()
        
        self.d_model = d_model
        self.max_price_log = max_price_log
        self.min_price_log = min_price_log
        
        print(f"Creating multimodal transformer:")
        print(f"  - Model dimension: {d_model}")
        print(f"  - Attention heads: {nhead}")
        print(f"  - Layers: {num_layers}")
        print(f"  - Dropout: {dropout}")
        
        # Positional encoding for 3 tokens
        self.pos_encoding = nn.Parameter(torch.randn(3, d_model) * 0.1)
        
        # Token type embeddings (helps distinguish different modalities)
        self.token_type_embedding = nn.Embedding(3, d_model)
        
        # Transformer encoder layers
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=d_model * 2,  # Simple 2x expansion
            dropout=dropout,
            activation='relu',
            batch_first=True,
            norm_first=True  # Pre-norm for stability
        )
        
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers)
        
        # Attention pooling - learns which tokens are important
        self.attention_pooling = nn.MultiheadAttention(
            embed_dim=d_model,
            num_heads=1,  # Single head for simplicity
            dropout=dropout,
            batch_first=True
        )
        
        # Simple price prediction head
        self.price_head = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(d_model, d_model // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_model // 2, 1)
        )
        
        # Initialize weights properly
        self._init_weights()
        
        total_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        print(f"✅ Model created with {total_params:,} parameters")
    
    def _init_weights(self):
        """Initialize weights for stable training."""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
            elif isinstance(module, nn.LayerNorm):
                nn.init.ones_(module.weight)
                nn.init.zeros_(module.bias)
    
    def forward(self, token_sequence):
        """
        Forward pass for price prediction.
        
        Args:
            token_sequence: [batch_size, 3, d_model] - 3 tokens per sample
        
        Returns:
            price_predictions: [batch_size] - predicted log prices
        """
        batch_size, seq_len, _ = token_sequence.shape
        
        # Add positional encoding
        pos_encoded = token_sequence + self.pos_encoding.unsqueeze(0)
        
        # Add token type embeddings (0=text, 1=category, 2=numeric)
        token_types = torch.arange(3, device=token_sequence.device).unsqueeze(0).expand(batch_size, -1)
        type_embedded = pos_encoded + self.token_type_embedding(token_types)
        
        # Apply transformer layers
        encoded = self.transformer(type_embedded)
        
        # Attention pooling - let model decide which tokens matter most
        # Use first token as query, all tokens as keys/values
        query = encoded[:, 0:1]  # [batch_size, 1, d_model]
        pooled, attention_weights = self.attention_pooling(query, encoded, encoded)
        pooled = pooled.squeeze(1)  # [batch_size, d_model]
        
        # Predict price
        price_logits = self.price_head(pooled).squeeze(-1)  # [batch_size]
        
        # Constrain to reasonable price range
        price_pred = torch.clamp(price_logits, self.min_price_log, self.max_price_log)
        
        return price_pred
    
    def get_attention_weights(self, token_sequence):
        """Get attention weights for interpretation."""
        self.eval()
        with torch.no_grad():
            batch_size, seq_len, _ = token_sequence.shape
            
            # Forward pass to get attention
            pos_encoded = token_sequence + self.pos_encoding.unsqueeze(0)
            token_types = torch.arange(3, device=token_sequence.device).unsqueeze(0).expand(batch_size, -1)
            type_embedded = pos_encoded + self.token_type_embedding(token_types)
            encoded = self.transformer(type_embedded)
            
            query = encoded[:, 0:1]
            _, attention_weights = self.attention_pooling(query, encoded, encoded)
            
            return attention_weights  # [batch_size, 1, 3]


class SimplePricePredictor(nn.Module):
    """
    Ultra-simple fallback model if transformer doesn't work.
    """
    
    def __init__(self, d_model=128):
        super().__init__()
        
        self.global_pool = nn.AdaptiveAvgPool1d(1)
        self.predictor = nn.Sequential(
            nn.Linear(d_model, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, 1)
        )
        
        print("✅ Created simple fallback predictor")
    
    def forward(self, token_sequence):
        # Simple global average pooling
        pooled = self.global_pool(token_sequence.transpose(1, 2)).squeeze(-1)
        price_pred = self.predictor(pooled).squeeze(-1)
        return torch.clamp(price_pred, 2.0, 13.0)