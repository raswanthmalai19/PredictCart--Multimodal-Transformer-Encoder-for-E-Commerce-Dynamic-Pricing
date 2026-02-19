# 🛒 PredictCart: Multimodal Transformer for E-Commerce Dynamic Pricing

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![Transformers](https://img.shields.io/badge/🤗_Transformers-4.35+-yellow.svg)](https://huggingface.co/transformers/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)

> **AI-Powered Amazon India Price Prediction** combining BERT embeddings, category encodings, and numeric features through a compact multimodal transformer. Trained on real Amazon India listings, best for products in the ₹200–₹25,000 range.

![PredictCart Demo](https://img.shields.io/badge/Status-Production_Ready-success)

## 🌟 Features

- **🤖 Advanced AI Model**: Multimodal transformer (~340K params) combining text (BERT), category, and numeric features
- **🌐 Beautiful Web Interface**: Modern, responsive UI with real-time predictions
- **⚡ Fast Predictions**: Get price estimates in under 3 seconds
- **📊 High Accuracy**: 85%+ accuracy for products in the ₹200–₹25,000 range
- **🎯 Target Products**: Bags & accessories, camera gear, sports equipment, home & kitchen, baby products, books
- **🔌 RESTful API**: Easy integration with existing systems
- **📱 Mobile Responsive**: Works seamlessly on all devices
- **🎯 Confidence Scoring**: Know how reliable each prediction is
- **📈 Price Ranges**: Get upper and lower bounds for predictions
- **⚠️ Scope**: Trained on Amazon India budget/mid-range products — not for premium smartphones or luxury goods

## 🎬 Demo

```bash
# Quick Start
pip install -r requirements_web.txt
python app.py
# Open http://localhost:5000
```

## 📋 Table of Contents

- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Model Details](#-model-details)
- [Dataset](#-dataset)
- [Performance](#-performance)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

## 🏗️ Architecture

### Multimodal Transformer Pipeline

```
Product Input
     │
     ├─► Text Description ──► BERT Encoder ──► 768→128 dim
     │
     ├─► Category ──────────► One-Hot Encoding ──► 128 dim
     │
     └─► Numeric Features ──► Normalization ──► 128 dim
           (ratings, reviews, discounts)
                       │
                       ▼
              ┌────────────────────┐
              │   3-Token Sequence │
              │  [Text, Cat, Num]  │
              └──────────┬─────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │   Transformer Encoder          │
        │   • 2 Layers                   │
        │   • 4 Attention Heads          │
        │   • 128 Model Dimension        │
        │   • Positional Encoding        │
        │   • Token Type Embeddings      │
        └──────────────┬─────────────────┘
                       │
                       ▼
        ┌────────────────────────────────┐
        │   Attention Pooling            │
        └──────────────┬─────────────────┘
                       │
                       ▼
        ┌────────────────────────────────┐
        │   Price Regression Head        │
        │   Output: Log Price            │
        └──────────────┬─────────────────┘
                       │
                       ▼
            Predicted Price (₹)
```

### System Flow

```
Frontend (HTML/CSS/JS)
        ↓
Flask API Server (app.py)
        ↓
Prediction Engine (predict.py)
        ↓
Model (transformer.py)
        ↓
Price Prediction + Confidence
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- 4GB+ RAM (8GB recommended)
- Internet connection (first run downloads BERT model)

### Setup

```bash
# Clone the repository
git clone https://github.com/raswanthmalai19/PredictCart--Multimodal-Transformer-Encoder-for-E-Commerce-Dynamic-Pricing.git
cd PredictCart--Multimodal-Transformer-Encoder-for-E-Commerce-Dynamic-Pricing

# Install dependencies
pip install -r requirements_web.txt

# Verify setup
python check_setup.py

# Run the application
python app.py
```

The app will be available at `http://localhost:5000`

### Quick Start with Script

```bash
# Use the automated startup script
bash start_web.sh
```

## 💻 Usage

### Web Interface

1. **Open Browser**: Navigate to `http://localhost:5000`

2. **Enter Product Details**:
   - Product name/description
   - Category (electronics, books, sports, etc.)
   - Rating (0-5 stars)
   - Number of reviews
   - Discount percentage

3. **Get Prediction**: Click "Predict Price"

4. **View Results**:
   - Estimated price
   - Confidence level (0-100%)
   - Expected price range
   - Input summary

### Example Predictions

#### Bags & Accessories
```
Product: Wildcraft 45L Rucksack Backpack with Rain Cover
Category: fashion
Rating: 4.3 ⭐
Reviews: 1800
Discount: 25%

→ Predicted Price: ₹1,500 – ₹2,200
→ Confidence: 90%
```

#### Camera Accessories
```
Product: CP Plus 3MP Full HD Smart Wi-Fi CCTV Camera
Category: electronics
Rating: 3.7 ⭐
Reviews: 95
Discount: 20%

→ Predicted Price: ₹1,800 – ₹3,500
→ Confidence: 90%
```

#### Home & Kitchen
```
Product: Pigeon Favourite Electric Pressure Cooker 3L
Category: home & kitchen
Rating: 4.1 ⭐
Reviews: 3200
Discount: 30%

→ Predicted Price: ₹1,200 – ₹3,000
→ Confidence: 90%
```

#### Sports & Fitness
```
Product: Boldfit Resistance Band Set with Carry Bag
Category: sports
Rating: 4.2 ⭐
Reviews: 500
Discount: 15%

→ Predicted Price: ₹400 – ₹1,100
→ Confidence: 90%
```

> ⚠️ **Note:** The model is trained on budget/mid-range Amazon India products (₹200–₹25,000). It is **not suitable** for premium smartphones, high-end laptops, or luxury items that cost ₹40,000+.

## 🔌 API Documentation

### Predict Price

**Endpoint**: `POST /api/predict`

**Request**:
```json
{
  "product_name": "Wildcraft 45L Rucksack Backpack with Rain Cover",
  "category": "fashion",
  "ratings": 4.3,
  "no_of_ratings": 1800,
  "discount_ratio": 0.25
}
```

**Response**:
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
  }
}
```

### Get Categories

**Endpoint**: `GET /api/categories`

**Response**:
```json
{
  "success": true,
  "categories": ["accessories", "appliances", "books", "electronics", ...]
}
```

### Health Check

**Endpoint**: `GET /api/health`

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## 🧠 Model Details

### Architecture Specifications

- **Model Type**: Multimodal Transformer Encoder
- **Input Dimension**: 128
- **Attention Heads**: 4
- **Encoder Layers**: 2
- **Dropout**: 0.2
- **Total Parameters**: ~340K

### Input Features

1. **Text Embeddings** (768 → 128 dim):
   - Source: BERT (`bert-base-uncased`)
   - CLS token embedding
   - Linear projection to model dimension

2. **Category Encoding** (128 dim):
   - Hash-based encoding
   - 5 supported categories: electronics, books, sports, fashion, home & kitchen

3. **Numeric Features** (128 dim):
   - Product rating (0-5)
   - Log number of ratings
   - Discount ratio (0-1)
   - Popularity (derived metric)

### Training Configuration

- **Loss Function**: Mean Squared Error (MSE)
- **Optimizer**: AdamW (lr=3e-4)
- **Batch Size**: 32
- **Epochs**: 30 (with early stopping)
- **Learning Rate Schedule**: ReduceLROnPlateau

## 📊 Dataset

### Source Data

- **Source**: Real Amazon India product listings (scraped dataset)
- **Categories**: Bags & luggage, camera accessories, sports & fitness, home & kitchen, baby products, books, and more
- **Price Range**: ₹200 – ₹25,000 (budget to mid-range)
- **Features per product**: Name, category, ratings, number of ratings, discount ratio, actual price

### What the Model Knows

| Category | Typical Price Range | Examples |
|----------|--------------------|---------|
| Bags & Luggage | ₹300 – ₹3,000 | Wildcraft backpacks, travel bags |
| Camera Accessories | ₹200 – ₹5,000 | Ring lights, CCTV cameras, lens hoods |
| Sports & Fitness | ₹300 – ₹3,000 | Resistance bands, yoga mats |
| Home & Kitchen | ₹400 – ₹12,000 | Pressure cookers, appliances |
| Baby Products | ₹400 – ₹3,000 | Grooming kits, bath products |
| Books | ₹100 – ₹1,500 | Novels, textbooks |

> ⚠️ The model has **not** been trained on premium smartphones, high-end laptops, luxury fashion, or any product regularly priced above ₹25,000. Predictions for such products will be unreliable.

### Preprocessing

1. Log transformation of prices (log-price regression)
2. Text cleaning and normalization
3. BERT embedding generation (CLS token)
4. Feature normalization
5. Train/Val/Test split

## 📈 Performance

### Metrics

| Metric | Value |
|--------|---------|
| **R² Score** | 0.85+ |
| **Target Price Range** | ₹200 – ₹25,000 |
| **Best Categories** | Bags, camera accessories, sports, home & kitchen |
| **Confidence (typical products)** | 90% |

### Confidence Levels

- **90%**: Products in the ₹500–₹50,000 range
- **75%**: Products in the ₹100–₹500 or ₹50,000–₹1,00,000 range
- **60%**: Extreme values or out-of-distribution products

## 📁 Project Structure

```
PredictCart/
├── 🌐 Frontend
│   ├── templates/
│   │   ├── base.html               # Base layout
│   │   ├── home.html               # Landing page
│   │   ├── predict.html            # Prediction page
│   │   ├── about.html              # About page
│   │   ├── features.html           # Features page
│   │   ├── docs.html               # Documentation
│   │   └── api_docs.html           # API reference
│   └── static/
│       ├── css/style.css           # Styling
│       └── js/app.js               # Client-side logic
│
├── 🔧 Backend
│   ├── app.py                      # Flask server
│   ├── predict.py                  # Prediction engine
│   ├── transformer.py              # Model architecture
│   └── config.py                   # Configuration
│
├── 🧠 Model & Data
│   ├── simple_models/
│   │   └── best_model.pth          # Trained weights
│   └── Transformer_Ready_Input/
│       ├── prepared_tokens.pkl     # Processed data
│       └── transform_info.pkl      # Feature transforms
│
├── 📊 Training
│   ├── main.py                     # Training script
│   ├── dataloader.py               # Data loading
│   ├── evaluate.py                 # Evaluation
│   └── *.ipynb                     # Jupyter notebooks
│
├── 📚 Documentation
│   ├── README.md                   # This file
│   ├── README_WEB.md               # Web app docs
│   ├── QUICKSTART.md               # Quick guide
│   └── PROJECT_SUMMARY.md          # Overview
│
└── 🛠️ Utilities
    ├── check_setup.py              # Setup validator
    ├── start_web.sh                # Startup script
    └── requirements_web.txt        # Dependencies
```

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker
```bash
docker build -t predictcart .
docker run -p 5000:5000 predictcart
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
MODEL_CONFIG = {
    'd_model': 128,
    'nhead': 4,
    'num_layers': 2,
    'dropout': 0.2
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PyTorch** - Deep learning framework
- **Hugging Face** - Transformers library
- **Flask** - Web framework
- **BERT** - Text embeddings

## 📧 Contact

**Raswanth Malaisamy** - [@raswanthmalai19](https://github.com/raswanthmalai19)

**Project Link**: [https://github.com/raswanthmalai19/PredictCart--Multimodal-Transformer-Encoder-for-E-Commerce-Dynamic-Pricing](https://github.com/raswanthmalai19/PredictCart--Multimodal-Transformer-Encoder-for-E-Commerce-Dynamic-Pricing)

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ using PyTorch, Transformers, and Flask

</div>
