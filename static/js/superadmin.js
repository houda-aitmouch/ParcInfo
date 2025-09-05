// dashboard.js

/**
 * Configuration globale du dashboard
 */
const DashboardConfig = {
    animationDuration: 300,
    debounceDelay: 250,
    apiEndpoints: {
        stats: '/api/dashboard/stats/',
        notifications: '/api/notifications/'
    },
    theme: {
        primary: '#2563eb',
        secondary: '#64748b',
        success: '#10b981',
        warning: '#f59e0b',
        error: '#ef4444'
    }
};

/**
 * Classe principale du Dashboard
 */
class Dashboard {
    constructor() {
        this.init();
        this.bindEvents();
        this.loadStats();
        this.initializeAnimations();
    }

    /**
     * Initialisation du dashboard
     */
    init() {
        console.log('🚀 Dashboard initialization started');

        // Vérification de la compatibilité Alpine.js
        if (typeof Alpine !== 'undefined') {
            console.log('✅ Alpine.js is loaded');
        }

        // Configuration des données globales Alpine
        document.addEventListener('alpine:init', () => {
            Alpine.data('dashboard', () => ({
                loading: false,
                stats: {
                    equipements: '--',
                    materiels: '--',
                    fournisseurs: '--'
                },
                notifications: [],
                showNotifications: false,

                // Méthodes Alpine
                toggleNotifications() {
                    this.showNotifications = !this.showNotifications;
                },

                refreshStats() {
                    this.loading = true;
                    setTimeout(() => {
                        this.loadDashboardStats();
                        this.loading = false;
                    }, 1000);
                }
            }));
        });

        this.setupServiceWorker();
        this.initializeTooltips();
    }

    /**
     * Liaison des événements
     */
    bindEvents() {
        // Gestion du redimensionnement de la fenêtre
        window.addEventListener('resize', this.debounce(this.handleResize.bind(this), DashboardConfig.debounceDelay));

        // Gestion des clics sur les cartes
        document.querySelectorAll('.dashboard-card').forEach(card => {
            card.addEventListener('click', this.handleCardClick.bind(this));
            card.addEventListener('mouseenter', this.handleCardHover.bind(this));
            card.addEventListener('mouseleave', this.handleCardLeave.bind(this));
        });

        // Gestion de la navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', this.handleNavClick.bind(this));
        });

        // Gestion du formulaire de déconnexion
        const logoutForm = document.getElementById('logout-form');
        if (logoutForm) {
            logoutForm.addEventListener('submit', this.handleLogout.bind(this));
        }

        // Gestion des raccourcis clavier
        document.addEventListener('keydown', this.handleKeyboardShortcuts.bind(this));

        // Gestion de la visibilité de la page
        document.addEventListener('visibilitychange', this.handleVisibilityChange.bind(this));
    }

    /**
     * Chargement des statistiques
     */
    async loadStats() {
        try {
            // Simulation du chargement des données (remplacer par votre API)
            await this.delay(800);

            const mockStats = {
                equipements: Math.floor(Math.random() * 100) + 50,
                materiels: Math.floor(Math.random() * 200) + 100,
                fournisseurs: Math.floor(Math.random() * 50) + 20
            };

            this.updateStatsDisplay(mockStats);
            this.animateStatsCounters(mockStats);

        } catch (error) {
            console.error('❌ Erreur lors du chargement des statistiques:', error);
            this.showNotification('Erreur lors du chargement des données', 'error');
        }
    }

    /**
     * Mise à jour de l'affichage des statistiques
     */
    updateStatsDisplay(stats) {
        const statsElements = {
            equipements: document.querySelector('[data-stat="equipements"]'),
            materiels: document.querySelector('[data-stat="materiels"]'),
            fournisseurs: document.querySelector('[data-stat="fournisseurs"]')
        };

        Object.keys(stats).forEach(key => {
            const element = statsElements[key];
            if (element) {
                element.textContent = stats[key];
            }
        });
    }

    /**
     * Animation des compteurs de statistiques
     */
    animateStatsCounters(stats) {
        Object.keys(stats).forEach(key => {
            const element = document.querySelector(`[data-stat="${key}"]`);
            if (element) {
                this.animateCounter(element, 0, stats[key], 1500);
            }
        });
    }

    /**
     * Animation d'un compteur
     */
    animateCounter(element, start, end, duration) {
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            const current = Math.floor(start + (end - start) * this.easeOutCubic(progress));
            element.textContent = current;

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }

    /**
     * Fonction d'easing
     */
    easeOutCubic(t) {
        return 1 - Math.pow(1 - t, 3);
    }

    /**
     * Gestion du clic sur une carte
     */
    handleCardClick(event) {
        const card = event.currentTarget;
        const link = card.querySelector('a');

        // Animation de clic
        card.style.transform = 'scale(0.98) translateY(-2px)';
        setTimeout(() => {
            card.style.transform = '';
        }, 150);

        // Analytics (optionnel)
        this.trackEvent('card_click', {
            card_type: card.dataset.cardType || 'unknown'
        });
    }

    /**
     * Gestion du survol des cartes
     */
    handleCardHover(event) {
        const card = event.currentTarget;
        card.classList.add('animate-pulse');
    }

    /**
     * Gestion de la sortie du survol des cartes
     */
    handleCardLeave(event) {
        const card = event.currentTarget;
        card.classList.remove('animate-pulse');
    }

    /**
     * Gestion des clics de navigation
     */
    handleNavClick(event) {
        const link = event.currentTarget;

        // Animation de loading pour les liens internes
        if (link.getAttribute('href').startsWith('/')) {
            this.showLoadingState(link);
        }
    }

    /**
     * Gestion de la déconnexion
     */
    handleLogout(event) {
        // Ajout d'une animation de déconnexion
        this.showNotification('Déconnexion en cours...', 'info');

        // Optionnel: nettoyage des données locales
        this.clearLocalData();
    }

    /**
     * Gestion des raccourcis clavier
     */
    handleKeyboardShortcuts(event) {
        // Raccourcis utiles
        if (event.ctrlKey || event.metaKey) {
            switch(event.key) {
                case '1':
                    event.preventDefault();
                    this.navigateToSection('equipements');
                    break;
                case '2':
                    event.preventDefault();
                    this.navigateToSection('materiels');
                    break;
                case '3':
                    event.preventDefault();
                    this.navigateToSection('fournisseurs');
                    break;
                case 'r':
                    event.preventDefault();
                    this.refreshDashboard();
                    break;
            }
        }

        // Échap pour fermer les modales/dropdowns
        if (event.key === 'Escape') {
            this.closeAllDropdowns();
        }
    }

    /**
     * Gestion du changement de visibilité de la page
     */
    handleVisibilityChange() {
        if (!document.hidden) {
            // Actualiser les données quand l'utilisateur revient sur l'onglet
            this.refreshStats();
        }
    }

    /**
     * Gestion du redimensionnement
     */
    handleResize() {
        // Ajustement responsive si nécessaire
        this.adjustLayoutForViewport();
    }

    /**
     * Initialisation des animations
     */
    initializeAnimations() {
        // Animation d'entrée pour les cartes
        const cards = document.querySelectorAll('.dashboard-card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';

            setTimeout(() => {
                card.style.transition = 'all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });

        // Intersection Observer pour les animations au scroll
        this.setupScrollAnimations();
    }

    /**
     * Configuration des animations au scroll
     */
    setupScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in-up');
                }
            });
        }, observerOptions);

        document.querySelectorAll('.stats-card, .dashboard-card').forEach(el => {
            observer.observe(el);
        });
    }

    /**
     * Initialisation des tooltips
     */
    initializeTooltips() {
        document.querySelectorAll('[data-tooltip]').forEach(element => {
            element.addEventListener('mouseenter', this.showTooltip.bind(this));
            element.addEventListener('mouseleave', this.hideTooltip.bind(this));
        });
    }

    /**
     * Affichage d'un tooltip
     */
    showTooltip(event) {
        const element = event.currentTarget;
        const text = element.dataset.tooltip;

        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip absolute bg-gray-900 text-white px-2 py-1 rounded text-sm z-50';
        tooltip.textContent = text;
        tooltip.id = 'active-tooltip';

        document.body.appendChild(tooltip);

        // Position du tooltip
        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
    }

    /**
     * Masquage du tooltip
     */
    hideTooltip() {
        const tooltip = document.getElementById('active-tooltip');
        if (tooltip) {
            tooltip.remove();
        }
    }

    /**
     * Configuration du Service Worker
     */
    setupServiceWorker() {
        if (!('serviceWorker' in navigator)) {
            return;
        }

        if (location.protocol === 'https:') {
            navigator.serviceWorker.register('/sw.js')
                .then(() => {
                    console.log('✅ Service Worker registered');
                })
                .catch(() => {
                    console.log('❌ Service Worker registration failed');
                });
        } else {
            // On HTTP dev, unregister any existing SW and clear caches to prevent HTTPS attempts
            navigator.serviceWorker.getRegistrations()
                .then(registrations => registrations.forEach(r => r.unregister()))
                .catch(() => {});
            if (window.caches && typeof caches.keys === 'function') {
                caches.keys().then(keys => keys.forEach(k => caches.delete(k))).catch(() => {});
            }
        }
    }

    /**
     * Affichage d'une notification
     */
    showNotification(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `notification fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 transform translate-x-full transition-transform duration-300 ${this.getNotificationClass(type)}`;
        notification.innerHTML = `
            <div class="flex items-center space-x-3">
                ${this.getNotificationIcon(type)}
                <span class="text-sm font-medium">${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-gray-400 hover:text-gray-600">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                    </svg>
                </button>
            </div>
        `;

        document.body.appendChild(notification);

        // Animation d'entrée
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Suppression automatique
        setTimeout(() => {
            notification.style.transform = 'translateX(full)';
            setTimeout(() => notification.remove(), 300);
        }, duration);
    }

    /**
     * Classes CSS pour les notifications
     */
    getNotificationClass(type) {
        const classes = {
            info: 'bg-blue-500 text-white',
            success: 'bg-green-500 text-white',
            warning: 'bg-yellow-500 text-black',
            error: 'bg-red-500 text-white'
        };
        return classes[type] || classes.info;
    }

    /**
     * Icônes pour les notifications
     */
    getNotificationIcon(type) {
        const icons = {
            info: '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>',
            success: '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>',
            warning: '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path></svg>',
            error: '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path></svg>'
        };
        return icons[type] || icons.info;
    }

    /**
     * Fonctions utilitaires
     */

    // Debounce function
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Delay function
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Navigation vers une section
    navigateToSection(section) {
        const links = {
            'equipements': document.querySelector('[href*="equipement_list"]'),
            'materiels': document.querySelector('[href*="materiel_list"]'),
            'fournisseurs': document.querySelector('[href*="fournisseur_list"]')
        };

        if (links[section]) {
            links[section].click();
        }
    }

    // Actualisation du dashboard
    refreshDashboard() {
        this.showNotification('Actualisation des données...', 'info', 2000);
        this.loadStats();
    }

    // Fermeture des dropdowns
    closeAllDropdowns() {
        // Utilisation d'Alpine.js pour fermer les dropdowns
        document.querySelectorAll('[x-show]').forEach(element => {
            if (element._x_dataStack && element._x_dataStack[0].open) {
                element._x_dataStack[0].open = false;
            }
        });
    }

    // Ajustement pour différentes tailles d'écran
    adjustLayoutForViewport() {
        const isMobile = window.innerWidth < 768;
        document.body.classList.toggle('mobile-view', isMobile);
    }

    // Nettoyage des données locales
    clearLocalData() {
        // Nettoyage du cache ou des données temporaires
        console.log('🧹 Nettoyage des données locales');
    }

    // État de chargement
    showLoadingState(element) {
        element.classList.add('loading');
        setTimeout(() => {
            element.classList.remove('loading');
        }, 1000);
    }

    // Tracking des événements (pour analytics)
    trackEvent(eventName, parameters = {}) {
        // Intégration avec Google Analytics, Mixpanel, etc.
        console.log('📊 Event tracked:', eventName, parameters);
    }
}

/**
 * Initialisation automatique du dashboard
 */
document.addEventListener('DOMContentLoaded', () => {
    // Vérification de l'environnement
    console.log('🌍 Environment:', document.location.hostname);

    // Initialisation du dashboard
    window.dashboard = new Dashboard();

    // Gestion des erreurs globales
    window.addEventListener('error', (event) => {
        console.error('❌ Global error:', event.error);
    });

    // Gestion des promesses rejetées
    window.addEventListener('unhandledrejection', (event) => {
        console.error('❌ Unhandled promise rejection:', event.reason);
    });
});

/**
 * Fonctions utilitaires globales
 */

// Animation smooth scroll
function smoothScrollTo(target, duration = 800) {
    const targetElement = document.querySelector(target);
    if (targetElement) {
        targetElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Formatage des nombres
function formatNumber(num) {
    return new Intl.NumberFormat('fr-FR').format(num);
}

// Gestion des thèmes (si nécessaire plus tard)
function toggleTheme() {
    document.body.classList.toggle('dark-theme');
    localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
}

// Copie vers le presse-papier
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        window.dashboard.showNotification('Copié dans le presse-papier', 'success');
    } catch (err) {
        window.dashboard.showNotification('Erreur lors de la copie', 'error');
    }
}

// Export des fonctions pour usage global
window.dashboardUtils = {
    smoothScrollTo,
    formatNumber,
    toggleTheme,
    copyToClipboard
};