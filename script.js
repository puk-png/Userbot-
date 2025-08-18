class DashboardManager {
    constructor() {
        this.updateInterval = null;
        this.startTime = Date.now();
        this.init();
    }

    init() {
        console.log('Initializing Telegram Userbot Dashboard...');
        this.startStatusUpdates();
        this.bindEvents();
    }

    bindEvents() {
        // Auto-refresh every 5 seconds
        this.updateInterval = setInterval(() => {
            this.updateStatus();
        }, 5000);

        // Clear error button
        window.clearError = () => {
            this.clearError();
        };

        // Cleanup on page unload
        window.addEventListener('beforeunload', () => {
            if (this.updateInterval) {
                clearInterval(this.updateInterval);
            }
        });
    }

    async updateStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();

            if (data.error) {
                this.updateStatusIndicator(false, 'Помилка підключення');
                console.error('Bot status error:', data.error);
                return;
            }

            // Update status indicator
            this.updateStatusIndicator(data.is_running, data.is_running ? 'Онлайн' : 'Офлайн');

            // Update statistics
            this.updateStatistics(data);

            // Update uptime
            this.updateUptime(data.uptime);

            // Show error if exists
            if (data.last_error) {
                this.showError(data.last_error);
            } else {
                this.hideError();
            }

        } catch (error) {
            console.error('Failed to fetch status:', error);
            this.updateStatusIndicator(false, 'Немає зв\'язку');
        }
    }

    updateStatusIndicator(isOnline, statusText) {
        const indicator = document.getElementById('statusIndicator');
        const text = document.getElementById('statusText');

        if (indicator && text) {
            indicator.className = `status-indicator ${isOnline ? 'online' : 'offline'}`;
            text.textContent = statusText;
            
            // Add fade-in animation
            text.classList.add('fade-in');
            setTimeout(() => text.classList.remove('fade-in'), 500);
        }
    }

    updateStatistics(data) {
        const stats = {
            'commandsCount': data.commands_processed || 0,
            'reactionsCount': data.reactions_sent || 0,
            'messagesCount': data.messages_processed || 0
        };

        Object.entries(stats).forEach(([elementId, value]) => {
            const element = document.getElementById(elementId);
            if (element) {
                const currentValue = parseInt(element.textContent) || 0;
                if (currentValue !== value) {
                    this.animateNumber(element, currentValue, value);
                }
            }
        });
    }

    animateNumber(element, from, to) {
        const duration = 1000; // 1 second
        const steps = 30;
        const stepValue = (to - from) / steps;
        const stepDuration = duration / steps;
        
        let current = from;
        let step = 0;

        const animate = () => {
            if (step < steps) {
                current += stepValue;
                element.textContent = Math.round(current);
                step++;
                setTimeout(animate, stepDuration);
            } else {
                element.textContent = to;
            }
        };

        animate();
    }

    updateUptime(uptimeSeconds) {
        const uptimeElement = document.getElementById('uptime');
        if (uptimeElement && uptimeSeconds > 0) {
            const hours = Math.floor(uptimeSeconds / 3600);
            const minutes = Math.floor((uptimeSeconds % 3600) / 60);
            const seconds = Math.floor(uptimeSeconds % 60);
            
            const timeString = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            uptimeElement.textContent = timeString;
        }
    }

    showError(errorMessage) {
        const errorContainer = document.getElementById('errorContainer');
        const errorText = document.getElementById('errorText');
        
        if (errorContainer && errorText) {
            errorText.textContent = errorMessage;
            errorContainer.style.display = 'block';
            errorContainer.classList.add('fade-in');
        }
    }

    hideError() {
        const errorContainer = document.getElementById('errorContainer');
        if (errorContainer) {
            errorContainer.style.display = 'none';
        }
    }

    async clearError() {
        try {
            await fetch('/api/clear_error');
            this.hideError();
        } catch (error) {
            console.error('Failed to clear error:', error);
        }
    }

    startStatusUpdates() {
        console.log('Starting status updates...');
        this.updateStatus(); // Initial update
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new DashboardManager();
});

// Add some visual feedback for user interactions
document.addEventListener('click', (e) => {
    // Add ripple effect to buttons and cards
    if (e.target.matches('.btn, .card, .stat-card')) {
        const ripple = document.createElement('div');
        ripple.style.position = 'absolute';
        ripple.style.borderRadius = '50%';
        ripple.style.background = 'rgba(255, 255, 255, 0.6)';
        ripple.style.transform = 'scale(0)';
        ripple.style.animation = 'ripple 0.6s linear';
        ripple.style.pointerEvents = 'none';
        
        const rect = e.target.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
        ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
        
        e.target.style.position = 'relative';
        e.target.style.overflow = 'hidden';
        e.target.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }
});

// Add ripple animation to CSS if not already present
if (!document.querySelector('style[data-ripple]')) {
    const style = document.createElement('style');
    style.setAttribute('data-ripple', 'true');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}
