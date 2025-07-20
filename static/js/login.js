// login.js - Code JavaScript pour la page de connexion

/**
 * Configuration Tailwind CSS personnalisée
 * À inclure dans le <head> si vous utilisez le CDN Tailwind
 */
const tailwindConfig = {
    theme: {
        extend: {
            colors: {
                'brand-blue': '#3399FF',
                'brand-purple': '#8B5CF6'
            }
        }
    }
};

/**
 * Fonction Alpine.js pour le formulaire de connexion
 * Gère l'état du formulaire et les interactions utilisateur
 */
function loginForm() {
    return {
        // État du formulaire
        loading: false,
        formData: {
            username: '',
            password: '',
            rememberMe: false
        },

        // Gestion de la soumission du formulaire
        handleSubmit(event) {
            this.loading = true;

            // Validation côté client (optionnelle)
            if (!this.validateForm()) {
                this.loading = false;
                event.preventDefault();
                return false;
            }

            // Ajout d'un feedback visuel
            this.showSubmissionFeedback();

            // Le formulaire Django se chargera de la soumission réelle
            // Le loading sera réinitialisé au chargement de la nouvelle page
        },

        // Validation basique du formulaire
        validateForm() {
            const username = document.querySelector('input[name="username"]');
            const password = document.querySelector('input[name="password"]');

            if (!username.value.trim()) {
                this.showError('Veuillez saisir votre nom d\'utilisateur ou email');
                username.focus();
                return false;
            }

            if (!password.value.trim()) {
                this.showError('Veuillez saisir votre mot de passe');
                password.focus();
                return false;
            }

            return true;
        },

        // Affichage des erreurs
        showError(message) {
            // Créer ou mettre à jour un élément d'erreur
            let errorDiv = document.getElementById('client-error');
            if (!errorDiv) {
                errorDiv = document.createElement('div');
                errorDiv.id = 'client-error';
                errorDiv.className = 'bg-red-50 border-l-4 border-red-400 p-4 rounded-lg mb-4 error-fade-in';

                const form = document.querySelector('form');
                form.insertBefore(errorDiv, form.firstChild);
            }

            errorDiv.innerHTML = `
                <div class="flex">
                    <i class="fas fa-exclamation-triangle text-red-400 mr-2 mt-0.5"></i>
                    <div class="text-red-700 text-sm">
                        <p>${message}</p>
                    </div>
                </div>
            `;

            // Faire disparaître l'erreur après 5 secondes
            setTimeout(() => {
                if (errorDiv) {
                    errorDiv.style.opacity = '0';
                    setTimeout(() => errorDiv.remove(), 300);
                }
            }, 5000);
        },

        // Feedback visuel lors de la soumission
        showSubmissionFeedback() {
            const button = document.querySelector('button[type="submit"]');
            if (button) {
                button.classList.add('animate-pulse');
            }
        },

        // Initialisation du composant
        init() {
            // Animation d'entrée
            this.$nextTick(() => {
                const formContainer = this.$el.querySelector('.bg-white');
                if (formContainer) {
                    formContainer.classList.add('animate-fade-in');
                }
            });

            // Gestion du focus automatique
            this.setupAutoFocus();

            // Gestion des raccourcis clavier
            this.setupKeyboardShortcuts();

            // Préchargement des icônes
            this.preloadIcons();
        },

        // Configuration du focus automatique
        setupAutoFocus() {
            setTimeout(() => {
                const firstInput = document.querySelector('input[name="username"]');
                if (firstInput && !firstInput.value) {
                    firstInput.focus();
                }
            }, 100);
        },

        // Raccourcis clavier
        setupKeyboardShortcuts() {
            document.addEventListener('keydown', (e) => {
                // Entrée pour soumettre le formulaire
                if (e.key === 'Enter' && e.ctrlKey) {
                    e.preventDefault();
                    document.querySelector('form').submit();
                }
            });
        },

        // Préchargement des icônes pour une meilleure performance
        preloadIcons() {
            const icons = ['fa-user', 'fa-lock', 'fa-eye', 'fa-eye-slash', 'fa-sign-in-alt'];
            icons.forEach(icon => {
                const link = document.createElement('link');
                link.rel = 'preload';
                link.href = `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/fa-solid-900.woff2`;
                link.as = 'font';
                link.type = 'font/woff2';
                link.crossOrigin = 'anonymous';
                document.head.appendChild(link);
            });
        }
    }
}

/**
 * Fonction pour gérer la visibilité du mot de passe
 * Utilisation: x-data="passwordToggle()"
 */
function passwordToggle() {
    return {
        showPassword: false,
        focused: false,

        toggleVisibility() {
            this.showPassword = !this.showPassword;

            // Maintenir le focus sur le champ
            const input = this.$el.querySelector('input');
            if (input) {
                setTimeout(() => input.focus(), 10);
            }
        }
    }
}

/**
 * Fonction pour gérer les champs de saisie avec animation
 * Utilisation: x-data="inputField()"
 */
function inputField() {
    return {
        focused: false,
        hasValue: false,

        init() {
            const input = this.$el.querySelector('input');
            if (input) {
                this.hasValue = input.value.length > 0;

                // Observer les changements de valeur
                input.addEventListener('input', () => {
                    this.hasValue = input.value.length > 0;
                });
            }
        },

        handleFocus() {
            this.focused = true;
        },

        handleBlur() {
            this.focused = false;
        }
    }
}

/**
 * Initialisation après le chargement du DOM
 */
document.addEventListener('DOMContentLoaded', function() {
    // Gestion des erreurs de réseau
    setupNetworkErrorHandling();

    // Amélioration de l'accessibilité
    enhanceAccessibility();

    // Configuration des événements globaux
    setupGlobalEvents();
});

/**
 * Gestion des erreurs de réseau et de connectivité
 */
function setupNetworkErrorHandling() {
    // Détection de la perte de connexion
    window.addEventListener('offline', () => {
        showNetworkStatus('Connexion perdue. Vérifiez votre connexion internet.', 'error');
    });

    window.addEventListener('online', () => {
        showNetworkStatus('Connexion rétablie.', 'success');
    });
}

/**
 * Affichage du statut réseau
 */
function showNetworkStatus(message, type) {
    const statusDiv = document.createElement('div');
    statusDiv.className = `fixed top-4 right-4 z-50 px-4 py-2 rounded-lg shadow-lg text-white text-sm transform transition-all duration-300 ${
        type === 'error' ? 'bg-red-500' : 'bg-green-500'
    }`;
    statusDiv.textContent = message;

    document.body.appendChild(statusDiv);

    // Animation d'entrée
    setTimeout(() => {
        statusDiv.style.transform = 'translateX(0)';
    }, 10);

    // Suppression automatique
    setTimeout(() => {
        statusDiv.style.transform = 'translateX(100%)';
        setTimeout(() => statusDiv.remove(), 300);
    }, 3000);
}

/**
 * Amélioration de l'accessibilité
 */
function enhanceAccessibility() {
    // Ajout d'attributs ARIA aux éléments interactifs
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        if (input.hasAttribute('required')) {
            input.setAttribute('aria-required', 'true');
        }
    });

    // Gestion des messages d'erreur pour les lecteurs d'écran
    const errorContainers = document.querySelectorAll('.text-red-500');
    errorContainers.forEach(container => {
        container.setAttribute('role', 'alert');
        container.setAttribute('aria-live', 'polite');
    });
}

/**
 * Configuration des événements globaux
 */
function setupGlobalEvents() {
    // Prévention de la soumission multiple
    let isSubmitting = false;

    document.addEventListener('submit', (e) => {
        if (isSubmitting) {
            e.preventDefault();
            return false;
        }
        isSubmitting = true;

        // Réinitialisation après 5 secondes (sécurité)
        setTimeout(() => {
            isSubmitting = false;
        }, 5000);
    });

    // Gestion du redimensionnement de la fenêtre
    window.addEventListener('resize', debounce(() => {
        // Ajustements responsive si nécessaire
    }, 250));
}

/**
 * Utilitaire de debounce pour optimiser les performances
 */
function debounce(func, wait) {
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

/**
 * Fonction utilitaire pour valider les emails
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Fonction utilitaire pour valider la force du mot de passe
 */
function checkPasswordStrength(password) {
    const strength = {
        score: 0,
        feedback: []
    };

    if (password.length >= 8) strength.score++;
    else strength.feedback.push('Au moins 8 caractères');

    if (/[A-Z]/.test(password)) strength.score++;
    else strength.feedback.push('Au moins une majuscule');

    if (/[a-z]/.test(password)) strength.score++;
    else strength.feedback.push('Au moins une minuscule');

    if (/\d/.test(password)) strength.score++;
    else strength.feedback.push('Au moins un chiffre');

    if (/[^A-Za-z0-9]/.test(password)) strength.score++;
    else strength.feedback.push('Au moins un caractère spécial');

    return strength;
}

// Export pour les modules ES6 (si utilisé)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        loginForm,
        passwordToggle,
        inputField,
        isValidEmail,
        checkPasswordStrength
    };
}