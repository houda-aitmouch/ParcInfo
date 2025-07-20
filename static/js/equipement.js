// ===== CONFIGURATION ALPINE.JS POUR LA GESTION DU TABLEAU =====
document.addEventListener('alpine:init', () => {
    Alpine.data('equipmentTable', () => ({
        // État de l'application
        isLoading: false,
        searchQuery: '',
        sortColumn: '',
        sortDirection: 'asc',
        selectedRows: [],
        showFilters: false,
        currentPage: 1,
        itemsPerPage: 10,

        // Données d'exemple pour le tableau d'équipements
        equipment: [
            {
                id: 1,
                name: 'Serveur Principal',
                type: 'Serveur',
                location: 'Salle A',
                status: 'active',
                lastMaintenance: '2024-01-15',
                nextMaintenance: '2024-07-15',
                responsible: 'Jean Dupont'
            },
            {
                id: 2,
                name: 'Router Cisco 2900',
                type: 'Réseau',
                location: 'Salle B',
                status: 'active',
                lastMaintenance: '2024-02-01',
                nextMaintenance: '2024-08-01',
                responsible: 'Marie Martin'
            },
            {
                id: 3,
                name: 'Switch HP 48 ports',
                type: 'Réseau',
                location: 'Salle A',
                status: 'maintenance',
                lastMaintenance: '2024-01-20',
                nextMaintenance: '2024-07-20',
                responsible: 'Pierre Durand'
            },
            {
                id: 4,
                name: 'Onduleur APC 3000VA',
                type: 'Alimentation',
                location: 'Salle C',
                status: 'active',
                lastMaintenance: '2024-01-10',
                nextMaintenance: '2024-07-10',
                responsible: 'Sophie Bernard'
            },
            {
                id: 5,
                name: 'Serveur Backup',
                type: 'Serveur',
                location: 'Salle A',
                status: 'inactive',
                lastMaintenance: '2024-01-25',
                nextMaintenance: '2024-07-25',
                responsible: 'Michel Dubois'
            },
            {
                id: 6,
                name: 'Firewall FortiGate',
                type: 'Sécurité',
                location: 'Salle B',
                status: 'active',
                lastMaintenance: '2024-02-05',
                nextMaintenance: '2024-08-05',
                responsible: 'Laura Petit'
            },
            {
                id: 7,
                name: 'NAS Synology',
                type: 'Stockage',
                location: 'Salle C',
                status: 'pending',
                lastMaintenance: '2024-01-30',
                nextMaintenance: '2024-07-30',
                responsible: 'Thomas Moreau'
            },
            {
                id: 8,
                name: 'Imprimante Réseau HP',
                type: 'Périphérique',
                location: 'Bureau',
                status: 'active',
                lastMaintenance: '2024-02-10',
                nextMaintenance: '2024-08-10',
                responsible: 'Anne Leroy'
            }
        ],

        // Filtres disponibles
        statusFilters: ['all', 'active', 'inactive', 'maintenance', 'pending'],
        typeFilters: ['all', 'Serveur', 'Réseau', 'Alimentation', 'Sécurité', 'Stockage', 'Périphérique'],

        selectedStatusFilter: 'all',
        selectedTypeFilter: 'all',

        // Initialisation
        init() {
            this.animateTableRows();
            this.setupIntersectionObserver();
            this.preloadStatusColors();
        },

        // Animation des lignes du tableau
        animateTableRows() {
            this.$nextTick(() => {
                const rows = document.querySelectorAll('.equipment-row');
                rows.forEach((row, index) => {
                    setTimeout(() => {
                        row.style.opacity = '1';
                        row.style.transform = 'translateY(0)';
                    }, index * 100);
                });
            });
        },

        // Configuration de l'observateur d'intersection pour les animations
        setupIntersectionObserver() {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('fade-in');
                    }
                });
            }, { threshold: 0.1 });

            this.$nextTick(() => {
                const elements = document.querySelectorAll('.animate-on-scroll');
                elements.forEach(el => observer.observe(el));
            });
        },

        // Préchargement des couleurs de statut
        preloadStatusColors() {
            const statusColors = {
                active: 'status-active',
                inactive: 'status-inactive',
                maintenance: 'status-maintenance',
                pending: 'status-pending'
            };
            this.statusColors = statusColors;
        },

        // Données filtrées et triées
        get filteredEquipment() {
            let filtered = this.equipment;

            // Filtre par recherche
            if (this.searchQuery) {
                const query = this.searchQuery.toLowerCase();
                filtered = filtered.filter(item =>
                    item.name.toLowerCase().includes(query) ||
                    item.type.toLowerCase().includes(query) ||
                    item.location.toLowerCase().includes(query) ||
                    item.responsible.toLowerCase().includes(query)
                );
            }

            // Filtre par statut
            if (this.selectedStatusFilter !== 'all') {
                filtered = filtered.filter(item => item.status === this.selectedStatusFilter);
            }

            // Filtre par type
            if (this.selectedTypeFilter !== 'all') {
                filtered = filtered.filter(item => item.type === this.selectedTypeFilter);
            }

            // Tri
            if (this.sortColumn) {
                filtered.sort((a, b) => {
                    let aVal = a[this.sortColumn];
                    let bVal = b[this.sortColumn];

                    if (typeof aVal === 'string') {
                        aVal = aVal.toLowerCase();
                        bVal = bVal.toLowerCase();
                    }

                    if (this.sortDirection === 'asc') {
                        return aVal > bVal ? 1 : -1;
                    } else {
                        return aVal < bVal ? 1 : -1;
                    }
                });
            }

            return filtered;
        },

        // Pagination
        get paginatedEquipment() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.filteredEquipment.slice(start, end);
        },

        get totalPages() {
            return Math.ceil(this.filteredEquipment.length / this.itemsPerPage);
        },

        // Fonctions de tri
        sort(column) {
            if (this.sortColumn === column) {
                this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                this.sortColumn = column;
                this.sortDirection = 'asc';
            }
            this.currentPage = 1;
            this.animateTableRows();
        },

        // Fonctions de sélection
        toggleRow(id) {
            const index = this.selectedRows.indexOf(id);
            if (index > -1) {
                this.selectedRows.splice(index, 1);
            } else {
                this.selectedRows.push(id);
            }
        },

        toggleAllRows() {
            if (this.selectedRows.length === this.paginatedEquipment.length) {
                this.selectedRows = [];
            } else {
                this.selectedRows = this.paginatedEquipment.map(item => item.id);
            }
        },

        // Fonctions de pagination
        goToPage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
                this.animateTableRows();
            }
        },

        nextPage() {
            this.goToPage(this.currentPage + 1);
        },

        prevPage() {
            this.goToPage(this.currentPage - 1);
        },

        // Utilitaires pour le statut
        getStatusClass(status) {
            const classes = {
                active: 'bg-green-500 text-white status-active',
                inactive: 'bg-red-500 text-white status-inactive',
                maintenance: 'bg-yellow-500 text-white status-maintenance',
                pending: 'bg-blue-500 text-white status-pending'
            };
            return classes[status] || 'bg-gray-500 text-white';
        },

        getStatusText(status) {
            const texts = {
                active: 'Actif',
                inactive: 'Inactif',
                maintenance: 'Maintenance',
                pending: 'En attente'
            };
            return texts[status] || status;
        },

        // Fonctions de filtrage
        resetFilters() {
            this.searchQuery = '';
            this.selectedStatusFilter = 'all';
            this.selectedTypeFilter = 'all';
            this.sortColumn = '';
            this.sortDirection = 'asc';
            this.currentPage = 1;
        },

        // Fonctions d'actions
        async refreshTable() {
            this.isLoading = true;

            // Simulation d'un appel API
            await new Promise(resolve => setTimeout(resolve, 1000));

            this.isLoading = false;
            this.animateTableRows();

            // Notification de succès
            this.showNotification('Tableau mis à jour avec succès', 'success');
        },

        exportToCSV() {
            const headers = ['ID', 'Nom', 'Type', 'Localisation', 'Statut', 'Dernière Maintenance', 'Prochaine Maintenance', 'Responsable'];
            const csvContent = [
                headers.join(','),
                ...this.filteredEquipment.map(item => [
                    item.id,
                    `"${item.name}"`,
                    `"${item.type}"`,
                    `"${item.location}"`,
                    `"${this.getStatusText(item.status)}"`,
                    item.lastMaintenance,
                    item.nextMaintenance,
                    `"${item.responsible}"`
                ].join(','))
            ].join('\n');

            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'equipments.csv';
            link.click();
        },

        // Système de notifications
        notifications: [],

        showNotification(message, type = 'info', duration = 3000) {
            const id = Date.now();
            this.notifications.push({ id, message, type });

            setTimeout(() => {
                this.removeNotification(id);
            }, duration);
        },

        removeNotification(id) {
            const index = this.notifications.findIndex(n => n.id === id);
            if (index > -1) {
                this.notifications.splice(index, 1);
            }
        }
    }));
});

// ===== FONCTIONS UTILITAIRES GLOBALES =====

// Animation au scroll
function animateOnScroll() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// Smooth scroll pour les ancres
function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Gestion du thème sombre/clair
function setupThemeToggle() {
    const themeToggle = document.querySelector('#theme-toggle');
    const html = document.documentElement;

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            html.classList.toggle('dark');
            localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
        });
    }

    // Chargement du thème sauvegardé
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        html.classList.add('dark');
    }
}

// Effets de particules pour le background
function createParticleEffect() {
    const canvas = document.createElement('canvas');
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '-1';
    canvas.style.opacity = '0.1';

    document.body.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    const particles = [];

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    function createParticle() {
        return {
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5,
            size: Math.random() * 3 + 1,
            opacity: Math.random() * 0.5 + 0.2
        };
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach((particle, index) => {
            particle.x += particle.vx;
            particle.y += particle.vy;

            if (particle.x < 0 || particle.x > canvas.width) particle.vx *= -1;
            if (particle.y < 0 || particle.y > canvas.height) particle.vy *= -1;

            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(139, 92, 246, ${particle.opacity})`;
            ctx.fill();
        });

        requestAnimationFrame(animate);
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Créer des particules
    for (let i = 0; i < 50; i++) {
        particles.push(createParticle());
    }

    animate();
}

// Initialisation au chargement du DOM
document.addEventListener('DOMContentLoaded', function() {
    animateOnScroll();
    setupSmoothScroll();
    setupThemeToggle();

    // Créer l'effet de particules (optionnel)
    // createParticleEffect();

    // Animation d'entrée pour la page
    document.body.style.opacity = '0';
    document.body.style.transform = 'translateY(20px)';

    setTimeout(() => {
        document.body.style.transition = 'all 0.6s ease-out';
        document.body.style.opacity = '1';
        document.body.style.transform = 'translateY(0)';
    }, 100);
});

// ===== FONCTIONS DE PERFORMANCE =====

// Debounce pour les recherches
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

// Throttle pour les événements scroll
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Lazy loading pour les images
function setupLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('loading');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}