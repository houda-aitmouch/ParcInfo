"""
Composants réutilisables pour le Dashboard Garantie
"""

import streamlit as st
from datetime import datetime
from theme_config import COLORS, GRADIENTS, SHADOWS, ICONS, METRICS_CONFIG, ALERT_MESSAGES

def render_header(title, subtitle=None, icon="🛡️"):
    """Affiche un header professionnel"""
    st.markdown(f"""
    <div class="main-header">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <span style="font-size: 3em; margin-right: 20px;">{icon}</span>
            <div>
                <h1>{title}</h1>
                {f'<p>{subtitle}</p>' if subtitle else ''}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_metric_card(value, label, icon, color=None, trend=None):
    """Affiche une carte de métrique moderne"""
    if color is None:
        color = COLORS['primary']['main']
    
    trend_html = ""
    if trend:
        trend_icon = "📈" if trend > 0 else "📉"
        trend_color = COLORS['success']['main'] if trend > 0 else COLORS['danger']['main']
        trend_html = f"""
        <div style="font-size: 0.75rem; color: {trend_color}; margin-top: 0.5rem;">
            {trend_icon} {abs(trend)}% vs mois précédent
        </div>
        """
    
    st.markdown(f"""
    <div class="metric-container">
        <span class="metric-icon">{icon}</span>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {trend_html}
    </div>
    """, unsafe_allow_html=True)

def render_alert(alert_type, count, description=None):
    """Affiche une alerte stylisée"""
    config = ALERT_MESSAGES.get(alert_type, ALERT_MESSAGES['info'])
    
    if description is None:
        description = config['description']
    
    st.markdown(f"""
    <div class="alert-{alert_type}">
        <div style="display: flex; align-items: center; justify-content: center;">
            <span style="font-size: 2.5em; margin-right: 15px;">{config['icon']}</span>
            <div style="text-align: center;">
                <h2 style="margin: 0; font-size: 1.8em; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                    {count} {config['title']}
                </h2>
                <p style="margin: 10px 0 0 0; font-size: 1.1em; opacity: 0.95;">
                    {description}
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_section_header(title, subtitle=None, icon="📊"):
    """Affiche un en-tête de section"""
    st.markdown(f"""
    <div class="section-header">
        <div class="section-title">
            <span style="margin-right: 10px;">{icon}</span>
            {title}
        </div>
        {f'<div class="section-subtitle">{subtitle}</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def render_chart_card(title, chart, height=400):
    """Affiche une carte contenant un graphique"""
    st.markdown(f"""
    <div class="chart-card">
        <div class="chart-title">{title}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})

def render_user_info(username, role, date=None):
    """Affiche les informations utilisateur"""
    if date is None:
        date = datetime.now().strftime('%d/%m/%Y')
    
    role_config = {
        'super_admin': {'name': 'Super Admin', 'icon': '👑', 'color': COLORS['primary']['main']},
        'gestionnaire_info': {'name': 'Gestionnaire Info', 'icon': ICONS['computer'], 'color': COLORS['info']['main']},
        'gestionnaire_bureau': {'name': 'Gestionnaire Bureau', 'icon': ICONS['office'], 'color': COLORS['secondary']['main']},
        'employe': {'name': 'Employé', 'icon': ICONS['user'], 'color': COLORS['text']['secondary']}
    }
    
    role_info = role_config.get(role, {'name': role, 'icon': ICONS['user'], 'color': COLORS['text']['secondary']})
    
    col1, col2, col3 = st.columns(3)
    with col1:
        render_metric_card(username, "Utilisateur", ICONS['user'])
    with col2:
        render_metric_card(role_info['name'], "Rôle", role_info['icon'])
    with col3:
        render_metric_card(date, "Date", ICONS['calendar'])

def render_navigation_tabs(tabs, active_tab=None):
    """Affiche une navigation par onglets"""
    if active_tab is None:
        active_tab = tabs[0]['key']
    
    tab_html = ""
    for tab in tabs:
        is_active = "active" if tab['key'] == active_tab else ""
        tab_html += f"""
        <div class="nav-tab {is_active}" onclick="document.querySelector('[data-tab=\'{tab["key"]}\']').click()">
            {tab['icon']} {tab['label']}
        </div>
        """
    
    st.markdown(f"""
    <div class="nav-tabs">
        {tab_html}
    </div>
    """, unsafe_allow_html=True)
    
    # Créer les onglets Streamlit cachés
    tab_labels = [tab['label'] for tab in tabs]
    selected_tab = st.tabs(tab_labels)
    
    return selected_tab

def render_filters(filters):
    """Affiche des filtres interactifs"""
    st.markdown("""
    <div class="filter-container">
        <div class="filter-row">
    """, unsafe_allow_html=True)
    
    cols = st.columns(len(filters))
    values = {}
    
    for i, (key, config) in enumerate(filters.items()):
        with cols[i]:
            st.markdown(f"""
            <div class="filter-item">
                <label class="filter-label">{config['label']}</label>
            </div>
            """, unsafe_allow_html=True)
            
            if config['type'] == 'select':
                values[key] = st.selectbox(
                    config['label'],
                    options=config['options'],
                    key=f"filter_{key}"
                )
            elif config['type'] == 'multiselect':
                values[key] = st.multiselect(
                    config['label'],
                    options=config['options'],
                    key=f"filter_{key}"
                )
            elif config['type'] == 'date':
                values[key] = st.date_input(
                    config['label'],
                    key=f"filter_{key}"
                )
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    return values

def render_data_table(df, title=None, show_filters=True):
    """Affiche un tableau de données avec style moderne"""
    if title:
        render_section_header(title)
    
    if show_filters and not df.empty:
        # Filtres rapides
        col1, col2, col3 = st.columns(3)
        with col1:
            if 'Type' in df.columns:
                selected_types = st.multiselect(
                    "Filtrer par type",
                    options=df['Type'].unique(),
                    default=df['Type'].unique()
                )
                df = df[df['Type'].isin(selected_types)]
        
        with col2:
            if 'Fournisseur' in df.columns:
                selected_fournisseurs = st.multiselect(
                    "Filtrer par fournisseur",
                    options=df['Fournisseur'].unique(),
                    default=df['Fournisseur'].unique()
                )
                df = df[df['Fournisseur'].isin(selected_fournisseurs)]
        
        with col3:
            if 'Statut' in df.columns:
                selected_statuts = st.multiselect(
                    "Filtrer par statut",
                    options=df['Statut'].unique(),
                    default=df['Statut'].unique()
                )
                df = df[df['Statut'].isin(selected_statuts)]
    
    if not df.empty:
        # Configuration des colonnes pour un meilleur affichage
        column_config = {}
        
        if 'Jours Restants' in df.columns:
            column_config['Jours Restants'] = st.column_config.NumberColumn(
                "Jours Restants",
                help="Nombre de jours restants avant expiration",
                format="%d jours"
            )
        
        if 'Fin Garantie' in df.columns:
            column_config['Fin Garantie'] = st.column_config.DateColumn(
                "Fin Garantie",
                format="DD/MM/YYYY"
            )
        
        if 'Date Commande' in df.columns:
            column_config['Date Commande'] = st.column_config.DateColumn(
                "Date Commande",
                format="DD/MM/YYYY"
            )
        
        if 'Date Réception' in df.columns:
            column_config['Date Réception'] = st.column_config.DateColumn(
                "Date Réception",
                format="DD/MM/YYYY"
            )
        
        st.dataframe(
            df,
            use_container_width=True,
            column_config=column_config,
            hide_index=True
        )
        
        # Statistiques du tableau
        st.markdown(f"""
        <div style="text-align: center; margin-top: 1rem; color: {COLORS['text']['secondary']}; font-size: 0.875rem;">
            📊 {len(df)} élément(s) affiché(s)
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("📭 Aucune donnée à afficher avec les filtres actuels")

def render_summary_cards(df):
    """Affiche des cartes de résumé des données"""
    if df.empty:
        return
    
    # Calculs des métriques
    total = len(df)
    en_garantie = len(df[df['Statut'] == 'En Garantie']) if 'Statut' in df.columns else 0
    expirees = len(df[df['Statut'] == 'Garantie Expirée']) if 'Statut' in df.columns else 0
    
    df_valid = df[df['Jours Restants'].notna()].copy() if 'Jours Restants' in df.columns else df
    critiques = len(df_valid[(df_valid['Jours Restants'] > 0) & (df_valid['Jours Restants'] <= 15)]) if not df_valid.empty else 0
    urgentes = len(df_valid[(df_valid['Jours Restants'] > 15) & (df_valid['Jours Restants'] <= 30)]) if not df_valid.empty else 0
    
    # Affichage des métriques
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        render_metric_card(total, "Total", METRICS_CONFIG['total_commandes']['icon'])
    
    with col2:
        render_metric_card(en_garantie, "En Garantie", METRICS_CONFIG['en_garantie']['icon'])
    
    with col3:
        render_metric_card(expirees, "Expirées", METRICS_CONFIG['expirees']['icon'])
    
    with col4:
        render_metric_card(critiques, "Critiques", METRICS_CONFIG['critiques']['icon'])
    
    with col5:
        render_metric_card(urgentes, "Urgentes", METRICS_CONFIG['urgentes']['icon'])

def render_loading_spinner(message="Chargement..."):
    """Affiche un spinner de chargement stylisé"""
    st.markdown(f"""
    <div class="loading">
        {ICONS['loading']} {message}
    </div>
    """, unsafe_allow_html=True)

def render_empty_state(title, description, icon="📭"):
    """Affiche un état vide stylisé"""
    st.markdown(f"""
    <div style="text-align: center; padding: 3rem; color: {COLORS['text']['secondary']};">
        <div style="font-size: 4rem; margin-bottom: 1rem;">{icon}</div>
        <h3 style="margin-bottom: 0.5rem; color: {COLORS['text']['primary']};">{title}</h3>
        <p style="margin: 0;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Affiche un footer professionnel"""
    st.markdown("""
    <div class="dashboard-footer">
        <p>© 2024 ParcInfo - Système de Gestion des Garanties | Développé avec Streamlit & Django</p>
        <p style="font-size: 0.75rem; margin-top: 0.5rem; opacity: 0.7;">
            🛡️ Surveillance en temps réel des garanties d'équipements
        </p>
    </div>
    """, unsafe_allow_html=True)
