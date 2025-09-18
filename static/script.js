// Secure NetVoid Website JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Get CSRF token
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
    
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Navbar background on scroll
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(10, 10, 10, 0.98)';
            } else {
                navbar.style.background = 'rgba(10, 10, 10, 0.95)';
            }
        });
    }

    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });

    // Observe pricing cards
    const pricingCards = document.querySelectorAll('.pricing-card');
    pricingCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });

    // Button click animations
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary, .btn-outline');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Create ripple effect
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Add ripple effect CSS
    const style = document.createElement('style');
    style.textContent = `
        .btn-primary, .btn-secondary, .btn-outline {
            position: relative;
            overflow: hidden;
        }
        
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: scale(0);
            animation: ripple-animation 0.6s linear;
            pointer-events: none;
        }
        
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

    // Typing effect for hero title
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        const text = heroTitle.textContent;
        heroTitle.textContent = '';
        
        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                heroTitle.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        };
        
        // Start typing effect after a short delay
        setTimeout(typeWriter, 500);
    }

    // Counter animation for pricing
    const animateCounter = (element, target, duration = 2000) => {
        let start = 0;
        const increment = target / (duration / 16);
        
        const timer = setInterval(() => {
            start += increment;
            element.textContent = Math.floor(start);
            
            if (start >= target) {
                element.textContent = target;
                clearInterval(timer);
            }
        }, 16);
    };

    // Animate counters when pricing section is visible
    const pricingSection = document.querySelector('.pricing');
    if (pricingSection) {
        const pricingObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const amounts = entry.target.querySelectorAll('.amount');
                    amounts.forEach(amount => {
                        const value = parseInt(amount.textContent);
                        animateCounter(amount, value);
                    });
                    pricingObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        pricingObserver.observe(pricingSection);
    }

    // Add loading animation
    window.addEventListener('load', function() {
        document.body.classList.add('loaded');
    });

    // Add loading CSS
    const loadingStyle = document.createElement('style');
    loadingStyle.textContent = `
        body {
            opacity: 0;
            transition: opacity 0.5s ease;
        }
        
        body.loaded {
            opacity: 1;
        }
    `;
    document.head.appendChild(loadingStyle);

    // Security: Prevent right-click context menu
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
    });

    // Security: Prevent text selection
    document.addEventListener('selectstart', function(e) {
        e.preventDefault();
    });

    // Security: Prevent drag and drop
    document.addEventListener('dragstart', function(e) {
        e.preventDefault();
    });

    // Security: Prevent F12, Ctrl+Shift+I, etc.
    document.addEventListener('keydown', function(e) {
        // F12
        if (e.keyCode === 123) {
            e.preventDefault();
            return false;
        }
        
        // Ctrl+Shift+I
        if (e.ctrlKey && e.shiftKey && e.keyCode === 73) {
            e.preventDefault();
            return false;
        }
        
        // Ctrl+U
        if (e.ctrlKey && e.keyCode === 85) {
            e.preventDefault();
            return false;
        }
        
        // Ctrl+S
        if (e.ctrlKey && e.keyCode === 83) {
            e.preventDefault();
            return false;
        }
    });

    // Security: Obfuscate sensitive data
    function obfuscateData() {
        const sensitiveElements = document.querySelectorAll('[data-sensitive]');
        sensitiveElements.forEach(element => {
            element.addEventListener('mouseenter', function() {
                this.style.filter = 'blur(5px)';
            });
            element.addEventListener('mouseleave', function() {
                this.style.filter = 'none';
            });
        });
    }
    
    obfuscateData();

    // Security: Add integrity checks
    function addIntegrityChecks() {
        // Check if page has been modified
        const originalTitle = document.title;
        setInterval(() => {
            if (document.title !== originalTitle) {
                console.warn('Page title modified - possible tampering detected');
            }
        }, 1000);
    }
    
    addIntegrityChecks();

    // Security: Encrypt sensitive form data
    function encryptFormData(formData) {
        // Simple XOR encryption for demonstration
        const key = 'NetVoid2024SecretKey!@#';
        let encrypted = '';
        
        for (let i = 0; i < formData.length; i++) {
            encrypted += String.fromCharCode(
                formData.charCodeAt(i) ^ key.charCodeAt(i % key.length)
            );
        }
        
        return btoa(encrypted);
    }

    // Security: Add form validation
    function addFormValidation() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                // Validate CSRF token
                const csrfInput = form.querySelector('input[name="csrf_token"]');
                if (csrfInput && csrfInput.value !== csrfToken) {
                    e.preventDefault();
                    showNotification('Invalid CSRF token', 'error');
                    return false;
                }
                
                // Validate required fields
                const requiredFields = form.querySelectorAll('[required]');
                for (let field of requiredFields) {
                    if (!field.value.trim()) {
                        e.preventDefault();
                        showNotification(`Please fill in ${field.name}`, 'error');
                        field.focus();
                        return false;
                    }
                }
                
                // Validate email format
                const emailFields = form.querySelectorAll('input[type="email"]');
                for (let field of emailFields) {
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (field.value && !emailRegex.test(field.value)) {
                        e.preventDefault();
                        showNotification('Please enter a valid email address', 'error');
                        field.focus();
                        return false;
                    }
                }
            });
        });
    }
    
    addFormValidation();

    // Security: Rate limiting for API calls
    const apiCallLimits = new Map();
    
    function rateLimitApiCall(endpoint, maxCalls = 5, windowMs = 60000) {
        const now = Date.now();
        const key = `${endpoint}_${window.location.hostname}`;
        
        if (!apiCallLimits.has(key)) {
            apiCallLimits.set(key, []);
        }
        
        const calls = apiCallLimits.get(key);
        
        // Remove old calls
        while (calls.length > 0 && calls[0] < now - windowMs) {
            calls.shift();
        }
        
        if (calls.length >= maxCalls) {
            showNotification('Rate limit exceeded. Please try again later.', 'error');
            return false;
        }
        
        calls.push(now);
        return true;
    }

    // Security: Secure API calls
    function secureApiCall(url, options = {}) {
        if (!rateLimitApiCall(url)) {
            return Promise.reject(new Error('Rate limit exceeded'));
        }
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRF-Token': csrfToken
            }
        };
        
        const mergedOptions = { ...defaultOptions, ...options };
        
        return fetch(url, mergedOptions)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                return response.json();
            })
            .catch(error => {
                console.error('API call failed:', error);
                showNotification('Request failed. Please try again.', 'error');
                throw error;
            });
    }

    // Make secure API call available globally
    window.secureApiCall = secureApiCall;

    // Security: Add input sanitization
    function sanitizeInput(input) {
        return input
            .replace(/[<>]/g, '') // Remove potential HTML tags
            .replace(/javascript:/gi, '') // Remove javascript: protocol
            .replace(/on\w+=/gi, '') // Remove event handlers
            .trim();
    }

    // Apply sanitization to all inputs
    const inputs = document.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = sanitizeInput(this.value);
        });
    });

    // Security: Add session timeout
    let sessionTimeout;
    function resetSessionTimeout() {
        clearTimeout(sessionTimeout);
        sessionTimeout = setTimeout(() => {
            showNotification('Session expired. Please refresh the page.', 'warning');
        }, 30 * 60 * 1000); // 30 minutes
    }
    
    // Reset timeout on user activity
    ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'].forEach(event => {
        document.addEventListener(event, resetSessionTimeout, true);
    });
    
    resetSessionTimeout();

    // Security: Add anti-debugging
    let devtools = {open: false, orientation: null};
    setInterval(() => {
        if (window.outerHeight - window.innerHeight > 200 || window.outerWidth - window.innerWidth > 200) {
            if (!devtools.open) {
                devtools.open = true;
                console.clear();
                console.log('%cStop!', 'color: red; font-size: 50px; font-weight: bold;');
                console.log('%cThis is a browser feature intended for developers.', 'color: red; font-size: 16px;');
            }
        }
    }, 500);

    // Global notification function
    window.showNotification = function(message, type = 'info') {
        const existingNotification = document.querySelector('.notification');
        if (existingNotification) {
            existingNotification.remove();
        }

        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 10000;
            animation: slideIn 0.3s ease;
            max-width: 300px;
        `;
        
        if (type === 'error') {
            notification.style.background = 'linear-gradient(135deg, #ff6b6b, #ee5a52)';
        } else if (type === 'success') {
            notification.style.background = 'linear-gradient(135deg, #51cf66, #40c057)';
        } else if (type === 'warning') {
            notification.style.background = 'linear-gradient(135deg, #ffd43b, #fab005)';
        } else {
            notification.style.background = 'linear-gradient(135deg, #667eea, #764ba2)';
        }
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    };
});
