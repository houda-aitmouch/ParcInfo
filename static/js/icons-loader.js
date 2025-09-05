/**
 * SYSTÈME DE CHARGEMENT D'ICÔNES MODERNE - PARCINFO
 * 
 * Chargeur d'icônes optimisé utilisant Lucide Icons
 * Performances améliorées avec lazy loading et cache
 */

class IconsLoader {
    constructor() {
        this.cache = new Map();
        this.loadedIcons = new Set();
        this.baseUrl = 'https://cdn.jsdelivr.net/npm/lucide@latest/icons/';
        this.fallbackIcons = this.initFallbackIcons();
        this.init();
    }

    init() {
        this.preloadCriticalIcons();
        this.setupIntersectionObserver();
        this.replaceOldIcons();
        console.log('🎨 Système d\'icônes ParcInfo initialisé');
    }

    initFallbackIcons() {
        return {
            'home': '<svg class="icon" viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9,22 9,12 15,12 15,22"/></svg>',
            'user': '<svg class="icon" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
            'settings': '<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
            'loading': '<svg class="icon icon-spin" viewBox="0 0 24 24"><path d="M21 12a9 9 0 11-6.219-8.56"/></svg>'
        };
    }

    async preloadCriticalIcons() {
        const criticalIcons = [
            'home', 'user', 'settings', 'menu', 'x', 'search',
            'bell', 'help-circle', 'chevron-down', 'chevron-right'
        ];

        const promises = criticalIcons.map(icon => this.loadIcon(icon));
        await Promise.all(promises);
        console.log('✅ Icônes critiques préchargées');
    }

    setupIntersectionObserver() {
        if ('IntersectionObserver' in window) {
            this.observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.loadIconElement(entry.target);
                        this.observer.unobserve(entry.target);
                    }
                });
            }, {
                rootMargin: '50px'
            });

            document.querySelectorAll('[data-icon]').forEach(el => {
                this.observer.observe(el);
            });
        }
    }

    async loadIcon(iconName) {
        if (this.cache.has(iconName)) {
            return this.cache.get(iconName);
        }

        try {
            const response = await fetch(`${this.baseUrl}${iconName}.svg`);
            if (response.ok) {
                const svgContent = await response.text();
                const processedSvg = this.processSvg(svgContent);
                this.cache.set(iconName, processedSvg);
                this.loadedIcons.add(iconName);
                return processedSvg;
            }
        } catch (error) {
            console.warn(`⚠️ Impossible de charger l'icône ${iconName}, utilisation du fallback`);
        }

        const fallback = this.fallbackIcons[iconName] || this.fallbackIcons['settings'];
        this.cache.set(iconName, fallback);
        return fallback;
    }

    processSvg(svgContent) {
        return svgContent
            .replace(/<svg[^>]*>/, '<svg class="icon" viewBox="0 0 24 24">')
            .replace(/stroke="[^"]*"/g, 'stroke="currentColor"')
            .replace(/fill="[^"]*"/g, 'fill="none"')
            .replace(/stroke-width="[^"]*"/g, 'stroke-width="2"')
            .replace(/stroke-linecap="[^"]*"/g, 'stroke-linecap="round"')
            .replace(/stroke-linejoin="[^"]*"/g, 'stroke-linejoin="round"');
    }

    async loadIconElement(element) {
        const iconName = element.getAttribute('data-icon');
        const iconSize = element.getAttribute('data-icon-size') || 'md';
        const iconColor = element.getAttribute('data-icon-color') || '';

        if (!iconName) return;

        element.innerHTML = this.fallbackIcons['loading'];

        try {
            const iconSvg = await this.loadIcon(iconName);
            element.innerHTML = iconSvg;
            
            const svg = element.querySelector('svg');
            if (svg) {
                svg.classList.add(`icon-${iconSize}`);
                if (iconColor) svg.classList.add(`icon-${iconColor}`);
            }
        } catch (error) {
            console.error(`❌ Erreur lors du chargement de l'icône ${iconName}:`, error);
            element.innerHTML = this.fallbackIcons['settings'];
        }
    }

    replaceOldIcons() {
        const iconMappings = {
            'fas fa-home': 'home',
            'fas fa-user': 'user',
            'fas fa-cog': 'settings',
            'fas fa-bell': 'bell',
            'fas fa-search': 'search',
            'fas fa-menu': 'menu',
            'fas fa-times': 'x',
            'fas fa-plus': 'plus',
            'fas fa-edit': 'edit',
            'fas fa-trash': 'trash-2',
            'fas fa-eye': 'eye',
            'fas fa-download': 'download',
            'fas fa-save': 'save',
            'fas fa-print': 'printer',
            'fas fa-robot': 'bot',
            'fas fa-question-circle': 'help-circle',
            'fas fa-history': 'history',
            'fas fa-paper-plane': 'send',
            'fas fa-microphone': 'mic',
            'fas fa-copy': 'copy',
            'fas fa-thumbs-up': 'thumbs-up',
            'fas fa-thumbs-down': 'thumbs-down'
        };

        Object.entries(iconMappings).forEach(([oldClass, newIcon]) => {
            document.querySelectorAll(`i.${oldClass.replace(/\s+/g, '.')}`).forEach(element => {
                const container = document.createElement('span');
                container.setAttribute('data-icon', newIcon);
                container.className = element.className.replace(oldClass, 'icon-container');
                element.parentNode.replaceChild(container, element);
                this.loadIconElement(container);
            });
        });
    }

    // API publique
    static getInstance() {
        if (!window.parcInfoIcons) {
            window.parcInfoIcons = new IconsLoader();
        }
        return window.parcInfoIcons;
    }

    static loadIcon(iconName, size = 'md', color = '') {
        const instance = IconsLoader.getInstance();
        return instance.loadIcon(iconName);
    }

    static replaceIcon(element, iconName, size = 'md', color = '') {
        element.setAttribute('data-icon', iconName);
        element.setAttribute('data-icon-size', size);
        if (color) element.setAttribute('data-icon-color', color);
        
        const instance = IconsLoader.getInstance();
        instance.loadIconElement(element);
    }
}

// Initialisation automatique
document.addEventListener('DOMContentLoaded', () => {
    IconsLoader.getInstance();
});

// Export pour utilisation externe
window.IconsLoader = IconsLoader;
