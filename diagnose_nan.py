#!/usr/bin/env python3
"""
Diagnostic Script to Debug NaN Predictions
"""
import requests
import json
import sys

def test_prediction(product_name, category, ratings, no_of_ratings, discount_ratio):
    """Test a single prediction and show detailed output."""
    
    print(f"\n{'='*60}")
    print(f"Testing Prediction")
    print(f"{'='*60}")
    print(f"Product: {product_name}")
    print(f"Category: {category}")
    print(f"Ratings: {ratings}")
    print(f"No. of Ratings: {no_of_ratings}")
    print(f"Discount: {discount_ratio * 100}%")
    print(f"{'='*60}\n")
    
    try:
        response = requests.post(
            'http://localhost:5000/api/predict',
            json={
                'product_name': product_name,
                'category': category,
                'ratings': ratings,
                'no_of_ratings': no_of_ratings,
                'discount_ratio': discount_ratio
            },
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"\nFull Response:")
        print(json.dumps(response.json(), indent=2))
        
        data = response.json()
        
        if data.get('success'):
            prediction = data.get('prediction', {})
            price = prediction.get('price')
            
            print(f"\n{'='*60}")
            if price is None or (isinstance(price, float) and (price != price)):  # Check for NaN
                print(f"❌ PROBLEM FOUND: Price is NaN or None!")
                print(f"Raw price value: {price}")
            else:
                print(f"✅ SUCCESS: Valid prediction received!")
                print(f"Price: {prediction.get('price_formatted', f'₹{price}')}")
                print(f"Confidence: {prediction.get('confidence')}%")
            print(f"{'='*60}\n")
        else:
            print(f"\n❌ API Error: {data.get('error')}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure Flask app is running on port 5000")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\n🔍 NaN Prediction Diagnostic Tool\n")
    
    # Test various products
    test_cases = [
        {
            'product_name': 'Samsung Galaxy S21 Ultra 5G 128GB',
            'category': 'electronics',
            'ratings': 4.5,
            'no_of_ratings': 1250,
            'discount_ratio': 0.15
        },
        {
            'product_name': 'Sony WH-1000XM4 Headphones',
            'category': 'electronics',
            'ratings': 4.8,
            'no_of_ratings': 3420,
            'discount_ratio': 0.20
        },
        {
            'product_name': 'Test Product',
            'category': 'electronics',
            'ratings': 4.0,
            'no_of_ratings': 100,
            'discount_ratio': 0.0
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'#'*60}")
        print(f"TEST CASE {i} of {len(test_cases)}")
        print(f"{'#'*60}")
        test_prediction(**test_case)
        
        if i < len(test_cases):
            input("Press Enter to continue to next test...")
    
    print("\n✅ Diagnostic complete!")
