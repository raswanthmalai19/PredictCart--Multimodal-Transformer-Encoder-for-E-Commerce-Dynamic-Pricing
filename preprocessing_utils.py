"""
Feature Preprocessing Utilities for E-Commerce Price Prediction
Extracted from PREPROCESSING_PIPELINE.ipynb for use in the web application.
"""
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class FeaturePreparation:
    def __init__(self, scale_target=False):
        """
        Enhanced Feature Preparation with CRITICAL FIX for negative values issue.
        
        Args:
            scale_target: Whether to scale target variable (DISABLED to prevent negative values)
        """
        # Updated parameter from 'sparse' to 'sparse_output'
        self.main_category_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        self.sub_category_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        self.numeric_scaler = StandardScaler()

        # CRITICAL FIX: Target scaler conditionally initialized
        self.scale_target = scale_target
        self.target_scaler = StandardScaler() if scale_target else None

        self.fitted = False
        self.target_fitted = False

        # Enhanced statistics storage for debugging
        self.original_target_stats = {}
        self.log_transformed_stats = {}
        self.scaled_target_stats = {}
        self.transformation_metadata = {
            'target_scaling_enabled': scale_target,
            'fix_applied': 'Disabled target scaling to prevent negative values',
            'reason': 'StandardScaler after log transform creates negative values that break inverse transform',
            'training_approach': 'Use log-transformed targets directly for better stability'
        }

        print(f"✅ FeaturePreparation initialized with CRITICAL FIX:")
        print(f"   - Target scaling: {'ENABLED' if scale_target else 'DISABLED (FIXED)'}")
        print(f"   - Will use log-transformed targets directly for training")
        if not scale_target:
            print(f"   - 🔧 FIX: Prevents negative values that break inverse transformation")
    
    def fit(self, df):
        """Fit encoders and scalers to the data."""
        print("Fitting category encoders and numeric scaler...")
        self.main_category_encoder.fit(df[['main_category']])
        self.sub_category_encoder.fit(df[['sub_category']])

        numeric_features = ['discount_price', 'actual_price', 'discount_ratio',
                            'popularity', 'ratings', 'log_no_of_ratings']
        self.numeric_scaler.fit(df[numeric_features])
        self.fitted = True

        print("✅ Feature fitting complete!")
        return self

    def fit_target(self, y, store_stats=True):
        """Fit target scaler with proper validation and statistics storage."""
        print(f"\n=== Target Processing (Scale Target: {self.scale_target}) ===")
        print(f"Input range: {np.min(y):.4f} to {np.max(y):.4f}")
        print(f"Input mean: {np.mean(y):.4f}, std: {np.std(y):.4f}")

        # Store log-transformed statistics
        if store_stats:
            self.log_transformed_stats = {
                'min': float(np.min(y)),
                'max': float(np.max(y)),
                'mean': float(np.mean(y)),
                'std': float(np.std(y)),
                'median': float(np.median(y)),
                'negative_count': int(np.sum(y < 0)),
                'positive_count': int(np.sum(y >= 0))
            }

            # CRITICAL CHECK: Verify no negative values in log-transformed data
            if np.any(y < 0):
                print(f"⚠️  WARNING: Found {np.sum(y < 0)} negative values in log-transformed data!")
            else:
                print(f"✅ GOOD: All {len(y)} log-transformed values are non-negative")
        
        if self.scale_target and self.target_scaler is not None:
            # Fit the scaler only if enabled
            y_reshaped = y.reshape(-1, 1)
            self.target_scaler.fit(y_reshaped)
            print(f"✅ Target scaler fitted!")
            print(f"   Scaler mean_: {self.target_scaler.mean_[0]:.4f}")
            print(f"   Scaler scale_: {self.target_scaler.scale_[0]:.4f}")
        else:
            print(f"🔧 Target scaling DISABLED - using log-transformed values directly")
            print(f"   This prevents negative values that break inverse transformation")
        
        self.target_fitted = True
        return self

    def transform_target(self, y):
        """Transform target variable with validation."""
        if not self.target_fitted:
            raise ValueError("Target scaler is not fitted yet.")

        if self.scale_target and self.target_scaler is not None:
            y_transformed = self.target_scaler.transform(y.reshape(-1, 1)).flatten()
            print(f"Target scaling: {np.min(y):.4f}-{np.max(y):.4f} → {np.min(y_transformed):.4f}-{np.max(y_transformed):.4f}")
            
            # CRITICAL CHECK: Warn if scaling creates negative values
            if np.any(y_transformed < 0):
                neg_count = np.sum(y_transformed < 0)
                print(f"⚠️  WARNING: Target scaling created {neg_count} negative values!")
                print(f"   This will break inverse log transformation!")

            return y_transformed
        else:
            print(f"🔧 Using log-transformed targets directly (no scaling)")
            print(f"   Range: {np.min(y):.4f} to {np.max(y):.4f}")
            return y  # Return log-transformed values directly

    def inverse_transform_target(self, y_scaled):
        """Inverse transform with validation."""
        if not self.target_fitted:
            raise ValueError("Target scaler is not fitted yet.")

        if self.scale_target and self.target_scaler is not None:
            y_unscaled = self.target_scaler.inverse_transform(y_scaled.reshape(-1, 1)).flatten()
            print(f"Inverse scaling: {np.min(y_scaled):.4f}-{np.max(y_scaled):.4f} → {np.min(y_unscaled):.4f}-{np.max(y_unscaled):.4f}")
            return y_unscaled
        else:
            print(f"🔧 No inverse scaling needed - returning log-transformed values")
            print(f"   Range: {np.min(y_scaled):.4f} to {np.max(y_scaled):.4f}")
            return y_scaled  # Return as-is (still log-transformed)

    def transform(self, df, add_noise=False, noise_level=0.05):
        """Transform features to be ready for the model."""
        if not self.fitted:
            raise ValueError("FeaturePreparation is not fitted yet.")

        print("Transforming features...")

        # One-hot encode categories
        main_cat_encoded = self.main_category_encoder.transform(df[['main_category']])
        sub_cat_encoded = self.sub_category_encoder.transform(df[['sub_category']])
        
        # Scale numeric features
        numeric_features = ['discount_price', 'actual_price', 'discount_ratio',
                           'popularity', 'ratings', 'log_no_of_ratings']
        numeric_scaled = self.numeric_scaler.transform(df[numeric_features])

        # Optionally add Gaussian noise to numeric features (for uncertainty modeling)
        if add_noise:
            noise = np.random.normal(0, noise_level, numeric_scaled.shape)
            numeric_scaled = numeric_scaled + noise
            print(f"Adding Gaussian noise (level={noise_level})...")

        print("✅ Feature transformation complete!")

        return {
            'main_category': main_cat_encoded,
            'sub_category': sub_cat_encoded,
            'numeric_features': numeric_scaled
        }

    def fit_transform(self, df, add_noise=False, noise_level=0.05):
        """Convenience method to fit and transform in one step."""
        self.fit(df)
        return self.transform(df, add_noise, noise_level)
