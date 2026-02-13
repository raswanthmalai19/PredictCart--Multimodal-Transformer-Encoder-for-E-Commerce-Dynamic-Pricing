"""
Quick Start Flask App - Loads UI immediately, model on first prediction
"""
from flask import Flask, render_template, request, jsonify
import traceback

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ecommerce-price-predictor-2026'
app.config['JSON_SORT_KEYS'] = False

# Predictor loaded on first use
_predictor = None
_loading = False

def load_predictor():
    """Load predictor lazily."""
    global _predictor, _loading
    
    if _predictor is not None:
        return _predictor
    
    if _loading:
        return None
    
    _loading = True
    try:
        print("🔄 Loading predictor (this may take 2-3 minutes on first run)...")
        from predict import get_predictor
        _predictor = get_predictor()
        print("✅ Predictor loaded!")
        return _predictor
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return None
    finally:
        _loading = False

@app.route('/')
def home():
    """Landing page."""
    return render_template('home.html')

@app.route('/predict')
def predict_page():
    """Prediction tool page."""
    categories = [
        'accessories', 'appliances', 'automotive', 'baby',
        'beauty', 'books', 'car & motorbike', 'computers',
        'electronics', 'fashion', 'grocery', 'health & personal care',
        'home & kitchen', 'music', 'pet supplies', 'sports',
        'toys & games', 'tv, audio & cameras', 'video games'
    ]
    return render_template('predict.html', categories=categories)

@app.route('/docs')
def docs():
    """Documentation page."""
    return render_template('docs.html')

@app.route('/about')
def about():
    """About page."""
    return render_template('about.html')

@app.route('/features')
def features():
    """Features page."""
    return render_template('features.html')

@app.route('/api-docs')
def api_docs():
    """API Documentation page."""
    return render_template('api_docs.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict price."""
    try:
        # Load predictor if not loaded
        predictor = load_predictor()
        
        if predictor is None:
            return jsonify({
                'success': False,
                'error': 'Model is loading... Please wait 2-3 minutes and try again.'
            }), 503
        
        # Get data
        data = request.get_json()
        
        # Validate
        if not data.get('product_name') or not data.get('category'):
            return jsonify({
                'success': False,
                'error': 'Product name and category are required'
            }), 400
        
        # Make prediction
        price, conf = predictor.predict_price(
            product_name=data['product_name'],
            category=data['category'],
            ratings=float(data.get('ratings', 4.0)),
            no_of_ratings=int(data.get('no_of_ratings', 100)),
            discount_ratio=float(data.get('discount_ratio', 0.0))
        )
        
        # Return result
        return jsonify({
            'success': True,
            'prediction': {
                'price': round(price, 2),
                'price_formatted': f"₹{price:,.2f}",
                'confidence': round(conf * 100, 1),
                'price_range': {
                    'lower': round(price * 0.85, 2),
                    'upper': round(price * 1.15, 2),
                    'lower_formatted': f"₹{price * 0.85:,.2f}",
                    'upper_formatted': f"₹{price * 1.15:,.2f}"
                }
            },
            'input': data
        })
    
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get categories."""
    return jsonify({
        'success': True,
        'categories': [
            'accessories', 'appliances', 'automotive', 'baby',
            'beauty', 'books', 'car & motorbike', 'computers',
            'electronics', 'fashion', 'grocery', 'health & personal care',
            'home & kitchen', 'music', 'pet supplies', 'sports',
            'toys & games', 'tv, audio & cameras', 'video games'
        ]
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Health check."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': _predictor is not None,
        'loading': _loading
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🛒 PredictCart - E-Commerce Price Predictor")
    print("="*60)
    print("\n✅ Server starting...")
    print("📱 Open: http://localhost:5000")
    print("⚡ UI loads instantly!")
    print("🤖 Model loads on first prediction (2-3 min first time)")
    print("\n" + "="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
