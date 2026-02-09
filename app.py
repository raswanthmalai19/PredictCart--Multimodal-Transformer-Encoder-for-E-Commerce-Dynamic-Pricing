"""
Flask Web Application for E-Commerce Price Prediction
Professional frontend for multimodal price prediction model.
"""
from flask import Flask, render_template, request, jsonify
import traceback
import os
from predict import get_predictor

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ecommerce-price-predictor-2026'
app.config['JSON_SORT_KEYS'] = False

# Initialize predictor
print("🚀 Starting Flask Application...")
predictor = None

def initialize_predictor():
    """Initialize predictor on first request."""
    global predictor
    if predictor is None:
        try:
            predictor = get_predictor()
            print("✅ Predictor initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing predictor: {e}")
            traceback.print_exc()

@app.route('/')
def index():
    """Render main page."""
    initialize_predictor()
    categories = predictor.get_available_categories() if predictor else []
    return render_template('index.html', categories=categories)

@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for price prediction."""
    try:
        initialize_predictor()
        
        if predictor is None:
            return jsonify({
                'success': False,
                'error': 'Model not loaded. Please check server logs.'
            }), 500
        
        # Get input data
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['product_name', 'category']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Extract parameters
        product_name = data['product_name'].strip()
        category = data['category'].strip().lower()
        ratings = float(data.get('ratings', 4.0))
        no_of_ratings = int(data.get('no_of_ratings', 100))
        discount_ratio = float(data.get('discount_ratio', 0.0))
        
        # Validate ranges
        if not (0 <= ratings <= 5):
            return jsonify({
                'success': False,
                'error': 'Ratings must be between 0 and 5'
            }), 400
        
        if no_of_ratings < 0:
            return jsonify({
                'success': False,
                'error': 'Number of ratings must be positive'
            }), 400
        
        if not (0 <= discount_ratio <= 1):
            return jsonify({
                'success': False,
                'error': 'Discount ratio must be between 0 and 1'
            }), 400
        
        # Make prediction
        predicted_price, confidence = predictor.predict_price(
            product_name=product_name,
            category=category,
            ratings=ratings,
            no_of_ratings=no_of_ratings,
            discount_ratio=discount_ratio
        )
        
        # Calculate price range (confidence interval)
        price_lower = predicted_price * 0.85
        price_upper = predicted_price * 1.15
        
        # Return results
        return jsonify({
            'success': True,
            'prediction': {
                'price': round(predicted_price, 2),
                'price_formatted': f"₹{predicted_price:,.2f}",
                'confidence': round(confidence * 100, 1),
                'price_range': {
                    'lower': round(price_lower, 2),
                    'upper': round(price_upper, 2),
                    'lower_formatted': f"₹{price_lower:,.2f}",
                    'upper_formatted': f"₹{price_upper:,.2f}"
                }
            },
            'input': {
                'product_name': product_name,
                'category': category,
                'ratings': ratings,
                'no_of_ratings': no_of_ratings,
                'discount_ratio': discount_ratio
            }
        })
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid input: {str(e)}'
        }), 400
    
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': 'An error occurred during prediction. Please try again.'
        }), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get available product categories."""
    try:
        initialize_predictor()
        
        if predictor is None:
            return jsonify({
                'success': False,
                'error': 'Model not loaded'
            }), 500
        
        categories = predictor.get_available_categories()
        
        return jsonify({
            'success': True,
            'categories': categories
        })
    
    except Exception as e:
        print(f"❌ Error fetching categories: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    initialize_predictor()
    
    return jsonify({
        'status': 'healthy' if predictor else 'initializing',
        'model_loaded': predictor is not None
    })

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🛒 E-Commerce Price Prediction System")
    print("="*60)
    print("\nStarting Flask web server...")
    print("Access the application at: http://localhost:5000")
    print("API Documentation:")
    print("  POST /api/predict - Predict product price")
    print("  GET  /api/categories - Get available categories")
    print("  GET  /api/health - Health check")
    print("\n" + "="*60 + "\n")
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False  # Prevent double loading of model
    )
