// Purchase page functionality
document.addEventListener('DOMContentLoaded', function() {
    const planOptions = document.querySelectorAll('.plan-option');
    const selectedPlanElement = document.getElementById('selectedPlan');
    const selectedPriceElement = document.getElementById('selectedPrice');
    const totalPriceElement = document.getElementById('totalPrice');
    const paymentForm = document.getElementById('paymentForm');
    const purchaseButton = document.querySelector('.btn-purchase');
    const btnText = document.querySelector('.btn-text');
    const btnLoading = document.querySelector('.btn-loading');

    // Plan data
    const plans = {
        basic: {
            name: 'Basic Access',
            price: '$9.99',
            period: '/month',
            total: '$9.99'
        },
        premium: {
            name: 'Premium Access',
            price: '$19.99',
            period: '/month',
            total: '$19.99'
        },
        lifetime: {
            name: 'Lifetime Access',
            price: '$99.99',
            period: '/one-time',
            total: '$99.99'
        }
    };

    // Update plan selection
    function updatePlanSelection() {
        const selectedPlan = document.querySelector('input[name="plan"]:checked').value;
        const plan = plans[selectedPlan];
        
        selectedPlanElement.textContent = plan.name;
        selectedPriceElement.textContent = plan.price + plan.period;
        totalPriceElement.textContent = plan.total;
    }

    // Add click handlers to plan options
    planOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Remove selected class from all options
            planOptions.forEach(opt => opt.classList.remove('selected'));
            // Add selected class to clicked option
            this.classList.add('selected');
            // Update plan selection
            updatePlanSelection();
        });
    });

    // Add visual feedback for plan selection
    planOptions.forEach(option => {
        const radio = option.querySelector('input[type="radio"]');
        radio.addEventListener('change', function() {
            planOptions.forEach(opt => {
                opt.classList.remove('selected');
                opt.querySelector('.plan-card').classList.remove('selected');
            });
            
            if (this.checked) {
                option.classList.add('selected');
                option.querySelector('.plan-card').classList.add('selected');
            }
        });
    });

    // Initialize with default selection
    updatePlanSelection();

    // Form validation
    function validateForm() {
        const email = document.getElementById('email').value;
        const name = document.getElementById('name').value;
        const terms = document.getElementById('terms').checked;
        
        if (!email || !name || !terms) {
            showNotification('Please fill in all required fields and accept the terms.', 'error');
            return false;
        }
        
        if (!isValidEmail(email)) {
            showNotification('Please enter a valid email address.', 'error');
            return false;
        }
        
        return true;
    }

    // Email validation
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Show notification
    function showNotification(message, type = 'info') {
        // Remove existing notifications
        const existingNotification = document.querySelector('.notification');
        if (existingNotification) {
            existingNotification.remove();
        }

        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Add styles
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
        } else {
            notification.style.background = 'linear-gradient(135deg, #667eea, #764ba2)';
        }
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }

    // Add CSS for notifications
    const notificationStyle = document.createElement('style');
    notificationStyle.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(notificationStyle);

    // Form submission
    paymentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (!validateForm()) {
            return;
        }
        
        // Show loading state
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline';
        purchaseButton.disabled = true;
        
        // Simulate payment processing
        setTimeout(() => {
            // Get form data
            const formData = new FormData(paymentForm);
            const selectedPlan = document.querySelector('input[name="plan"]:checked').value;
            const paymentMethod = document.querySelector('input[name="payment"]:checked').value;
            
            // Simulate successful payment
            showNotification('Payment successful! Your key will be delivered via email.', 'success');
            
            // Generate a mock key (in real implementation, this would come from your server)
            const mockKey = generateMockKey();
            
            // Show success modal
            showSuccessModal(mockKey, selectedPlan);
            
            // Reset form
            btnText.style.display = 'inline';
            btnLoading.style.display = 'none';
            purchaseButton.disabled = false;
            
        }, 2000);
    });

    // Generate mock key
    function generateMockKey() {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                result += chars.charAt(Math.floor(Math.random() * chars.length));
            }
            if (i < 3) result += '-';
        }
        return result;
    }

    // Show success modal
    function showSuccessModal(key, plan) {
        const modal = document.createElement('div');
        modal.className = 'success-modal';
        modal.innerHTML = `
            <div class="modal-overlay">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>🎉 Purchase Successful!</h2>
                        <button class="modal-close">&times;</button>
                    </div>
                    <div class="modal-body">
                        <p>Your NetVoid key has been generated and will be sent to your email.</p>
                        <div class="key-display">
                            <label>Your Access Key:</label>
                            <div class="key-container">
                                <input type="text" value="${key}" readonly class="key-input">
                                <button class="copy-btn" onclick="copyToClipboard('${key}')">Copy</button>
                            </div>
                        </div>
                        <div class="next-steps">
                            <h3>Next Steps:</h3>
                            <ol>
                                <li>Download the NetVoid client</li>
                                <li>Run the application</li>
                                <li>Enter your key when prompted</li>
                                <li>Enjoy your premium features!</li>
                            </ol>
                        </div>
                        <div class="modal-actions">
                            <button class="btn-primary" onclick="downloadClient()">Download Client</button>
                            <button class="btn-secondary" onclick="closeModal()">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Close modal handlers
        modal.querySelector('.modal-close').addEventListener('click', closeModal);
        modal.querySelector('.modal-overlay').addEventListener('click', function(e) {
            if (e.target === this) closeModal();
        });
        
        function closeModal() {
            modal.remove();
        }
        
        // Make functions global for onclick handlers
        window.copyToClipboard = function(text) {
            navigator.clipboard.writeText(text).then(() => {
                showNotification('Key copied to clipboard!', 'success');
            });
        };
        
        window.downloadClient = function() {
            showNotification('Client download started!', 'success');
            // In real implementation, this would trigger actual download
        };
        
        window.closeModal = closeModal;
    }

    // Add CSS for success modal
    const modalStyle = document.createElement('style');
    modalStyle.textContent = `
        .success-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 10000;
        }
        
        .modal-overlay {
            background: rgba(0, 0, 0, 0.8);
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .modal-content {
            background: #1a1a2e;
            border-radius: 16px;
            border: 1px solid #333;
            max-width: 500px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
        }
        
        .modal-header {
            padding: 20px 30px;
            border-bottom: 1px solid #333;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .modal-header h2 {
            color: #ffffff;
            margin: 0;
        }
        
        .modal-close {
            background: none;
            border: none;
            color: #cccccc;
            font-size: 24px;
            cursor: pointer;
            padding: 0;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .modal-body {
            padding: 30px;
        }
        
        .key-display {
            margin: 20px 0;
        }
        
        .key-display label {
            display: block;
            color: #cccccc;
            margin-bottom: 10px;
            font-weight: 500;
        }
        
        .key-container {
            display: flex;
            gap: 10px;
        }
        
        .key-input {
            flex: 1;
            padding: 12px;
            background: #0a0a0a;
            border: 1px solid #333;
            border-radius: 8px;
            color: #ffffff;
            font-family: monospace;
            font-size: 14px;
        }
        
        .copy-btn {
            padding: 12px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
        }
        
        .next-steps {
            margin: 20px 0;
        }
        
        .next-steps h3 {
            color: #ffffff;
            margin-bottom: 10px;
        }
        
        .next-steps ol {
            color: #cccccc;
            padding-left: 20px;
        }
        
        .next-steps li {
            margin-bottom: 5px;
        }
        
        .modal-actions {
            display: flex;
            gap: 15px;
            margin-top: 30px;
        }
        
        .modal-actions .btn-primary,
        .modal-actions .btn-secondary {
            flex: 1;
            padding: 12px 20px;
            border-radius: 8px;
            text-decoration: none;
            text-align: center;
            font-weight: 500;
            cursor: pointer;
            border: none;
        }
        
        .modal-actions .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .modal-actions .btn-secondary {
            background: transparent;
            color: #cccccc;
            border: 1px solid #333;
        }
    `;
    document.head.appendChild(modalStyle);

    // Add additional CSS for purchase page
    const purchaseStyle = document.createElement('style');
    purchaseStyle.textContent = `
        .purchase-section {
            padding: 120px 0 80px;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
            min-height: 100vh;
        }
        
        .purchase-container {
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .purchase-header {
            text-align: center;
            margin-bottom: 60px;
        }
        
        .purchase-header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 20px;
            color: #ffffff;
        }
        
        .purchase-header p {
            font-size: 1.2rem;
            color: #cccccc;
        }
        
        .purchase-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            margin-bottom: 60px;
        }
        
        .plan-selection h2,
        .payment-section h2 {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 30px;
            color: #ffffff;
        }
        
        .plan-options {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .plan-option {
            position: relative;
        }
        
        .plan-option input[type="radio"] {
            position: absolute;
            opacity: 0;
            pointer-events: none;
        }
        
        .plan-option label {
            cursor: pointer;
            display: block;
        }
        
        .plan-card {
            background: #0a0a0a;
            border: 2px solid #333;
            border-radius: 12px;
            padding: 25px;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .plan-card:hover {
            border-color: #667eea;
            transform: translateY(-2px);
        }
        
        .plan-card.selected {
            border-color: #667eea;
            background: rgba(102, 126, 234, 0.1);
        }
        
        .plan-badge {
            position: absolute;
            top: -10px;
            right: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: 600;
        }
        
        .plan-card h3 {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 15px;
            color: #ffffff;
        }
        
        .plan-price {
            margin-bottom: 20px;
        }
        
        .plan-price .currency {
            font-size: 1.2rem;
            color: #cccccc;
        }
        
        .plan-price .amount {
            font-size: 2rem;
            font-weight: 700;
            color: #ffffff;
        }
        
        .plan-price .period {
            font-size: 1rem;
            color: #cccccc;
        }
        
        .plan-features {
            list-style: none;
        }
        
        .plan-features li {
            padding: 5px 0;
            color: #cccccc;
            font-size: 0.95rem;
        }
        
        .payment-form {
            background: #0a0a0a;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 30px;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        .form-group label {
            display: block;
            color: #ffffff;
            font-weight: 500;
            margin-bottom: 8px;
        }
        
        .form-group input {
            width: 100%;
            padding: 12px 15px;
            background: #1a1a2e;
            border: 1px solid #333;
            border-radius: 8px;
            color: #ffffff;
            font-size: 1rem;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .payment-methods {
            margin: 30px 0;
        }
        
        .payment-methods h3 {
            color: #ffffff;
            margin-bottom: 15px;
            font-size: 1.1rem;
        }
        
        .payment-options {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
        }
        
        .payment-option input[type="radio"] {
            position: absolute;
            opacity: 0;
            pointer-events: none;
        }
        
        .payment-option label {
            cursor: pointer;
            display: block;
        }
        
        .payment-card {
            background: #1a1a2e;
            border: 2px solid #333;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .payment-card:hover {
            border-color: #667eea;
        }
        
        .payment-option input:checked + label .payment-card {
            border-color: #667eea;
            background: rgba(102, 126, 234, 0.1);
        }
        
        .payment-icon {
            font-size: 1.5rem;
            margin-bottom: 8px;
        }
        
        .payment-card span {
            color: #ffffff;
            font-weight: 500;
            font-size: 0.9rem;
        }
        
        .terms-section {
            margin: 25px 0;
        }
        
        .terms-checkbox {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            cursor: pointer;
            color: #cccccc;
            font-size: 0.95rem;
            line-height: 1.4;
        }
        
        .terms-checkbox input[type="checkbox"] {
            margin: 0;
            width: 18px;
            height: 18px;
            accent-color: #667eea;
        }
        
        .terms-link {
            color: #667eea;
            text-decoration: none;
        }
        
        .terms-link:hover {
            text-decoration: underline;
        }
        
        .purchase-summary {
            background: #1a1a2e;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 20px;
            margin: 25px 0;
        }
        
        .summary-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            color: #cccccc;
        }
        
        .summary-total {
            display: flex;
            justify-content: space-between;
            font-weight: 600;
            font-size: 1.1rem;
            color: #ffffff;
            padding-top: 10px;
            border-top: 1px solid #333;
        }
        
        .btn-purchase {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 16px;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn-purchase:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        
        .btn-purchase:disabled {
            opacity: 0.7;
            cursor: not-allowed;
        }
        
        .security-features {
            text-align: center;
            background: #0a0a0a;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 30px;
        }
        
        .security-features h3 {
            color: #ffffff;
            margin-bottom: 20px;
            font-size: 1.2rem;
        }
        
        .security-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
        }
        
        .security-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
            color: #cccccc;
        }
        
        .security-icon {
            font-size: 1.5rem;
        }
        
        @media (max-width: 768px) {
            .purchase-content {
                grid-template-columns: 1fr;
                gap: 40px;
            }
            
            .plan-options {
                gap: 15px;
            }
            
            .payment-options {
                grid-template-columns: 1fr;
            }
        }
    `;
    document.head.appendChild(purchaseStyle);
});
