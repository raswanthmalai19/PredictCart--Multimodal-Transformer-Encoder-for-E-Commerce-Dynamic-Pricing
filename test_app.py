#!/usr/bin/env python3
"""
Comprehensive Test Script for E-Commerce Price Prediction App
Run this to test all functionality and identify any issues.
"""
import requests
import json
import sys
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

BASE_URL = "http://localhost:5000"

def print_header(text):
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}{text}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

def print_success(text):
    print(f"{Fore.GREEN}✅ {text}{Style.RESET_ALL}")

def print_error(text):
    print(f"{Fore.RED}❌ {text}{Style.RESET_ALL}")

def print_info(text):
    print(f"{Fore.YELLOW}ℹ️  {text}{Style.RESET_ALL}")

def test_server_running():
    """Test if server is running"""
    print_header("TEST 1: Server Status")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print_success(f"Server is running on {BASE_URL}")
            return True
        else:
            print_error(f"Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error(f"Cannot connect to {BASE_URL}")
        print_info("Make sure the Flask app is running (python3 app.py)")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_health_endpoint():
    """Test health check endpoint"""
    print_header("TEST 2: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        data = response.json()
        
        print(f"Status: {data.get('status')}")
        print(f"Model Loaded: {data.get('model_loaded')}")
        
        if data.get('model_loaded'):
            print_success("Model is loaded and ready")
            return True
        else:
            print_error("Model is not loaded")
            if data.get('error'):
                print_error(f"Error: {data.get('error')}")
            return False
    except Exception as e:
        print_error(f"Health check failed: {e}")
        return False

def test_categories_endpoint():
    """Test categories endpoint"""
    print_header("TEST 3: Categories Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/api/categories", timeout=5)
        data = response.json()
        
        if data.get('success'):
            categories = data.get('categories', [])
            print_success(f"Retrieved {len(categories)} categories")
            print(f"Categories: {', '.join(categories[:5])}...")
            return True
        else:
            print_error("Failed to get categories")
            return False
    except Exception as e:
        print_error(f"Categories test failed: {e}")
        return False

def test_prediction_endpoint():
    """Test prediction endpoint with sample data"""
    print_header("TEST 4: Prediction Endpoint")
    
    test_cases = [
        {
            "name": "Electronics - Samsung TV",
            "data": {
                "product_name": "Samsung 55-inch 4K Smart TV",
                "category": "electronics",
                "ratings": 4.5,
                "no_of_ratings": 250,
                "discount_ratio": 0.15
            }
        },
        {
            "name": "Books - Fiction Novel",
            "data": {
                "product_name": "The Great Gatsby Novel",
                "category": "books",
                "ratings": 4.8,
                "no_of_ratings": 1500,
                "discount_ratio": 0.0
            }
        },
        {
            "name": "Fashion - Nike Shoes",
            "data": {
                "product_name": "Nike Air Max Running Shoes",
                "category": "fashion",
                "ratings": 4.2,
                "no_of_ratings": 800,
                "discount_ratio": 0.25
            }
        }
    ]
    
    all_passed = True
    
    for test_case in test_cases:
        print(f"\n{Fore.BLUE}Testing: {test_case['name']}{Style.RESET_ALL}")
        try:
            response = requests.post(
                f"{BASE_URL}/api/predict",
                json=test_case['data'],
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code != 200:
                print_error(f"API returned status code: {response.status_code}")
                print(f"Response: {response.text}")
                all_passed = False
                continue
            
            data = response.json()
            
            if data.get('success'):
                prediction = data.get('prediction', {})
                price = prediction.get('price')
                confidence = prediction.get('confidence')
                price_range = prediction.get('price_range', {})
                
                print_success("Prediction successful!")
                print(f"  Product: {test_case['data']['product_name']}")
                print(f"  Predicted Price: {prediction.get('price_formatted', f'₹{price}')}")
                print(f"  Confidence: {confidence}%")
                print(f"  Price Range: {price_range.get('lower_formatted')} - {price_range.get('upper_formatted')}")
                
                # Validate the prediction makes sense
                if price and price > 0:
                    print_success("Price is valid (positive number)")
                else:
                    print_error(f"Invalid price: {price}")
                    all_passed = False
                
                if confidence and 0 <= confidence <= 100:
                    print_success("Confidence is valid (0-100%)")
                else:
                    print_error(f"Invalid confidence: {confidence}")
                    all_passed = False
            else:
                print_error(f"Prediction failed: {data.get('error', 'Unknown error')}")
                all_passed = False
                
        except Exception as e:
            print_error(f"Test failed: {e}")
            all_passed = False
    
    return all_passed

def test_web_pages():
    """Test that all web pages load"""
    print_header("TEST 5: Web Pages")
    
    pages = [
        ('/', 'Home Page'),
        ('/predict', 'Prediction Page'),
        ('/about', 'About Page'),
        ('/features', 'Features Page'),
        ('/docs', 'Documentation Page'),
        ('/api-docs', 'API Documentation Page')
    ]
    
    all_passed = True
    
    for path, name in pages:
        try:
            response = requests.get(f"{BASE_URL}{path}", timeout=5)
            if response.status_code == 200:
                print_success(f"{name} - OK")
            else:
                print_error(f"{name} - Status: {response.status_code}")
                all_passed = False
        except Exception as e:
            print_error(f"{name} - Error: {e}")
            all_passed = False
    
    return all_passed

def test_invalid_inputs():
    """Test error handling with invalid inputs"""
    print_header("TEST 6: Error Handling")
    
    invalid_cases = [
        {
            "name": "Missing product name",
            "data": {"category": "electronics", "ratings": 4.5},
            "expected": "Missing required field"
        },
        {
            "name": "Invalid ratings",
            "data": {"product_name": "Test", "category": "electronics", "ratings": 6.0},
            "expected": "Ratings must be between 0 and 5"
        },
        {
            "name": "Invalid discount ratio",
            "data": {"product_name": "Test", "category": "electronics", "discount_ratio": 1.5},
            "expected": "Discount ratio must be between 0 and 1"
        }
    ]
    
    all_passed = True
    
    for test_case in invalid_cases:
        print(f"\n{Fore.BLUE}Testing: {test_case['name']}{Style.RESET_ALL}")
        try:
            response = requests.post(
                f"{BASE_URL}/api/predict",
                json=test_case['data'],
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            data = response.json()
            
            if not data.get('success') and 'error' in data:
                print_success(f"Properly rejected invalid input")
                print(f"  Error message: {data['error']}")
            else:
                print_error("Should have rejected invalid input but didn't")
                all_passed = False
                
        except Exception as e:
            print_error(f"Test failed: {e}")
            all_passed = False
    
    return all_passed

def main():
    """Run all tests"""
    print(f"{Fore.MAGENTA}")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "E-COMMERCE PRICE PREDICTION TEST SUITE" + " " * 9 + "║")
    print("╚" + "═" * 58 + "╝")
    print(f"{Style.RESET_ALL}")
    
    print_info(f"Testing server at: {BASE_URL}")
    print_info("Make sure the Flask app is running before running tests\n")
    
    results = {
        "Server Status": test_server_running(),
        "Health Check": False,
        "Categories": False,
        "Predictions": False,
        "Web Pages": False,
        "Error Handling": False
    }
    
    # Only run other tests if server is running
    if results["Server Status"]:
        results["Health Check"] = test_health_endpoint()
        results["Categories"] = test_categories_endpoint()
        results["Predictions"] = test_prediction_endpoint()
        results["Web Pages"] = test_web_pages()
        results["Error Handling"] = test_invalid_inputs()
    
    # Print summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        if result:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
    
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    if passed == total:
        print(f"{Fore.GREEN}✅ ALL TESTS PASSED ({passed}/{total}){Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}🎉 Your application is working perfectly!{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}You can now use the app at: {BASE_URL}{Style.RESET_ALL}")
        return 0
    else:
        print(f"{Fore.RED}❌ SOME TESTS FAILED ({passed}/{total} passed){Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Please check the errors above to identify issues{Style.RESET_ALL}")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Tests interrupted by user{Style.RESET_ALL}")
        sys.exit(1)
