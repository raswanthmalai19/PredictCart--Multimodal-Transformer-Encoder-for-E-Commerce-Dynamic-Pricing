# 🛒 E-Commerce Price Predictor - Web Application

A professional web application for predicting e-commerce product prices using advanced deep learning. Built with Flask, PyTorch, and Transformers.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3-green.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

- **AI-Powered Predictions**: Multimodal transformer model combining text, category, and numeric features
- **Modern UI/UX**: Beautiful, responsive interface built with modern web technologies
- **Real-time Analysis**: Instant price predictions with confidence scores
- **RESTful API**: Clean API endpoints for integration with other systems
- **Production Ready**: Includes deployment configurations and best practices

## 🏗️ Architecture

The system uses a sophisticated multimodal architecture:

1. **BERT Embeddings** for product descriptions (768-dim → 128-dim)
2. **Category Encoding** for product categories (one-hot style)
3. **Numeric Features** for ratings, reviews, and popularity metrics
4. **Transformer Encoder** to process the 3-token sequence
5. **Price Regression Head** for final price prediction

## 📋 Prerequisites

- Python 3.8 or higher
- 4GB+ RAM (8GB recommended for BERT model)
- Trained model file (`best_model.pth`)
- Feature preprocessing files (`transform_info.pkl`, `feature_prep.pkl`)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_web.txt
```

### 2. Verify Project Structure

Ensure you have the following structure:

```
e_commerce_new/
├── app.py                          # Flask application
├── predict.py                      # Prediction utilities
├── transformer.py                  # Model architecture
├── config.py                       # Configuration
├── requirements_web.txt            # Python dependencies
├── templates/
│   └── index.html                  # Frontend HTML
├── static/
│   ├── css/
│   │   └── style.css              # Styling
│   └── js/
│       └── app.js                 # Frontend JavaScript
├── simple_models/
│   └── best_model.pth             # Trained model
└── Transformer_Ready_Input/
    ├── transform_info.pkl         # Feature transformers
    └── feature_prep.pkl           # Preprocessing info
```

### 3. Update Configuration

Edit `config.py` to use correct paths:

```python
# Update these paths to match your system
DATA_PATH = "./Transformer_Ready_Input"
RESULTS_PATH = "./simple_results"
MODEL_SAVE_PATH = "./simple_models"
```

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### 5. Access the Web Interface

Open your browser and navigate to:
```
http://localhost:5000
```

## 🎯 Usage

### Web Interface

1. **Enter Product Details**:
   - Product name/description
   - Category (select from dropdown)
   - Rating (0-5 stars)
   - Number of reviews
   - Discount percentage

2. **Click "Predict Price"**

3. **View Results**:
   - Predicted price
   - Confidence level
   - Expected price range
   - Input summary

### API Endpoints

#### Predict Price
```bash
POST /api/predict
Content-Type: application/json

{
    "product_name": "Wildcraft 45L Rucksack Backpack with Rain Cover",
    "category": "fashion",
    "ratings": 4.3,
    "no_of_ratings": 1800,
    "discount_ratio": 0.25
}
```

Response:
```json
{
    "success": true,
    "prediction": {
        "price": 1899.00,
        "price_formatted": "₹1,899.00",
        "confidence": 90.0,
        "price_range": {
            "lower": 1614.15,
            "upper": 2183.85,
            "lower_formatted": "₹1,614.15",
            "upper_formatted": "₹2,183.85"
        }
    },
    "input": {
        "product_name": "Wildcraft 45L Rucksack Backpack with Rain Cover",
        "category": "fashion",
        "ratings": 4.3,
        "no_of_ratings": 1800,
        "discount_ratio": 0.25
    }
}
```

#### Get Categories
```bash
GET /api/categories
```

#### Health Check
```bash
GET /api/health
```

## 🧪 Testing

Test the prediction module directly:

```bash
python predict.py
```

This will run test predictions on sample products.

## 🔧 Configuration

### Model Settings (`config.py`)

```python
MODEL_CONFIG = {
    'd_model': 128,           # Model dimension
    'nhead': 4,              # Attention heads
    'num_layers': 2,         # Transformer layers
    'dropout': 0.2,          # Dropout rate
    'max_price_log': 13.0,   # Max log price
    'min_price_log': 2.0     # Min log price
}
```

### Available Categories

The system supports these product categories:
- Accessories
- Appliances
- Automotive
- Baby Products
- Beauty & Personal Care
- Books
- Computers & Electronics
- Fashion
- Grocery
- Health & Personal Care
- Home & Kitchen
- Music
- Pet Supplies
- Sports & Outdoors
- Toys & Games
- TV, Audio & Cameras
- Video Games

## 📊 Model Performance

Based on training results:
- **RMSE**: ~0.25 (log scale)
- **MAE**: ~₹2,500-3,000 (actual prices)
- **R² Score**: 0.85+
- **MAPE**: 15-20%

## 🚀 Production Deployment

### Using Gunicorn (Recommended)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements_web.txt .
RUN pip install --no-cache-dir -r requirements_web.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t price-predictor .
docker run -p 5000:5000 price-predictor
```

## 🛠️ Troubleshooting

### Model Not Loading
- Ensure `best_model.pth` exists in `simple_models/`
- Check file paths in `config.py`
- Verify model architecture matches the saved checkpoint

### BERT Model Download Issues
- First run requires internet to download BERT
- Model will be cached in `~/.cache/huggingface/`
- Ensure 2GB+ free disk space

### Memory Issues
- Reduce batch size if running on limited RAM
- Consider using quantized model for inference
- Close other applications to free memory

### Port Already in Use
```bash
# Change port in app.py or use:
python app.py --port 5001
```

## 📝 Development

### Project Structure

```
Frontend:
- templates/index.html    # Main interface
- static/css/style.css   # Styling
- static/js/app.js       # Client-side logic

Backend:
- app.py                 # Flask routes & API
- predict.py             # Prediction logic
- transformer.py         # Model architecture
- config.py              # Configuration

Data:
- Transformer_Ready_Input/  # Preprocessed data
- simple_models/            # Trained models
```

### Adding New Features

1. **New Category**: Update category encoder in preprocessing
2. **New Features**: Modify `prepare_numeric_features` in `predict.py`
3. **UI Changes**: Edit `templates/index.html` and `static/css/style.css`
4. **API Extensions**: Add new routes in `app.py`

## 📄 License

MIT License - feel free to use for personal or commercial projects.

## 👥 Contributors

Created with ❤️ for E-Commerce Analytics

## 🙏 Acknowledgments

- PyTorch Team for the deep learning framework
- Hugging Face for Transformers library
- Flask Team for the web framework

---

**Need Help?** Check the troubleshooting section or review the code comments for detailed explanations.
