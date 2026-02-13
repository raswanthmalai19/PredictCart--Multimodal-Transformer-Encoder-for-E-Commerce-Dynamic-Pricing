/* ============================================
   PredictCart — Professional JavaScript
   Single clean initialization
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initMobileMenu();
    initSmoothScroll();
    initCodeCopy();
    initScrollReveal();
    initBackToTop();

    // Predict-page specific
    if (document.getElementById('predictionForm')) {
        initSlider();
        initRating();
        initForm();
        checkModelStatus();
        addFieldAnimations();
    }
});

/* ============================================
   NAVBAR
   ============================================ */
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY;
        if (scrollY > 20) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        lastScroll = scrollY;
    }, { passive: true });
}

/* ============================================
   MOBILE MENU
   ============================================ */
function initMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const overlay = document.querySelector('.mobile-menu-overlay');
    const closeBtn = document.querySelector('.mobile-close');
    if (!hamburger || !overlay) return;

    function open() {
        hamburger.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
    function close() {
        hamburger.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    hamburger.addEventListener('click', open);
    if (closeBtn) closeBtn.addEventListener('click', close);
    overlay.addEventListener('click', (e) => { if (e.target === overlay) close(); });

    overlay.querySelectorAll('.mobile-link').forEach(link => {
        link.addEventListener('click', close);
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && overlay.classList.contains('active')) close();
    });
}

/* ============================================
   SMOOTH SCROLL
   ============================================ */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            const id = anchor.getAttribute('href');
            if (id === '#') return;
            const target = document.querySelector(id);
            if (!target) return;
            e.preventDefault();
            const offset = 80;
            const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
            window.scrollTo({ top, behavior: 'smooth' });
        });
    });
}

/* ============================================
   CODE COPY
   ============================================ */
function initCodeCopy() {
    document.querySelectorAll('.code-copy').forEach(btn => {
        btn.addEventListener('click', () => {
            const block = btn.closest('.code-block');
            const code = block.querySelector('code');
            if (!code) return;
            const text = code.textContent;
            navigator.clipboard.writeText(text).then(() => {
                const orig = btn.textContent;
                btn.textContent = 'Copied!';
                setTimeout(() => { btn.textContent = orig; }, 2000);
            });
        });
    });
}

/* ============================================
   SCROLL REVEAL
   ============================================ */
function initScrollReveal() {
    const targets = document.querySelectorAll(
        '.feature-card, .feature-detail-card, .process-step, .tech-card, .stat, .arch-card, .stat-box'
    );
    if (!targets.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, i) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, i * 60);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    targets.forEach(el => observer.observe(el));
}

/* ============================================
   BACK TO TOP
   ============================================ */
function initBackToTop() {
    const btn = document.createElement('button');
    btn.className = 'back-to-top';
    btn.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 15l-6-6-6 6"/></svg>`;
    btn.setAttribute('aria-label', 'Back to top');
    document.body.appendChild(btn);

    window.addEventListener('scroll', () => {
        if (window.scrollY > 400) {
            btn.classList.add('visible');
        } else {
            btn.classList.remove('visible');
        }
    }, { passive: true });

    btn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

/* ============================================
   SLIDER (discount)
   ============================================ */
function initSlider() {
    const slider = document.getElementById('discountRatio');
    const fill = document.getElementById('sliderFill');
    const badge = document.getElementById('discountBadge');
    if (!slider) return;

    function update() {
        const val = parseFloat(slider.value);
        const pct = (val / parseFloat(slider.max)) * 100;
        if (fill) fill.style.width = pct + '%';
        if (badge) badge.textContent = Math.round(val * 100) + '%';
    }
    slider.addEventListener('input', update);
    update();
}

/* ============================================
   STAR RATING
   ============================================ */
function initRating() {
    const input = document.getElementById('ratings');
    const display = document.getElementById('starDisplay');
    const text = document.getElementById('ratingText');
    if (!input || !display) return;

    function render() {
        const val = parseFloat(input.value) || 0;
        const clamped = Math.max(0, Math.min(5, val));
        const fullStars = Math.floor(clamped);
        const hasHalf = clamped % 1 >= 0.25;
        let html = '';
        for (let i = 0; i < 5; i++) {
            if (i < fullStars) {
                html += '<span class="star on">★</span>';
            } else if (i === fullStars && hasHalf) {
                html += '<span class="star half">★</span>';
            } else {
                html += '<span class="star">★</span>';
            }
        }
        display.innerHTML = html;
        if (text) text.textContent = clamped > 0 ? clamped.toFixed(1) : '';
    }
    input.addEventListener('input', render);
    render();
}

/* ============================================
   FIELD ANIMATIONS
   ============================================ */
function addFieldAnimations() {
    document.querySelectorAll('.field-input, .field-select').forEach(el => {
        el.addEventListener('focus', () => {
            el.closest('.field')?.classList.add('focused');
        });
        el.addEventListener('blur', () => {
            el.closest('.field')?.classList.remove('focused');
            if (el.value && el.value.trim()) {
                el.classList.add('filled');
            } else {
                el.classList.remove('filled');
            }
        });
    });
}

/* ============================================
   MODEL STATUS
   ============================================ */
function checkModelStatus() {
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.querySelector('.status-text');
    if (!statusDot) return;

    statusDot.className = 'status-dot loading';
    if (statusText) statusText.textContent = 'Connecting...';

    fetch('/api/health')
        .then(res => res.json())
        .then(data => {
            if (data.model_loaded) {
                statusDot.className = 'status-dot ready';
                if (statusText) statusText.textContent = 'Model Ready';
            } else {
                statusDot.className = 'status-dot loading';
                if (statusText) statusText.textContent = 'Loading...';
                setTimeout(checkModelStatus, 5000);
            }
        })
        .catch(() => {
            statusDot.className = 'status-dot error';
            if (statusText) statusText.textContent = 'Offline';
            setTimeout(checkModelStatus, 10000);
        });
}

/* ============================================
   PREDICTION FORM
   ============================================ */
function initForm() {
    const form = document.getElementById('predictionForm');
    const submitBtn = document.getElementById('submitBtn');
    if (!form || !submitBtn) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const productName = document.getElementById('productName').value.trim();
        const category = document.getElementById('category').value;
        const ratings = parseFloat(document.getElementById('ratings').value) || 0;
        const noOfRatings = parseInt(document.getElementById('noOfRatings').value) || 0;
        const discountRatio = parseFloat(document.getElementById('discountRatio').value) || 0;

        if (!productName) {
            showToast('Please enter a product name.', 'error');
            document.getElementById('productName').focus();
            return;
        }
        if (!category) {
            showToast('Please select a category.', 'error');
            document.getElementById('category').focus();
            return;
        }

        showState('loading');

        // Animate loading steps
        const steps = document.querySelectorAll('#loadingState .step');
        animateSteps(steps);

        submitBtn.disabled = true;
        const origText = submitBtn.querySelector('.btn-text');
        if (origText) origText.textContent = 'Analyzing...';

        try {
            const res = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    product_name: productName,
                    category: category,
                    ratings: ratings,
                    no_of_ratings: noOfRatings,
                    discount_ratio: discountRatio
                })
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.error || 'Prediction failed');
            }

            const data = await res.json();

            // Brief pause for step animation feel
            setTimeout(() => {
                displayResults(data, {
                    productName, category, ratings, noOfRatings, discountRatio
                });
                showState('results');
            }, 1200);

        } catch (err) {
            showState('error');
            const errText = document.querySelector('#errorState .error-text');
            if (errText) errText.textContent = err.message || 'Something went wrong.';
        } finally {
            submitBtn.disabled = false;
            if (origText) origText.textContent = 'Predict Price';
        }
    });

    // Reset button
    document.addEventListener('click', (e) => {
        if (e.target.closest('.reset-btn')) {
            form.reset();
            showState('placeholder');
            initSlider();
            initRating();
            document.querySelectorAll('.field-input').forEach(el => el.classList.remove('filled'));
        }
    });
}

/* ============================================
   STATE MANAGEMENT
   ============================================ */
function showState(state) {
    const ids = ['placeholderState', 'loadingState', 'resultsState', 'errorState'];
    ids.forEach(id => {
        const el = document.getElementById(id);
        if (!el) return;
        if (id === state + 'State') {
            el.classList.remove('hidden');
        } else {
            el.classList.add('hidden');
        }
    });
}

/* ============================================
   LOADING STEP ANIMATION
   ============================================ */
function animateSteps(steps) {
    if (!steps.length) return;
    let current = 0;
    const interval = setInterval(() => {
        if (current > 0) {
            steps[current - 1].classList.remove('active');
            steps[current - 1].classList.add('done');
        }
        if (current < steps.length) {
            steps[current].classList.add('active');
            current++;
        } else {
            clearInterval(interval);
        }
    }, 350);
}

/* ============================================
   DISPLAY RESULTS
   ============================================ */
function displayResults(data, inputs) {
    // Price
    const priceEl = document.getElementById('predictedPrice');
    if (priceEl) animateNumber(priceEl, data.predicted_price, '₹');

    // Confidence
    const confValue = document.getElementById('confidenceValue');
    const confFill = document.getElementById('confidenceFill');
    const confHint = document.getElementById('confidenceHint');
    const conf = data.confidence || 0;
    if (confValue) confValue.textContent = conf + '%';
    if (confFill) {
        confFill.style.width = '0%';
        requestAnimationFrame(() => {
            setTimeout(() => { confFill.style.width = conf + '%'; }, 100);
        });
    }
    if (confHint) {
        if (conf >= 80) confHint.textContent = 'High confidence — prediction is reliable.';
        else if (conf >= 50) confHint.textContent = 'Moderate confidence — consider as estimate.';
        else confHint.textContent = 'Low confidence — use as rough guideline.';
    }

    // Range
    const priceLow = document.getElementById('priceLow');
    const priceHigh = document.getElementById('priceHigh');
    const priceMid = document.getElementById('priceMid');
    const low = data.price_range?.low || data.predicted_price * 0.85;
    const high = data.price_range?.high || data.predicted_price * 1.15;

    if (priceLow) priceLow.textContent = formatCurrency(low);
    if (priceHigh) priceHigh.textContent = formatCurrency(high);
    if (priceMid) priceMid.textContent = formatCurrency(data.predicted_price);

    // Summary
    const sumProduct = document.getElementById('sumProduct');
    const sumCategory = document.getElementById('sumCategory');
    const sumRating = document.getElementById('sumReviews');
    const sumReviews = document.getElementById('sumReviews');

    if (sumProduct) sumProduct.textContent = truncate(inputs.productName, 28);
    if (sumCategory) sumCategory.textContent = inputs.category;
    if (document.getElementById('sumRating'))
        document.getElementById('sumRating').textContent = inputs.ratings.toFixed(1) + ' / 5';
    if (sumReviews)
        sumReviews.textContent = inputs.noOfRatings.toLocaleString();
}

/* ============================================
   HELPERS
   ============================================ */
function animateNumber(el, target, prefix = '') {
    const duration = 1200;
    const start = performance.now();
    const from = 0;

    function tick(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = from + (target - from) * eased;
        el.textContent = prefix + formatCurrency(current);
        if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
}

function formatCurrency(value) {
    if (value >= 100000) return (value / 100000).toFixed(2) + 'L';
    if (value >= 1000) return (value / 1000).toFixed(1) + 'K';
    return Math.round(value).toLocaleString('en-IN');
}

function truncate(str, max) {
    if (!str) return '';
    return str.length > max ? str.substring(0, max) + '...' : str;
}

/* ============================================
   TOAST NOTIFICATIONS
   ============================================ */
function showToast(message, type = 'info') {
    let toast = document.querySelector('.toast');
    if (toast) toast.remove();

    toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <span style="flex:1;font-size:0.88rem;color:var(--text)">${message}</span>
        <button class="toast-close" onclick="this.parentElement.classList.remove('show');setTimeout(()=>this.parentElement.remove(),300)">&times;</button>
    `;
    document.body.appendChild(toast);
    requestAnimationFrame(() => {
        requestAnimationFrame(() => { toast.classList.add('show'); });
    });
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}
