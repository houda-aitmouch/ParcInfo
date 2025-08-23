# 🎨 Guide Style Figma - ParcInfo

## 📋 Vue d'ensemble

Ce guide explique comment utiliser le style Figma exactement reproduit dans votre projet Django ParcInfo. Le design utilise Tailwind CSS avec des couleurs, gradients et composants personnalisés qui correspondent fidèlement au prototype Figma.

## 🚀 Installation et Configuration

### 1. Prérequis
- Django 5.2+
- Tailwind CSS (via CDN pour l'instant)
- Google Fonts (Inter)

### 2. Structure des fichiers
```
templates/
├── base_figma_exact.html    # Template de base avec style Figma
├── figma_style.html         # Page de démonstration
└── exemple_figma.html       # Exemple complet

static/
└── css/
    └── tailwind.css         # Styles personnalisés
```

## 🎯 Caractéristiques du Style Figma

### Couleurs principales
- **Gradient principal** : `from-blue-600 via-purple-600 to-indigo-600`
- **Fond** : `bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50`
- **Header** : `bg-white/95 backdrop-blur`

### Composants clés
- **Boutons** : Gradients avec hover effects
- **Badges** : Couleurs par rôle utilisateur
- **Cartes** : Ombres douces et bordures arrondies
- **Navigation** : Sidebar avec backdrop-blur

## 📱 Utilisation

### 1. Template de base
Utilisez `base_figma_exact.html` comme template de base :

```html
{% extends 'base_figma_exact.html' %}
{% load static %}

{% block title %}Ma Page{% endblock %}

{% block content %}
<!-- Votre contenu ici -->
{% endblock %}
```

### 2. Classes CSS disponibles

#### Boutons
```html
<!-- Bouton principal avec gradient -->
<button class="inline-flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 text-white hover:from-blue-700 hover:via-purple-700 hover:to-indigo-700 transition-all duration-200 shadow-md">
    Bouton Principal
</button>

<!-- Bouton contour -->
<button class="inline-flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 transition-all duration-200">
    Bouton Contour
</button>

<!-- Bouton fantôme -->
<button class="inline-flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md text-gray-700 hover:bg-gray-50 transition-all duration-200">
    Bouton Fantôme
</button>
```

#### Badges
```html
<!-- Badge Superadmin -->
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gradient-to-r from-red-500 to-pink-500 text-white">
    Superadmin
</span>

<!-- Badge IT Manager -->
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gradient-to-r from-blue-500 to-cyan-500 text-white">
    IT Manager
</span>

<!-- Badge Bureau Manager -->
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gradient-to-r from-purple-500 to-violet-500 text-white">
    Bureau Manager
</span>

<!-- Badge Employé -->
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border border-orange-300 text-orange-600 bg-transparent">
    Employé
</span>
```

#### Cartes
```html
<div class="bg-white rounded-lg shadow-card border border-gray-200 p-6">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">Titre de la carte</h3>
    <p class="text-gray-600">Contenu de la carte</p>
</div>
```

#### Titres avec gradient
```html
<h1 class="text-4xl font-bold text-gradient mb-2">Titre avec gradient</h1>
```

#### Messages d'alerte
```html
<!-- Succès -->
<div class="p-4 rounded-lg border bg-green-50 border-green-200 text-green-800">
    <div class="flex items-center space-x-3">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <span>Message de succès</span>
    </div>
</div>

<!-- Erreur -->
<div class="p-4 rounded-lg border bg-red-50 border-red-200 text-red-800">
    <div class="flex items-center space-x-3">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <span>Message d'erreur</span>
    </div>
</div>
```

## 🎨 Personnalisation

### Ajouter de nouvelles couleurs
Dans le fichier `base_figma_exact.html`, modifiez la configuration Tailwind :

```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                // Vos nouvelles couleurs ici
                custom: {
                    50: '#f0f9ff',
                    500: '#0ea5e9',
                    600: '#0284c7',
                }
            }
        }
    }
}
```

### Créer de nouveaux composants
Ajoutez vos styles personnalisés dans la section `<style>` :

```css
.my-custom-component {
    @apply bg-white rounded-lg shadow-card border border-gray-200 p-6;
}

.my-custom-button {
    @apply inline-flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md bg-gradient-to-r from-custom-500 to-custom-600 text-white hover:from-custom-600 hover:to-custom-700 transition-all duration-200;
}
```

## 📊 Exemples d'utilisation

### Page de tableau de bord
```html
{% extends 'base_figma_exact.html' %}

{% block content %}
<div class="space-y-8">
    <!-- Titre -->
    <div class="mb-8">
        <h1 class="text-4xl font-bold text-gradient mb-2">Tableau de bord</h1>
        <p class="text-gray-600">Vue d'ensemble de votre parc informatique</p>
    </div>

    <!-- Cartes KPI -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="bg-white rounded-lg shadow-card border border-gray-200 p-6">
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-sm font-medium text-gray-600">Total Équipements</p>
                    <p class="text-2xl font-bold text-gray-900">1,247</p>
                </div>
                <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                    </svg>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Formulaire
```html
<div class="bg-white rounded-lg shadow-card border border-gray-200 p-6">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">Ajouter un équipement</h3>
    
    <form class="space-y-4">
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nom de l'équipement</label>
            <input type="text" class="w-full px-3 py-2 border border-gray-200 rounded-md bg-gray-50/50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
        </div>
        
        <div class="flex gap-3">
            <button type="submit" class="inline-flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 text-white hover:from-blue-700 hover:via-purple-700 hover:to-indigo-700 transition-all duration-200 shadow-md">
                Enregistrer
            </button>
            <button type="button" class="inline-flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 transition-all duration-200">
                Annuler
            </button>
        </div>
    </form>
</div>
```

## 🔧 Développement

### Tester le style
1. Lancez le serveur Django : `python manage.py runserver`
2. Visitez : `http://127.0.0.1:8000/figma-style/`
3. Comparez avec votre prototype Figma

### Optimisation
- Pour la production, compilez Tailwind CSS localement
- Optimisez les images et icônes
- Testez sur différents navigateurs

## 📝 Notes importantes

1. **Responsive** : Le design est responsive par défaut
2. **Accessibilité** : Utilisez les attributs ARIA appropriés
3. **Performance** : Le CDN Tailwind est utilisé pour le développement
4. **Compatibilité** : Testé sur Chrome, Firefox, Safari

## 🎯 Prochaines étapes

1. Appliquer le style à toutes les pages existantes
2. Créer des composants réutilisables
3. Optimiser pour la production
4. Ajouter des animations personnalisées

---

**Version** : 1.0.0  
**Dernière mise à jour** : 20 août 2024  
**Auteur** : Équipe ParcInfo
