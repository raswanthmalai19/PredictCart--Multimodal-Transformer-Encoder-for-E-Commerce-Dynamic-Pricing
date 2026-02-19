# 🚀 Quick Start Guide - E-Commerce Price Predictor

## ⚡ 3-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements_web.txt
```

### Step 2: Check Setup
```bash
python check_setup.py
```

### Step 3: Run Application
```bash
python app.py
```

### Step 4: Open Browser
Navigate to: **http://localhost:5000**

---

## 📱 Using the Web Interface

### Input a Product

1. **Product Name**: Enter a detailed product description
   - Example: "Wildcraft 45L Rucksack Backpack with Rain Cover Olive Green"
   - Best for: bags, camera accessories, sports gear, home & kitchen, baby products (₹200–₹25,000)

2. **Category**: Select from dropdown
   - Electronics, Books, Sports, Fashion, etc.

3. **Rating**: Set product rating (0-5 stars)
   - Default: 4.0 ⭐

4. **Number of Reviews**: Enter review count
   - Default: 100

5. **Discount**: Slide to set discount percentage
   - Range: 0% - 100%

### Get Prediction

Click **"Predict Price"** button

### View Results

- **Estimated Price**: Main price prediction
- **Confidence Level**: Prediction accuracy (0-100%)
- **Price Range**: Lower and upper bounds
- **Input Summary**: Your entered details

---

## 🎯 Example Predictions

> ⚠️ The model is trained on Amazon India budget/mid-range products (₹200–₹25,000).
> Best results with bags, camera accessories, sports gear, home & kitchen, and baby products.
> **Not suitable for premium smartphones or laptops costing ₹40,000+.**

### Example 1: Bags & Accessories
```
Product: Wildcraft 45L Rucksack Backpack with Rain Cover
Category: fashion
Rating: 4.3 ⭐
Reviews: 1800
Discount: 25%

Result: ~₹1,900
```

### Example 2: Camera Accessories
```
Product: CP Plus 3MP Full HD Smart Wi-Fi CCTV Camera
Category: electronics
Rating: 3.7 ⭐
Reviews: 95
Discount: 20%

Result: ~₹2,500
```

### Example 3: Home & Kitchen
```
Product: Pigeon Favourite Electric Pressure Cooker 3 Litre
Category: home & kitchen
Rating: 4.1 ⭐
Reviews: 3200
Discount: 30%

Result: ~₹1,500
```

### Example 4: Sports & Fitness
```
Product: Boldfit Resistance Band Set with Handles and Carry Bag
Category: sports
Rating: 4.2 ⭐
Reviews: 500
Discount: 15%

Result: ~₹700
```

---

## 🔧 Keyboard Shortcuts

- **Ctrl/Cmd + Enter**: Submit form
- **Ctrl/Cmd + 1/2/3**: Fill sample products (for testing)

---

## 🌐 API Usage

### Predict Price Endpoint

**POST** `/api/predict`

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Wildcraft 45L Rucksack Backpack with Rain Cover",
    "category": "fashion",
    "ratings": 4.3,
    "no_of_ratings": 1800,
    "discount_ratio": 0.25
  }'
```

### Get Categories

**GET** `/api/categories`

```bash
curl http://localhost:5000/api/categories
```

### Health Check

**GET** `/api/health`

```bash
curl http://localhost:5000/api/health
```

---

## 🐛 Troubleshooting

### "Model not loaded" Error
```bash
# Check if model file exists
ls -lh simple_models/best_model.pth

# Verify paths in config.py
cat config.py | grep PATH
```

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use different port
python app.py --port 5001
```

### BERT Model Download Issues
```bash
# Ensure internet connection
# BERT downloads ~500MB on first run
# Cached in: ~/.cache/huggingface/

# Check cache
ls -lh ~/.cache/huggingface/hub/
```

### Memory Issues
```bash
# Check available memory
free -h  # Linux
vm_stat  # macOS

# Close other applications
# Minimum 4GB RAM recommended
```

---

## 📊 Understanding Predictions

### Confidence Levels

- **90-100%**: High confidence - typical products
- **75-89%**: Good confidence - some uncertainty
- **60-74%**: Moderate confidence - unusual specs
- **<60%**: Low confidence - extreme outliers

### Price Ranges

The system provides ±15% range around predicted price:
- **Lower Bound**: Predicted × 0.85
- **Upper Bound**: Predicted × 1.15

---

## 🎨 Customization

### Change Theme Colors
Edit `static/css/style.css`:
```css
:root {
    --primary: #6366f1;  /* Main color */
    --secondary: #10b981;  /* Accent color */
}
```

### Add New Categories
Edit category encoder in `predict.py` or retrain model with new categories.

### Adjust Model Settings
Edit `config.py`:
```python
MODEL_CONFIG = {
    'd_model': 128,
    'nhead': 4,
    'num_layers': 2,
    'dropout': 0.2
}
```

---

## 📈 Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker
```bash
docker build -t price-predictor .
docker run -p 5000:5000 price-predictor
```

### Environment Variables
```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
export MODEL_PATH=/path/to/model.pth
```

---

## 📚 Additional Resources

- **Full Documentation**: README_WEB.md
- **Model Architecture**: transformer.py
- **API Reference**: app.py
- **Training Code**: main.py

---

## 💡 Tips

1. **More Reviews = Better Predictions**
   - Products with 100+ reviews get better estimates

2. **Detailed Names Help**
   - Include brand, model, specs in product name

3. **Check Multiple Categories**
   - Same product in different categories may vary

4. **Discount Affects Price**
   - Higher discount = Lower predicted price

5. **Rating Matters**
   - Higher rated products often cost more

---

## 🆘 Need Help?

1. Run setup check:
   ```bash
   python check_setup.py
   ```

2. Check logs in terminal

3. Verify all files are present

4. Ensure Python 3.8+ installed

5. Review README_WEB.md for details

---

**Ready to predict prices? Let's go! 🚀**
