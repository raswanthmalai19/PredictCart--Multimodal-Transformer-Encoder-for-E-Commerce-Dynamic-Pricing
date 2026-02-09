#!/usr/bin/env python3
"""
Quick Start Script for E-Commerce Price Predictor Web App
Run this to quickly test if everything is set up correctly.
"""

import os
import sys

def check_environment():
    """Check if the environment is properly set up."""
    print("🔍 Checking Environment Setup...")
    print("=" * 60)
    
    issues = []
    
    # Check Python version
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"❌ Python version: {version.major}.{version.minor}.{version.micro}")
        issues.append("Python 3.8+ required")
    
    # Check required packages
    required_packages = [
        'flask',
        'torch',
        'transformers',
        'numpy',
        'pandas',
        'sklearn'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ Package: {package}")
        except ImportError:
            print(f"❌ Package: {package} (not installed)")
            issues.append(f"Install {package}")
    
    # Check required files
    required_files = {
        'Model': 'simple_models/best_model.pth',
        'Transform Info': 'Transformer_Ready_Input/transform_info.pkl',
        'Feature Prep': 'Transformer_Ready_Input/feature_prep.pkl',
        'App': 'app.py',
        'Predictor': 'predict.py',
        'Transformer': 'transformer.py'
    }
    
    for name, filepath in required_files.items():
        if os.path.exists(filepath):
            print(f"✅ {name}: {filepath}")
        else:
            print(f"❌ {name}: {filepath} (missing)")
            issues.append(f"Missing {filepath}")
    
    # Check directories
    required_dirs = ['templates', 'static/css', 'static/js']
    for dirname in required_dirs:
        if os.path.isdir(dirname):
            print(f"✅ Directory: {dirname}")
        else:
            print(f"❌ Directory: {dirname} (missing)")
            issues.append(f"Missing directory {dirname}")
    
    print("=" * 60)
    
    if issues:
        print("\n⚠️  Issues Found:")
        for issue in issues:
            print(f"   - {issue}")
        print("\nPlease fix these issues before starting the application.")
        return False
    else:
        print("\n✅ All checks passed! Environment is ready.")
        return True


def test_predictor():
    """Test the prediction module."""
    print("\n🧪 Testing Prediction Module...")
    print("=" * 60)
    
    try:
        from predict import PricePredictor
        
        print("Loading predictor...")
        predictor = PricePredictor()
        
        print("\nTesting sample prediction...")
        price, confidence = predictor.predict_price(
            product_name="Samsung Galaxy S21 5G Smartphone",
            category="electronics",
            ratings=4.5,
            no_of_ratings=1500,
            discount_ratio=0.15
        )
        
        print(f"\n✅ Prediction successful!")
        print(f"   Product: Samsung Galaxy S21 5G")
        print(f"   Predicted Price: ₹{price:,.2f}")
        print(f"   Confidence: {confidence*100:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function."""
    print("\n" + "=" * 60)
    print("🛒 E-Commerce Price Predictor - Quick Start Check")
    print("=" * 60 + "\n")
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please fix the issues above.")
        sys.exit(1)
    
    # Test predictor
    print("\n")
    if not test_predictor():
        print("\n❌ Predictor test failed. Check error messages above.")
        sys.exit(1)
    
    # Success
    print("\n" + "=" * 60)
    print("✅ All tests passed! Your setup is working correctly.")
    print("=" * 60)
    print("\nTo start the web application, run:")
    print("   python app.py")
    print("\nOr use the startup script:")
    print("   bash start_web.sh")
    print("\nThe application will be available at:")
    print("   http://localhost:5000")
    print("")


if __name__ == "__main__":
    main()
