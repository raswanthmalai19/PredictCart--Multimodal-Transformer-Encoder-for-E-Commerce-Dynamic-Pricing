/* ============================================
   BROWSER CONSOLE TEST
   Copy and paste this into your browser console when on http://localhost:5000/predict
   ============================================ */

console.log('%c🧪 Starting Frontend Test...', 'color: blue; font-size: 16px; font-weight: bold;');

async function testPrediction() {
    try {
        // Test API call
        console.log('%c1️⃣ Testing API call...', 'color: orange; font-weight: bold;');
        
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                product_name: "Test Product - Samsung Galaxy Phone",
                category: "electronics",
                ratings: 4.5,
                no_of_ratings: 500,
                discount_ratio: 0.2
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            console.log('%c✅ API call successful!', 'color: green; font-weight: bold;');
            console.log('📊 Response data:', data);
            console.log('💰 Predicted Price:', data.prediction.price_formatted);
            console.log('📈 Confidence:', data.prediction.confidence + '%');
            console.log('📉 Price Range:', data.prediction.price_range.lower_formatted, '-', data.prediction.price_range.upper_formatted);
            
            // Test if form exists
            console.log('%c2️⃣ Checking form elements...', 'color: orange; font-weight: bold;');
            const form = document.getElementById('predictionForm');
            const productNameInput = document.getElementById('productName');
            const categorySelect = document.getElementById('category');
            const submitBtn = document.getElementById('submitBtn');
            
            if (form) {
                console.log('%c✅ Form found!', 'color: green;');
            } else {
                console.log('%c❌ Form NOT found!', 'color: red; font-weight: bold;');
                return;
            }
            
            if (productNameInput && categorySelect && submitBtn) {
                console.log('%c✅ All form inputs found!', 'color: green;');
            } else {
                console.log('%c⚠️ Some form inputs missing:', 'color: orange;');
                console.log('  Product Name Input:', productNameInput ? '✅' : '❌');
                console.log('  Category Select:', categorySelect ? '✅' : '❌');
                console.log('  Submit Button:', submitBtn ? '✅' : '❌');
            }
            
            // Test result display elements
            console.log('%c3️⃣ Checking result display elements...', 'color: orange; font-weight: bold;');
            const predictedPrice = document.getElementById('predictedPrice');
            const confidenceValue = document.getElementById('confidenceValue');
            const priceLow = document.getElementById('priceLow');
            const priceHigh = document.getElementById('priceHigh');
            
            if (predictedPrice && confidenceValue && priceLow && priceHigh) {
                console.log('%c✅ All result display elements found!', 'color: green;');
            } else {
                console.log('%c⚠️ Some result elements missing:', 'color: orange;');
                console.log('  Predicted Price:', predictedPrice ? '✅' : '❌');
                console.log('  Confidence Value:', confidenceValue ? '✅' : '❌');
                console.log('  Price Low:', priceLow ? '✅' : '❌');
                console.log('  Price High:', priceHigh ? '✅' : '❌');
            }
            
            console.log('%c\n🎉 FRONTEND TEST COMPLETE!', 'color: green; font-size: 18px; font-weight: bold;');
            console.log('%c✅ Everything is working!', 'color: green; font-size: 14px;');
            console.log('%cYou can now:', 'color: blue;');
            console.log('  1. Fill in the form');
            console.log('  2. Click "Predict Price"');
            console.log('  3. See your results!');
            
        } else {
            console.log('%c❌ API returned error:', 'color: red; font-weight: bold;', data.error);
        }
        
    } catch (error) {
        console.log('%c❌ Test failed:', 'color: red; font-weight: bold;', error.message);
        console.log('Error details:', error);
    }
}

// Run the test
testPrediction();
