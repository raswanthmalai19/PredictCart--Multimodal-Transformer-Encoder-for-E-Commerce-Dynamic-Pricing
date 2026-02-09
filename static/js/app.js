// E-Commerce Price Predictor - Frontend JavaScript

// DOM Elements
const form = document.getElementById('predictionForm');
const submitBtn = document.getElementById('submitBtn');
const discountSlider = document.getElementById('discountRatio');
const discountValue = document.getElementById('discountValue');
const ratingsInput = document.getElementById('ratings');
const ratingStars = document.getElementById('ratingStars');

// Results elements
const placeholderState = document.getElementById('placeholderState');
const loadingState = document.getElementById('loadingState');
const resultsContent = document.getElementById('resultsContent');
const errorState = document.getElementById('errorState');

// Update discount value display
discountSlider.addEventListener('input', (e) => {
    const value = e.target.value;
    discountValue.textContent = `${value}%`;
});

// Update rating stars display
ratingsInput.addEventListener('input', (e) => {
    const value = parseFloat(e.target.value);
    updateRatingStars(value);
});

function updateRatingStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    
    let stars = '⭐'.repeat(fullStars);
    if (hasHalfStar && fullStars < 5) {
        stars += '⭐';
    }
    
    ratingStars.textContent = stars || '☆';
}

// Show/hide states
function showState(state) {
    placeholderState.classList.add('hidden');
    loadingState.classList.add('hidden');
    resultsContent.classList.add('hidden');
    errorState.classList.add('hidden');
    
    state.classList.remove('hidden');
}

// Format currency
function formatCurrency(value) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 2
    }).format(value);
}

// Format number
function formatNumber(value) {
    return new Intl.NumberFormat('en-IN').format(value);
}

// Reset results
function resetResults() {
    showState(placeholderState);
}

// Display error
function displayError(message) {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    showState(errorState);
}

// Display results
function displayResults(data) {
    const { prediction, input } = data;
    
    // Update price display
    document.getElementById('predictedPrice').textContent = prediction.price_formatted;
    
    // Update confidence
    const confidencePercent = prediction.confidence;
    document.getElementById('confidenceValue').textContent = `${confidencePercent}%`;
    document.getElementById('confidenceFill').style.width = `${confidencePercent}%`;
    
    // Update price range
    document.getElementById('priceLower').textContent = prediction.price_range.lower_formatted;
    document.getElementById('priceUpper').textContent = prediction.price_range.upper_formatted;
    
    // Update details
    document.getElementById('detailProduct').textContent = input.product_name;
    document.getElementById('detailCategory').textContent = input.category.charAt(0).toUpperCase() + input.category.slice(1);
    document.getElementById('detailRating').textContent = `${input.ratings} ⭐`;
    document.getElementById('detailReviews').textContent = formatNumber(input.no_of_ratings);
    
    // Show results
    showState(resultsContent);
}

// Handle form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(form);
    const data = {
        product_name: formData.get('product_name').trim(),
        category: formData.get('category').trim(),
        ratings: parseFloat(formData.get('ratings')),
        no_of_ratings: parseInt(formData.get('no_of_ratings')),
        discount_ratio: parseFloat(formData.get('discount_ratio')) / 100.0  // Convert to 0-1 range
    };
    
    // Validate inputs
    if (!data.product_name) {
        displayError('Please enter a product name');
        return;
    }
    
    if (!data.category) {
        displayError('Please select a category');
        return;
    }
    
    if (data.ratings < 0 || data.ratings > 5) {
        displayError('Rating must be between 0 and 5');
        return;
    }
    
    if (data.no_of_ratings < 0) {
        displayError('Number of ratings must be positive');
        return;
    }
    
    // Show loading state
    showState(loadingState);
    submitBtn.disabled = true;
    
    try {
        // Make API request
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Display results
            displayResults(result);
        } else {
            // Display error
            displayError(result.error || 'Prediction failed. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        displayError('Network error. Please check your connection and try again.');
    } finally {
        submitBtn.disabled = false;
    }
});

// Sample products for quick testing
const sampleProducts = [
    {
        name: 'Samsung Galaxy S21 Ultra 5G',
        category: 'electronics',
        ratings: 4.5,
        no_of_ratings: 2500,
        discount_ratio: 15
    },
    {
        name: 'Nike Air Zoom Pegasus Running Shoes',
        category: 'sports',
        ratings: 4.3,
        no_of_ratings: 850,
        discount_ratio: 25
    },
    {
        name: 'Harry Potter Complete Collection',
        category: 'books',
        ratings: 4.8,
        no_of_ratings: 5000,
        discount_ratio: 30
    }
];

// Add quick fill function (for testing - can be removed in production)
window.fillSample = function(index = 0) {
    const sample = sampleProducts[index];
    document.getElementById('productName').value = sample.name;
    document.getElementById('category').value = sample.category;
    document.getElementById('ratings').value = sample.ratings;
    document.getElementById('noOfRatings').value = sample.no_of_ratings;
    document.getElementById('discountRatio').value = sample.discount_ratio;
    
    updateRatingStars(sample.ratings);
    discountValue.textContent = `${sample.discount_ratio}%`;
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Price Predictor initialized');
    updateRatingStars(4.0);
});

// Keyboard shortcuts (optional - for developer convenience)
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to submit
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        form.dispatchEvent(new Event('submit'));
    }
    
    // Ctrl/Cmd + 1/2/3 to fill samples (for testing)
    if ((e.ctrlKey || e.metaKey) && ['1', '2', '3'].includes(e.key)) {
        const index = parseInt(e.key) - 1;
        fillSample(index);
    }
});

// Export resetResults for global access
window.resetResults = resetResults;
