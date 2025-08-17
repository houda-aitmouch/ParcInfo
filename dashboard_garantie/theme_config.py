"""
Configuration des thèmes et couleurs pour le Dashboard Garantie
"""

# Configuration des couleurs professionnelles
COLORS = {
    'primary': {
        'main': '#2563eb',
        'dark': '#1d4ed8',
        'light': '#3b82f6',
        'contrast': '#ffffff'
    },
    'secondary': {
        'main': '#64748b',
        'dark': '#475569',
        'light': '#94a3b8',
        'contrast': '#ffffff'
    },
    'success': {
        'main': '#059669',
        'dark': '#047857',
        'light': '#10b981',
        'contrast': '#ffffff'
    },
    'warning': {
        'main': '#d97706',
        'dark': '#b45309',
        'light': '#f59e0b',
        'contrast': '#ffffff'
    },
    'danger': {
        'main': '#dc2626',
        'dark': '#b91c1c',
        'light': '#ef4444',
        'contrast': '#ffffff'
    },
    'info': {
        'main': '#0891b2',
        'dark': '#0e7490',
        'light': '#06b6d4',
        'contrast': '#ffffff'
    },
    'background': {
        'primary': '#ffffff',
        'secondary': '#f8fafc',
        'tertiary': '#f1f5f9'
    },
    'text': {
        'primary': '#1e293b',
        'secondary': '#64748b',
        'muted': '#94a3b8'
    },
    'border': {
        'main': '#e2e8f0',
        'light': '#f1f5f9'
    }
}

# Configuration des gradients
GRADIENTS = {
    'primary': 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)',
    'secondary': 'linear-gradient(135deg, #64748b 0%, #475569 100%)',
    'success': 'linear-gradient(135deg, #059669 0%, #047857 100%)',
    'warning': 'linear-gradient(135deg, #d97706 0%, #b45309 100%)',
    'danger': 'linear-gradient(135deg, #dc2626 0%, #b91c1c 100%)',
    'info': 'linear-gradient(135deg, #0891b2 0%, #0e7490 100%)',
    'header': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'card': 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)'
}

# Configuration des ombres
SHADOWS = {
    'sm': '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    'md': '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    'lg': '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
    'xl': '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)'
}

# Configuration des bordures
BORDER_RADIUS = {
    'sm': '6px',
    'md': '12px',
    'lg': '16px',
    'xl': '20px',
    'full': '9999px'
}

# Configuration des espacements
SPACING = {
    'xs': '0.25rem',
    'sm': '0.5rem',
    'md': '1rem',
    'lg': '1.5rem',
    'xl': '2rem',
    '2xl': '3rem'
}

# Configuration des tailles de police
FONT_SIZES = {
    'xs': '0.75rem',
    'sm': '0.875rem',
    'md': '1rem',
    'lg': '1.125rem',
    'xl': '1.25rem',
    '2xl': '1.5rem',
    '3xl': '1.875rem',
    '4xl': '2.25rem'
}

# Configuration des poids de police
FONT_WEIGHTS = {
    'light': '300',
    'normal': '400',
    'medium': '500',
    'semibold': '600',
    'bold': '700',
    'extrabold': '800'
}

# Configuration des icônes par statut
ICONS = {
    'critical': '🚨',
    'warning': '⚠️',
    'success': '✅',
    'info': 'ℹ️',
    'error': '❌',
    'loading': '🔄',
    'shield': '🛡️',
    'chart': '📊',
    'user': '👤',
    'calendar': '📅',
    'clock': '⏰',
    'fire': '🔥',
    'lightning': '⚡',
    'gear': '⚙️',
    'home': '🏠',
    'computer': '💻',
    'office': '🏢'
}

# Configuration des messages d'alerte
ALERT_MESSAGES = {
    'critical': {
        'title': 'ALERTE CRITIQUE',
        'description': 'Garanties expirant dans les 15 prochains jours',
        'icon': ICONS['critical'],
        'color': COLORS['danger']['main']
    },
    'warning': {
        'title': 'ALERTE URGENTE',
        'description': 'Garanties expirant dans les 30 prochains jours',
        'icon': ICONS['warning'],
        'color': COLORS['warning']['main']
    },
    'info': {
        'title': 'INFORMATION',
        'description': 'Garanties nécessitant une attention particulière',
        'icon': ICONS['info'],
        'color': COLORS['info']['main']
    }
}

# Configuration des métriques
METRICS_CONFIG = {
    'total_commandes': {
        'label': 'Total Commandes',
        'icon': ICONS['chart'],
        'color': COLORS['primary']['main']
    },
    'en_garantie': {
        'label': 'En Garantie',
        'icon': ICONS['shield'],
        'color': COLORS['success']['main']
    },
    'expirees': {
        'label': 'Garanties Expirées',
        'icon': ICONS['error'],
        'color': COLORS['danger']['main']
    },
    'critiques': {
        'label': 'Critiques (≤15j)',
        'icon': ICONS['fire'],
        'color': COLORS['danger']['main']
    },
    'urgentes': {
        'label': 'Urgentes (≤30j)',
        'icon': ICONS['lightning'],
        'color': COLORS['warning']['main']
    }
}

# Configuration des graphiques Plotly
PLOTLY_CONFIG = {
    'displayModeBar': False,
    'responsive': True,
    'displaylogo': False
}

# Configuration des thèmes Plotly
PLOTLY_THEME = {
    'layout': {
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'font': {
            'family': 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            'color': COLORS['text']['primary']
        },
        'margin': {'l': 50, 'r': 50, 't': 50, 'b': 50}
    }
}

# Configuration des rôles utilisateur
USER_ROLES = {
    'super_admin': {
        'name': 'Super Admin',
        'description': 'Accès complet à toutes les fonctionnalités',
        'icon': '👑',
        'color': COLORS['primary']['main']
    },
    'gestionnaire_info': {
        'name': 'Gestionnaire Informatique',
        'description': 'Gestion des équipements informatiques',
        'icon': ICONS['computer'],
        'color': COLORS['info']['main']
    },
    'gestionnaire_bureau': {
        'name': 'Gestionnaire Bureau',
        'description': 'Gestion des équipements de bureau',
        'icon': ICONS['office'],
        'color': COLORS['secondary']['main']
    },
    'employe': {
        'name': 'Employé',
        'description': 'Consultation des garanties',
        'icon': ICONS['user'],
        'color': COLORS['text']['secondary']
    }
}
