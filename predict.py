"""
Price Prediction Utilities for Frontend
Handles model loading, input preprocessing, and prediction.
"""
import torch
import numpy as np
import pickle
import os
from transformers import AutoTokenizer, AutoModel
from transformer import MultimodalPriceTransformer
from config import MODEL_CONFIG, MODEL_SAVE_PATH, DATA_PATH
from preprocessing_utils import FeaturePreparation

class PricePredictor:
    """Handles all prediction operations for the frontend."""
    
    def __init__(self, model_path=None, device=None):
        print("🚀 Initializing Price Predictor...")
        
        # Setup device
        self.device = device or torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"   Using device: {self.device}")
        
        # Load BERT model for text embeddings
        print("   Loading BERT model...")
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.bert_model = AutoModel.from_pretrained('bert-base-uncased').to(self.device)
        self.bert_model.eval()
        
        # Load feature preprocessing info
        print("   Loading feature preprocessors...")
        transform_path = os.path.join(DATA_PATH, 'transform_info.pkl')
        try:
            with open(transform_path, 'rb') as f:
                self.transform_info = pickle.load(f)
        except Exception as e:
            print(f"   Warning: Could not load transform_info: {e}")
            self.transform_info = {}
        
        # Initialize feature preparation
        self.feature_prep = FeaturePreparation()
        
        # Try to load feature prep if available
        feature_prep_path = os.path.join(DATA_PATH, 'feature_prep.pkl')
        try:
            with open(feature_prep_path, 'rb') as f:
                loaded_prep = pickle.load(f)
                if hasattr(loaded_prep, 'scalers'):
                    self.feature_prep.scalers = loaded_prep.scalers
                    self.feature_prep.fitted = loaded_prep.fitted
                    print("   ✅ Loaded feature preprocessor from pickle")
        except Exception as e:
            print(f"   Warning: Could not load feature_prep pickle: {e}")
            print("   Using empty feature preparation")
        
        # Load price prediction model
        print("   Loading price prediction model...")
        if model_path is None:
            model_path = os.path.join(MODEL_SAVE_PATH, 'best_model.pth')
        
        self.model = MultimodalPriceTransformer(**MODEL_CONFIG).to(self.device)
        
        # Load checkpoint
        checkpoint = torch.load(model_path, map_location=self.device)
        if 'model_state_dict' in checkpoint:
            self.model.load_state_dict(checkpoint['model_state_dict'])
        else:
            self.model.load_state_dict(checkpoint)
        
        self.model.eval()
        print("✅ Price Predictor ready!")
    
    def get_available_categories(self):
        """Get list of available product categories."""
        if 'category_encoder' in self.feature_prep:
            categories = self.feature_prep['category_encoder'].classes_.tolist()
            return sorted(categories)
        else:
            # Fallback to common categories from your dataset
            return sorted([
                'accessories', 'appliances', 'automotive', 'baby', 'beauty',
                'books', 'car & motorbike', 'computers', 'electronics', 
                'fashion', 'grocery', 'health & personal care', 'home & kitchen',
                'music', 'pet supplies', 'sports', 'toys & games', 'tv, audio & cameras',
                'video games'
            ])
    
    def encode_text(self, text):
        """Encode product text using BERT."""
        # Tokenize
        inputs = self.tokenizer(
            text,
            return_tensors='pt',
            padding=True,
            truncation=True,
            max_length=128
        ).to(self.device)
        
        # Get BERT embeddings
        with torch.no_grad():
            outputs = self.bert_model(**inputs)
            # Use CLS token embedding
            text_embedding = outputs.last_hidden_state[:, 0, :]  # [1, 768]
        
            # Project to model dimension
            d_model = MODEL_CONFIG['d_model']
            if text_embedding.shape[-1] != d_model:
                # Simple linear projection
                projection = torch.nn.Linear(text_embedding.shape[-1], d_model).to(self.device)
                projection.eval()
                text_embedding = projection(text_embedding)
        
        return text_embedding.squeeze(0).detach().cpu().numpy()  # [d_model]
    
    def encode_category(self, category):
        """Encode product category."""
        d_model = MODEL_CONFIG['d_model']
        
        # Use encoder if available
        if hasattr(self.feature_prep, 'encoders') and 'category_encoder' in self.feature_prep.encoders:
            encoder = self.feature_prep.encoders['category_encoder']
            try:
                category_idx = encoder.transform([category])[0]
            except:
                # Unknown category - use mean encoding
                category_idx = len(encoder.classes_) // 2
        else:
            # Simple hash-based encoding
            category_idx = hash(category.lower()) % 100
        
        # Create embedding (simple one-hot style)
        category_embedding = np.zeros(d_model)
        category_embedding[category_idx % d_model] = 1.0
        
        return category_embedding
    
    def prepare_numeric_features(self, ratings, no_of_ratings, discount_ratio=0.0):
        """Prepare numeric features."""
        d_model = MODEL_CONFIG['d_model']
        
        # Create feature array
        features = []
        
        # Ratings (0-5 scale)
        features.append(ratings / 5.0)
        
        # Log number of ratings (log scale)
        log_ratings = np.log1p(no_of_ratings)
        features.append(log_ratings / 10.0)  # Normalize
        
        # Discount ratio (0-1)
        features.append(discount_ratio)
        
        # Popularity (derived from ratings count)
        popularity = ratings * np.log1p(no_of_ratings)
        features.append(popularity / 30.0)  # Normalize
        
        # Create embedding by repeating and padding
        features = np.array(features)
        numeric_embedding = np.zeros(d_model)
        
        # Repeat features to fill embedding
        for i in range(d_model):
            numeric_embedding[i] = features[i % len(features)]
        
        return numeric_embedding
    
    def predict_price(self, product_name, category, ratings=4.0, no_of_ratings=100, 
                     discount_ratio=0.0):
        """
        Predict price for a product.
        
        Args:
            product_name: Product name/description
            category: Product category
            ratings: Product rating (0-5)
            no_of_ratings: Number of ratings
            discount_ratio: Discount ratio (0-1)
        
        Returns:
            predicted_price: Predicted price in rupees
            confidence: Confidence score (0-1)
        """
        # Encode inputs
        text_emb = self.encode_text(product_name)
        category_emb = self.encode_category(category)
        numeric_emb = self.prepare_numeric_features(ratings, no_of_ratings, discount_ratio)
        
        # Create 3-token sequence [text, category, numeric]
        token_sequence = np.stack([text_emb, category_emb, numeric_emb], axis=0)  # [3, d_model]
        token_sequence = torch.tensor(token_sequence, dtype=torch.float32).unsqueeze(0)  # [1, 3, d_model]
        token_sequence = token_sequence.to(self.device)
        
        # Predict
        with torch.no_grad():
            log_price = self.model(token_sequence).squeeze().item()
        
        # Inverse transform to get actual price
        predicted_price = np.exp(log_price)
        
        # Calculate confidence (based on typical price ranges)
        # Lower confidence for extreme predictions
        if predicted_price < 100 or predicted_price > 100000:
            confidence = 0.6
        elif predicted_price < 500 or predicted_price > 50000:
            confidence = 0.75
        else:
            confidence = 0.9
        
        return predicted_price, confidence
    
    def predict_batch(self, products):
        """
        Predict prices for multiple products.
        
        Args:
            products: List of dicts with keys: product_name, category, ratings, no_of_ratings, discount_ratio
        
        Returns:
            List of (predicted_price, confidence) tuples
        """
        results = []
        for product in products:
            price, confidence = self.predict_price(
                product.get('product_name', ''),
                product.get('category', 'electronics'),
                product.get('ratings', 4.0),
                product.get('no_of_ratings', 100),
                product.get('discount_ratio', 0.0)
            )
            results.append((price, confidence))
        
        return results


# Global predictor instance (singleton)
_predictor = None

def get_predictor():
    """Get or create predictor instance."""
    global _predictor
    if _predictor is None:
        _predictor = PricePredictor()
    return _predictor


if __name__ == "__main__":
    # Test the predictor
    print("\n" + "="*60)
    print("Testing Price Predictor")
    print("="*60 + "\n")
    
    predictor = get_predictor()
    
    # Test predictions
    test_products = [
        {
            'product_name': 'Samsung Galaxy S21 5G Smartphone',
            'category': 'electronics',
            'ratings': 4.5,
            'no_of_ratings': 1500,
            'discount_ratio': 0.15
        },
        {
            'product_name': 'Nike Air Zoom Running Shoes',
            'category': 'sports',
            'ratings': 4.2,
            'no_of_ratings': 320,
            'discount_ratio': 0.25
        },
        {
            'product_name': 'Harry Potter Complete Book Set',
            'category': 'books',
            'ratings': 4.8,
            'no_of_ratings': 5000,
            'discount_ratio': 0.30
        }
    ]
    
    for product in test_products:
        price, confidence = predictor.predict_price(**product)
        print(f"Product: {product['product_name']}")
        print(f"Category: {product['category']}")
        print(f"Predicted Price: ₹{price:,.2f}")
        print(f"Confidence: {confidence*100:.1f}%")
        print("-" * 60)
