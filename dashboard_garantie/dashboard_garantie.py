import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import sys
import django
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page Streamlit sera faite dans la fonction main()

# Chargement des styles CSS personnalisés
def load_custom_css():
    with open('custom_styles.css', 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Configuration Django sera faite dans la fonction main()

def calculate_garantie_end_date(date_reception, duree_valeur, duree_unite):
    """Calcule la date de fin de garantie"""
    if not date_reception:
        return None
    
    if duree_unite == 'jour':
        return date_reception + timedelta(days=duree_valeur)
    elif duree_unite == 'mois':
        # Approximation simple pour les mois
        return date_reception + timedelta(days=duree_valeur * 30)
    elif duree_unite == 'annee':
        return date_reception + timedelta(days=duree_valeur * 365)
    return None

# Cette fonction sera définie dans la fonction main() après la configuration Django

# Ces fonctions seront définies dans la fonction main() après la configuration Django

def create_garantie_chart(df, title):
    """Crée un graphique intelligent pour les durées de garantie avec règles de visualisation"""
    if df.empty:
        return None
    
    # Filtrer les données valides
    df_valid = df[df['Jours Restants'].notna()].copy()
    
    if df_valid.empty:
        return None
    
    # Catégoriser les garanties par urgence avec nuances améliorées
    def categorize_urgency(jours):
        if jours <= 0:
            return 'Expirée'
        elif jours <= 15:
            return 'Urgente (≤15j)'
        elif jours <= 30:
            return 'Attention (≤30j)'
        elif jours <= 90:
            return 'Normale (≤90j)'
        else:
            return 'Longue (>90j)'
    
    df_valid['Urgence'] = df_valid['Jours Restants'].apply(categorize_urgency)
    
    # Palette de couleurs standardisée selon les recommandations
    color_map = {
        'Expirée': '#DC3545',           # Rouge critique (< 15 jours)
        'Urgente (≤15j)': '#F39C12',    # Orange (15-30 jours)
        'Attention (≤30j)': '#FFC107',  # Jaune (30-90 jours)
        'Normale (≤90j)': '#17A2B8',    # Bleu (90 jours - 1 an)
        'Longue (>90j)': '#28A745'      # Vert sécurisé (> 30 jours)
    }
    
    # Trier par urgence et jours restants
    urgency_order = ['Expirée', 'Urgente (≤15j)', 'Attention (≤30j)', 'Normale (≤90j)', 'Longue (>90j)']
    df_valid['Urgence'] = pd.Categorical(df_valid['Urgence'], categories=urgency_order, ordered=True)
    df_valid = df_valid.sort_values(['Urgence', 'Jours Restants'])
    
    # Créer un bar chart vertical pour comparaison claire des jours restants
    fig = px.bar(
        df_valid,
        x='Numéro',  # Axe X pour les commandes/équipements
        y='Jours Restants',  # Axe Y pour les jours restants
        color='Urgence',
        title=f"{title} - Jours Restants de Garantie par Commande",
        labels={
            'Jours Restants': 'Jours Restants de Garantie',
            'Numéro': 'Commande/Équipement',
            'Urgence': 'Niveau d\'Urgence'
        },
        color_discrete_map=color_map,
        hover_data=['Fournisseur', 'Fin Garantie', 'Type', 'Jours Restants'],
        text='Jours Restants'  # Afficher les valeurs sur les barres
    )
    
    # Améliorer la présentation avec échelle claire et légende
    fig.update_layout(
        height=500,
        showlegend=True,
        legend_title="Niveau d'Urgence",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.1)',
            borderwidth=1
        ),
        xaxis_title="Commande/Équipement",
        yaxis_title="Jours Restants de Garantie",
        yaxis=dict(
            range=[0, max(df_valid['Jours Restants'].max() + 10, 30)],  # Échelle claire 0-30 jours
            tickmode='linear',
            tick0=0,
            dtick=5  # Graduations tous les 5 jours
        ),
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Améliorer l'affichage des valeurs sur les barres
    fig.update_traces(
        texttemplate='%{text} jours',
        textposition='outside',
        textfont=dict(size=10, color='black')
    )
    
    # Ajouter des lignes de référence avec annotations plus visibles
    fig.add_hline(y=15, line_dash="dash", line_color="#ff6b35", 
                  annotation_text="Seuil critique (15 jours)",
                  annotation_position="top right")
    fig.add_hline(y=30, line_dash="dash", line_color="orange", 
                  annotation_text="Seuil d'attention (30 jours)",
                  annotation_position="top right")
    fig.add_hline(y=0, line_dash="solid", line_color="red", 
                  annotation_text="Garantie expirée",
                  annotation_position="bottom right")
    
    return fig

def create_timeline_chart(df, title):
    """Crée un graphique temporel intelligent des garanties"""
    if df.empty:
        return None
    
    df_valid = df[df['Fin Garantie'].notna()].copy()
    
    if df_valid.empty:
        return None
    
    # Ajouter une colonne pour l'urgence temporelle
    today = datetime.now().date()
    def get_temporal_urgency(row):
        fin_garantie = row['Fin Garantie']
        if pd.isna(fin_garantie):
            return 'Normale'
        if fin_garantie < today:
            return 'Expirée'
        elif fin_garantie <= today + timedelta(days=30):
            return 'Urgente'
        elif fin_garantie <= today + timedelta(days=90):
            return 'Attention'
        else:
            return 'Normale'
    
    df_valid['Urgence Temporelle'] = df_valid.apply(get_temporal_urgency, axis=1)
    
    # Couleurs pour l'urgence temporelle avec meilleure accessibilité
    color_map = {
        'Expirée': '#dc3545',      # Rouge critique
        'Urgente': '#ff6b35',      # Orange vif (plus visible)
        'Attention': '#ffa726',    # Orange clair (meilleur contraste)
        'Normale': '#28a745'       # Vert sécurisé
    }
    
    # Trier par date de fin de garantie
    df_valid = df_valid.sort_values('Fin Garantie')
    
    # Créer un line chart avec données réelles et cohérentes
    # S'assurer que 'Fin Garantie' est au format datetime
    df_valid['Fin Garantie'] = pd.to_datetime(df_valid['Fin Garantie'], errors='coerce')
    
    # Calculer le nombre de garanties expirant par date
    df_valid['Date_Expiration'] = df_valid['Fin Garantie'].dt.date
    expiration_counts = df_valid['Date_Expiration'].value_counts().sort_index()
    
    # Créer le line chart avec des données réelles
    fig = px.line(
        x=expiration_counts.index,
        y=expiration_counts.values,
        title=f"{title} - Nombre de Garanties Expirant par Date",
        labels={'x': 'Date d\'Expiration', 'y': 'Nombre de Garanties'},
        markers=True,  # Points marqués pour les dates critiques
        line_shape='linear'
    )
    
    # Améliorer la lisibilité du line chart
    fig.update_layout(
        height=400,
        xaxis_title="Date d'Expiration",
        yaxis_title="Nombre de Garanties",
        yaxis=dict(
            range=[0, max(expiration_counts.values) + 1],  # Échelle adaptée aux données réelles
            tickmode='linear',
            tick0=0,
            dtick=1  # Graduations par unité
        ),
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Améliorer la présentation
    fig.update_layout(
        height=600,
        showlegend=True,
        legend_title="Urgence Temporelle",
        xaxis_title="Période de Garantie",
        yaxis_title="Commandes",
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Note: Les lignes de référence sont omises pour éviter les problèmes de compatibilité
    # avec les graphiques timeline de Plotly
    
    return fig

def create_garantie_timeline_dashboard(df, title, dashboard_type=None):
    """Crée un tableau de bord complet pour le suivi des dates de fin de garantie"""
    if df.empty:
        return None
    
    df_valid = df[df['Jours Restants'].notna()].copy()
    
    if df_valid.empty:
        return None
    
    # Calculer les statistiques globales
    total_commandes = len(df_valid)
    commandes_expirees = len(df_valid[df_valid['Jours Restants'] <= 0])
    commandes_critiques = len(df_valid[(df_valid['Jours Restants'] > 0) & (df_valid['Jours Restants'] <= 15)])
    commandes_urgentes = len(df_valid[(df_valid['Jours Restants'] > 15) & (df_valid['Jours Restants'] <= 30)])
    
    # Créer un conteneur pour le tableau de bord
    dashboard_container = st.container()
    
    with dashboard_container:

        

        
        # Alertes visuelles professionnelles

        
        # Section 1: Timeline des garanties (Gantt-like)
        st.markdown("""
        <div class="section-header">
            <div class="section-title">
                        <svg style="width: 24px; height: 24px; margin-right: 10px; fill: currentColor;" viewBox="0 0 24 24">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
        </svg>
                Chronologie des Garanties
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Préparer les données pour la timeline
        df_timeline = df_valid.copy()
        df_timeline['Fin Garantie'] = pd.to_datetime(df_timeline['Fin Garantie'], errors='coerce')
        df_timeline = df_timeline.sort_values('Fin Garantie')
        
        # Créer un graphique de type Gantt pour les garanties
        fig_timeline = go.Figure()
        
        # Couleurs professionnelles selon l'urgence
        def get_timeline_color(jours):
            if jours <= 0:
                return '#ef4444'  # Rouge professionnel pour expiré
            elif jours <= 15:
                return '#f97316'  # Orange professionnel pour critique
            elif jours <= 30:
                return '#eab308'  # Jaune professionnel pour urgent
            elif jours <= 90:
                return '#3b82f6'  # Bleu professionnel pour attention
            else:
                return '#10b981'  # Vert professionnel pour OK
        
        # Ajouter des barres pour chaque garantie
        for idx, row in df_timeline.iterrows():
            if pd.notna(row['Fin Garantie']):
                color = get_timeline_color(row['Jours Restants'])
                fig_timeline.add_trace(go.Bar(
                    x=[row['Fin Garantie']],
                    y=[row['Numéro']],
                    orientation='h',
                    marker_color=color,
                    name=row['Numéro'],
                    hovertemplate=f"<b>{row['Numéro']}</b><br>" +
                                 f"Fournisseur: {row['Fournisseur']}<br>" +
                                 f"Fin garantie: {row['Fin Garantie'].strftime('%d/%m/%Y')}<br>" +
                                 f"Jours restants: {row['Jours Restants']}<br>" +
                                 f"Type: {row['Type']}<extra></extra>",
                    showlegend=False
                ))
        
        fig_timeline.update_layout(
            title=dict(
                text="Chronologie des Dates de Fin de Garantie",
                font=dict(size=20, color='#1e293b', family='Inter, SF Pro Display, system-ui, sans-serif'),
                x=0.5,
                xanchor='center'
            ),
            xaxis_title=dict(
                text="Date de Fin de Garantie",
                font=dict(size=15, color='#334155', weight=600)
            ),
            yaxis_title=dict(
                text="Numéro de Commande",
                font=dict(size=15, color='#334155', weight=600)
            ),
            height=500,
            showlegend=False,
            plot_bgcolor='rgba(248, 250, 252, 0.9)',
            paper_bgcolor='rgba(255, 255, 255, 0.95)',
            margin=dict(l=70, r=70, t=90, b=70),
            font=dict(family='Inter, SF Pro Display, system-ui, sans-serif'),
            xaxis=dict(
                gridcolor='rgba(226, 232, 240, 0.5)',
                zerolinecolor='rgba(226, 232, 240, 0.8)',
                linecolor='rgba(226, 232, 240, 0.8)'
            ),
            yaxis=dict(
                gridcolor='rgba(226, 232, 240, 0.5)',
                zerolinecolor='rgba(226, 232, 240, 0.8)',
                linecolor='rgba(226, 232, 240, 0.8)'
            )
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Section 2: Analyse par fournisseur
        # Déterminer le type de données pour adapter le titre
        if dashboard_type == 'all':
            data_type = "Toutes"
            subtitle = "Comparaison des garanties et performance par fournisseur - Toutes les commandes"
        elif dashboard_type is None:
            # Détection automatique basée sur les données
            if len(df_valid['Type'].unique()) > 1:
                data_type = "Toutes"
                subtitle = "Comparaison des garanties et performance par fournisseur - Toutes les commandes"
            else:
                data_type = df_valid['Type'].iloc[0] if not df_valid.empty else "Toutes"
                subtitle = f"Comparaison des garanties et performance par fournisseur - Commandes {data_type}"
        else:
            data_type = "Informatique" if df_valid['Type'].iloc[0] == 'Informatique' else "Bureautique"
            subtitle = f"Comparaison des garanties et performance par fournisseur - Commandes {data_type}"
        
        st.markdown(f"""
        <div class="section-header">
            <div class="section-title">
                Analyse par Fournisseur ({data_type})
            </div>
            <div class="section-subtitle">
                {subtitle}
            </div>
        </div>
        
        """, unsafe_allow_html=True)
        
        # Statistiques par fournisseur
        if not df_valid.empty and 'Fournisseur' in df_valid.columns:
        fournisseur_stats = df_valid.groupby('Fournisseur').agg({
            'Jours Restants': ['count', 'mean', 'min']
        }).round(1)
        
        # Aplatir les colonnes multi-niveaux
        fournisseur_stats.columns = ['Nombre_Commandes', 'Moyenne_Jours', 'Min_Jours']
        fournisseur_stats = fournisseur_stats.reset_index()
            
            # Vérifier qu'il y a des données à afficher
            if fournisseur_stats.empty:
                st.info("Aucune donnée de fournisseur disponible pour l'analyse.")
                return
        else:
            st.info("Données insuffisantes pour l'analyse par fournisseur.")
            return
        
        # Graphique en barres horizontales pour les fournisseurs
        graph_title = f"Répartition des Commandes par Fournisseur" if data_type == "Toutes" else f"Répartition des Commandes {data_type} par Fournisseur"
        
        fig_fournisseur = px.bar(
            fournisseur_stats,
            y='Fournisseur',
            x='Nombre_Commandes',
            title=graph_title,
            color='Moyenne_Jours',
            color_continuous_scale='RdYlGn_r',  # Rouge pour peu de jours, vert pour beaucoup
            orientation='h',
            hover_data=['Moyenne_Jours', 'Min_Jours'],
            text='Nombre_Commandes'  # Afficher les valeurs sur les barres
        )
        
        fig_fournisseur.update_layout(
            height=500,
            title=dict(
                text=graph_title,
                font=dict(size=20, color='#1e293b', family='Inter, SF Pro Display, system-ui, sans-serif'),
                x=0.5,
                xanchor='center'
            ),
            coloraxis_colorbar_title=dict(
                text="Moyenne Jours Restants",
                font=dict(size=13, color='#334155', weight=600)
            ),
            xaxis_title=dict(
                text="Nombre de Commandes",
                font=dict(size=15, color='#334155', weight=600)
            ),
            yaxis_title=dict(
                text="Fournisseur",
                font=dict(size=15, color='#334155', weight=600)
            ),
            margin=dict(l=70, r=70, t=90, b=70),
            plot_bgcolor='rgba(248, 250, 252, 0.9)',
            paper_bgcolor='rgba(255, 255, 255, 0.95)',
            font=dict(family='Inter, SF Pro Display, system-ui, sans-serif'),
            # Améliorer l'échelle de l'axe X
            xaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=1,  # Graduations par unité
                range=[0, max(fournisseur_stats['Nombre_Commandes']) + 1],  # Échelle adaptée aux données
                gridcolor='rgba(226, 232, 240, 0.5)',
                zerolinecolor='rgba(226, 232, 240, 0.8)',
                linecolor='rgba(226, 232, 240, 0.8)',
                showgrid=True,
                gridwidth=1,
                showline=True,
                linewidth=1,
                tickfont=dict(size=12, color='#334155'),
                tickformat='d'  # Format entier
            ),
            yaxis=dict(
                gridcolor='rgba(226, 232, 240, 0.5)',
                zerolinecolor='rgba(226, 232, 240, 0.8)',
                linecolor='rgba(226, 232, 240, 0.8)'
            )
        )
        
        # Améliorer l'affichage des valeurs sur les barres
        fig_fournisseur.update_traces(
            texttemplate='%{text}',
            textposition='outside',
            textfont=dict(size=12, color='#2c3e50')
        )
        
        st.plotly_chart(fig_fournisseur, use_container_width=True)
        
        # Section 3: Tableau détaillé avec formatage conditionnel
        st.markdown("""
        <div class="section-header">
            <div class="section-title">
                Détail des Commandes
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Préparer le tableau avec formatage conditionnel
        df_display = df_valid[['Numéro', 'Type', 'Fournisseur', 'Date Réception', 'Fin Garantie', 'Jours Restants']].copy()
        
        # Ajouter une colonne de statut coloré avec badges ultra-professionnels
        def get_status_badge(row):
            jours = row['Jours Restants']
            if jours <= 0:
                return 'EXPIRÉE'
            elif jours <= 15:
                return 'CRITIQUE'
            elif jours <= 30:
                return 'URGENTE'
            elif jours <= 90:
                return 'ATTENTION'
            else:
                return 'SÉCURISÉ'
        
        df_display['Statut'] = df_display.apply(get_status_badge, axis=1)
        
        # Convertir le nombre de commandes en entier pour un affichage plus logique
        df_display['Jours Restants'] = df_display['Jours Restants'].astype(int)
        
        # Afficher le tableau avec style professionnel
        st.dataframe(
            df_display,
            use_container_width=True,
            column_config={
                "Jours Restants": st.column_config.NumberColumn(
                    "Jours Restants",
                    help="Nombre de jours restants avant expiration",
                    format="%d jours",
                    min_value=0
                ),
                "Date Réception": st.column_config.DateColumn(
                    "Date Réception",
                    format="DD/MM/YYYY"
                ),
                "Fin Garantie": st.column_config.DateColumn(
                    "Fin Garantie",
                    format="DD/MM/YYYY"
                ),
                "Statut": st.column_config.TextColumn(
                    "Statut",
                    help="Niveau d'urgence de la garantie"
                )
            }
        )
    
    return dashboard_container

def create_fournisseur_analysis(df, title):
    """Crée une analyse par fournisseur"""
    if df.empty:
        return None
    
    df_valid = df[df['Jours Restants'].notna()].copy()
    
    if df_valid.empty:
        return None
    
    # Analyser par fournisseur
    fournisseur_stats = df_valid.groupby('Fournisseur').agg({
        'Jours Restants': ['count', 'mean', 'min'],
        'Numéro': 'count'
    }).round(1)
    
    fournisseur_stats.columns = ['Nombre_Commandes', 'Moyenne_Jours', 'Min_Jours']
    fournisseur_stats = fournisseur_stats.reset_index()
    
    # Créer un graphique en barres HORIZONTALES pour les fournisseurs (plus lisible)
    fig = px.bar(
        fournisseur_stats,
        y='Fournisseur',  # Axe Y pour les noms de fournisseurs
        x='Nombre_Commandes',  # Axe X pour les valeurs
        title=f"{title} - Analyse par Fournisseur",
        labels={'Nombre_Commandes': 'Nombre de Commandes', 'Fournisseur': 'Fournisseur'},
        color='Moyenne_Jours',
        color_continuous_scale='RdYlGn_r',  # Rouge pour peu de jours, vert pour beaucoup
        hover_data=['Moyenne_Jours', 'Min_Jours'],
        orientation='h'  # Barres horizontales pour une meilleure lisibilité
    )
    
    fig.update_layout(
        height=500,
        coloraxis_colorbar_title="Moyenne Jours Restants",
        xaxis_title="Nombre de Commandes",
        yaxis_title="Fournisseur"
    )
    
    return fig

def create_monthly_expiration_chart(df, title):
    """Crée un histogramme des expirations par mois pour voir les pics"""
    if df.empty:
        return None
    
    df_valid = df[df['Fin Garantie'].notna()].copy()
    
    if df_valid.empty:
        return None
    
    # Extraire le mois et l'année de fin de garantie
    df_valid['Mois_Expiration'] = df_valid['Fin Garantie'].dt.to_period('M')
    df_valid['Mois_Expiration_Str'] = df_valid['Mois_Expiration'].astype(str)
    
    # Compter les expirations par mois
    monthly_expirations = df_valid['Mois_Expiration_Str'].value_counts().sort_index()
    
    # Créer un histogramme pour voir les pics d'expiration
    fig = px.bar(
        x=monthly_expirations.index,
        y=monthly_expirations.values,
        title=f"{title} - Histogramme des Expirations par Mois",
        labels={'x': 'Mois d\'Expiration', 'y': 'Nombre d\'Équipements'},
        color=monthly_expirations.values,
        color_continuous_scale='RdYlGn_r'  # Rouge pour beaucoup, vert pour peu
    )
    
    # Améliorer la présentation
    fig.update_layout(
        height=400,
        xaxis_title="Mois d'Expiration",
        yaxis_title="Nombre d'Équipements",
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        coloraxis_colorbar_title="Intensité"
    )
    
    return fig

def display_colored_dataframe(df, title):
    """Affiche un tableau enrichi avec couleurs selon les règles de data visualization"""
    if df.empty:
        st.info("Aucune donnée à afficher")
        return
    
    st.subheader(f"{title}")
    
    # Créer une copie pour l'affichage
    df_display = df.copy()
    
    # Ajouter une colonne de statut coloré avec badges améliorés
    def get_status_color(row):
        jours_restants = row['Jours Restants']
        if pd.isna(jours_restants):
            return 'Non défini'
        elif jours_restants < 0:
            return 'EXPIRÉE'
        elif jours_restants <= 15:
            return 'URGENTE'
        elif jours_restants <= 30:
            return 'ATTENTION'
        else:
            return 'OK'
    
    df_display['Statut Coloré'] = df_display.apply(get_status_color, axis=1)
    
    # Réorganiser les colonnes pour une meilleure lisibilité
    columns_order = ['Numéro', 'Type', 'Fournisseur', 'Date Réception', 'Fin Garantie', 'Jours Restants', 'Statut Coloré']
    df_display = df_display[columns_order]
    
    # Afficher le tableau avec style
    st.dataframe(
        df_display,
        use_container_width=True,
        column_config={
            "Jours Restants": st.column_config.NumberColumn(
                "Jours Restants",
                help="Nombre de jours restants avant expiration",
                format="%d jours"
            ),
            "Date Réception": st.column_config.DateColumn(
                "Date Réception",
                format="DD/MM/YYYY"
            ),
            "Fin Garantie": st.column_config.DateColumn(
                "Fin Garantie",
                format="DD/MM/YYYY"
            )
        }
    )

# Cette fonction sera définie dans la fonction main() après la configuration Django

def main():
    st.set_page_config(
        page_title="Dashboard Garantie - ParcInfo",
        page_icon="",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://docs.streamlit.io/',
            'Report a bug': None,
            'About': 'Dashboard de suivi des garanties ParcInfo'
        }
    )
    
    # Configuration Django AVANT tous les imports Django
    # Ajouter le répertoire parent au path pour que Django trouve les paramètres
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
    django.setup()
    
    # Import des modèles Django APRÈS la configuration
    from django.db import connection
    from django.contrib.auth.models import Group, User
    from django.contrib.auth import authenticate
    from apps.commande_bureau.models import CommandeBureau
    from apps.commande_informatique.models import Commande
    from apps.fournisseurs.models import Fournisseur
    
    # Charger les styles CSS personnalisés
    try:
        load_custom_css()
    except FileNotFoundError:
        st.warning("Fichier CSS personnalisé non trouvé. Utilisation des styles par défaut.")
    
    # Configuration du thème professionnel ultra-moderne
    st.markdown("""
    <style>
    /* Configuration globale ultra-moderne et professionnelle */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 50%, #f1f5f9 100%);
        font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #1e293b;
        line-height: 1.6;
        min-height: 100vh;
    }
    
    /* Scrollbar personnalisée */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(241, 245, 249, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #60a5fa, #3b82f6);
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
    }
    
    /* Header principal ultra-moderne et professionnel */
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #334155 50%, #475569 75%, #64748b 100%);
        padding: 40px 35px;
        border-radius: 0 0 25px 25px;
        color: white;
        margin: -20px -20px 40px -20px;
        box-shadow: 0 20px 60px rgba(15, 23, 42, 0.3), 0 0 0 1px rgba(96, 165, 250, 0.1);
        border-bottom: 4px solid #60a5fa;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(20px);
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(96, 165, 250, 0.15) 50%, transparent 70%);
        animation: shimmer 6s infinite;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 20% 80%, rgba(96, 165, 250, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    /* Métriques ultra-modernes avec glassmorphism professionnel */
    .metric-container {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.9) 100%);
        backdrop-filter: blur(25px);
        border-radius: 20px;
        padding: 28px 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.08), 0 0 0 1px rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.4);
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #60a5fa, #8b5cf6, #06b6d4, #10b981);
        background-size: 200% 100%;
        animation: gradient-shift 3s ease infinite;
    }
    
    .metric-container::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 30% 20%, rgba(96, 165, 250, 0.05) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .metric-container:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 25px 60px rgba(0,0,0,0.12), 0 0 0 1px rgba(255, 255, 255, 0.3);
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(248, 250, 252, 0.95) 100%);
    }
    
    .metric-icon {
        font-size: 2.8em;
        margin-bottom: 20px;
        display: block;
        text-align: center;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }
    
    .metric-value {
        font-size: 2.8em;
        font-weight: 900;
        background: linear-gradient(135deg, #1e293b, #334155);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 15px 0;
        text-align: center;
        text-shadow: none;
    }
    
    .metric-label {
        font-size: 0.95em;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        text-align: center;
        margin-top: 10px;
    }
    
    /* Alertes ultra-modernes avec effets avancés - Taille réduite */
    .alert-critical {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 50%, #b91c1c 100%);
        color: white;
        padding: 25px;
        border-radius: 18px;
        margin: 20px 0;
        box-shadow: 0 12px 32px rgba(239, 68, 68, 0.35);
        border-left: 4px solid #fecaca;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .alert-critical::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.15) 50%, transparent 70%);
        animation: shimmer 2.5s infinite;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 50%, #b45309 100%);
        color: white;
        padding: 35px;
        border-radius: 20px;
        margin: 30px 0;
        box-shadow: 0 15px 40px rgba(245, 158, 11, 0.4);
        border-left: 5px solid #fed7aa;
        backdrop-filter: blur(10px);
    }
    
    /* Sections ultra-modernes avec glassmorphism professionnel */
    .section-header {
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 30%, #2563eb 70%, #1d4ed8 100%);
        padding: 20px 28px;
        border-radius: 18px;
        color: white;
        margin: 25px 0 20px 0;
        box-shadow: 0 15px 40px rgba(96, 165, 250, 0.2), 0 0 0 1px rgba(255, 255, 255, 0.1);
        border-left: 5px solid #93c5fd;
        position: relative;
        backdrop-filter: blur(15px);
        overflow: hidden;
    }
    
    .section-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.12) 50%, transparent 70%);
        animation: shimmer 4s infinite;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 20% 50%, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .section-title {
        font-size: 1.4em;
        font-weight: 800;
        margin: 0;
        display: flex;
        align-items: center;
        text-shadow: 0 2px 4px rgba(0,0,0,0.4);
        letter-spacing: 0.4px;
        position: relative;
        z-index: 2;
    }
    
    .section-subtitle {
        font-size: 1.0em;
        opacity: 0.95;
        margin: 10px 0 0 0;
        font-weight: 500;
        line-height: 1.5;
        position: relative;
        z-index: 2;
    }
    
    /* Tableaux ultra-modernes avec glassmorphism professionnel */
    .stDataFrame {
        border-radius: 22px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.08), 0 0 0 1px rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        overflow: hidden;
        backdrop-filter: blur(15px);
        background: rgba(255, 255, 255, 0.95);
    }
    
    .stDataFrame th {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 30%, #e2e8f0 70%, #cbd5e1 100%) !important;
        font-weight: 800 !important;
        color: #0f172a !important;
        padding: 22px 20px !important;
        border-bottom: 3px solid #60a5fa !important;
        font-size: 0.9em !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
        position: relative;
    }
    
    .stDataFrame th::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #60a5fa, #8b5cf6, #06b6d4);
        opacity: 0.8;
    }
    
    .stDataFrame td {
        padding: 20px !important;
        border-bottom: 1px solid rgba(226, 232, 240, 0.6) !important;
        color: #334155 !important;
        font-weight: 500 !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    .stDataFrame tr {
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    .stDataFrame tr:hover {
        background: linear-gradient(90deg, rgba(248, 250, 252, 0.9) 0%, rgba(241, 245, 249, 0.8) 100%) !important;
        transform: translateX(4px) scale(1.002);
        box-shadow: 0 4px 20px rgba(96, 165, 250, 0.1);
        border-left: 3px solid #60a5fa;
    }
    
    .stDataFrame tr:hover td {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    
    /* Graphiques ultra-modernes avec glassmorphism professionnel */
    .js-plotly-plot {
        border-radius: 24px;
        box-shadow: 0 25px 60px rgba(0,0,0,0.1), 0 0 0 1px rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(248, 250, 252, 0.95) 100%);
        backdrop-filter: blur(20px);
        overflow: hidden;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    .js-plotly-plot::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 20% 80%, rgba(96, 165, 250, 0.03) 0%, transparent 50%);
        pointer-events: none;
        z-index: 1;
    }
    
    .js-plotly-plot:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 30px 70px rgba(0,0,0,0.15), 0 0 0 1px rgba(255, 255, 255, 0.2);
        background: linear-gradient(135deg, rgba(255, 255, 255, 1) 0%, rgba(248, 250, 252, 0.98) 100%);
    }
    
    /* Animations professionnelles */
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 20px rgba(96, 165, 250, 0.3); }
        50% { box-shadow: 0 0 30px rgba(96, 165, 250, 0.6); }
    }
    
    /* Éléments interactifs ultra-modernes et professionnels */
    .stButton > button {
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 30%, #2563eb 70%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 14px 28px;
        font-weight: 700;
        font-size: 0.9em;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 25px rgba(96, 165, 250, 0.25), 0 0 0 1px rgba(255, 255, 255, 0.1);
        text-transform: uppercase;
        letter-spacing: 0.8px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.6s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 30%, #1d4ed8 70%, #1e40af 100%);
        transform: translateY(-4px) scale(1.03);
        box-shadow: 0 15px 35px rgba(96, 165, 250, 0.35), 0 0 0 1px rgba(255, 255, 255, 0.2);
        letter-spacing: 1px;
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(1.01);
        transition: all 0.1s ease;
    }
    
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
    }
    
    .stSelectbox > div > div:hover {
        border-color: #60a5fa;
        box-shadow: 0 0 0 4px rgba(96, 165, 250, 0.1);
        transform: translateY(-1px);
    }
    
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 12px 16px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #60a5fa;
        box-shadow: 0 0 0 4px rgba(96, 165, 250, 0.1);
        transform: translateY(-1px);
    }
    
    /* Messages d'état ultra-modernes et professionnels */
    .stSuccess {
        background: linear-gradient(135deg, #10b981 0%, #059669 30%, #047857 70%, #065f46 100%);
        color: white;
        border-radius: 16px;
        padding: 18px 24px;
        box-shadow: 0 12px 30px rgba(16, 185, 129, 0.25), 0 0 0 1px rgba(110, 231, 183, 0.2);
        border-left: 5px solid #6ee7b7;
        backdrop-filter: blur(15px);
        position: relative;
        overflow: hidden;
    }
    
    .stSuccess::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #6ee7b7, #34d399, #10b981);
    }
    
    .stWarning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 30%, #b45309 70%, #92400e 100%);
        color: white;
        border-radius: 16px;
        padding: 18px 24px;
        box-shadow: 0 12px 30px rgba(245, 158, 11, 0.25), 0 0 0 1px rgba(254, 215, 170, 0.2);
        border-left: 5px solid #fed7aa;
        backdrop-filter: blur(15px);
        position: relative;
        overflow: hidden;
    }
    
    .stWarning::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #fed7aa, #fbbf24, #f59e0b);
    }
    
    .stError {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 30%, #b91c1c 70%, #991b1b 100%);
        color: white;
        border-radius: 16px;
        padding: 18px 24px;
        box-shadow: 0 12px 30px rgba(239, 68, 68, 0.25), 0 0 0 1px rgba(254, 202, 202, 0.2);
        border-left: 5px solid #fecaca;
        backdrop-filter: blur(15px);
        position: relative;
        overflow: hidden;
    }
    
    .stError::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #fecaca, #fca5a5, #ef4444);
    }
    
    .stInfo {
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 30%, #2563eb 70%, #1d4ed8 100%);
        color: white;
        border-radius: 16px;
        padding: 18px 24px;
        box-shadow: 0 12px 30px rgba(96, 165, 250, 0.25), 0 0 0 1px rgba(147, 197, 253, 0.2);
        border-left: 5px solid #93c5fd;
        backdrop-filter: blur(15px);
        position: relative;
        overflow: hidden;
    }
    
    .stInfo::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #93c5fd, #60a5fa, #3b82f6);
    }
    
    /* Responsive design ultra-moderne - Tailles réduites */
    @media (max-width: 768px) {
        .metric-container {
            padding: 20px 18px;
            margin: 8px 0;
        }
        
        .metric-value {
            font-size: 2.0em;
        }
        
        .section-header {
            padding: 15px 20px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Définir les fonctions de récupération des données après la configuration Django
    def get_commande_bureau_data():
        """Récupère les données des commandes bureau avec calcul de fin de garantie"""
        commandes = CommandeBureau.objects.select_related('fournisseur').all()
        
        data = []
        for cmd in commandes:
            fin_garantie = calculate_garantie_end_date(
                cmd.date_reception, 
                cmd.duree_garantie_valeur, 
                cmd.duree_garantie_unite
            )
            
            jours_restants = None
            if fin_garantie:
                jours_restants = (fin_garantie - datetime.now().date()).days
            
            data.append({
                'Type': 'Bureautique',
                'Numéro': cmd.numero_commande,
                'Fournisseur': cmd.fournisseur.nom if cmd.fournisseur else 'N/A',
                'Date Commande': cmd.date_commande,
                'Date Réception': cmd.date_reception,
                'Durée Garantie': f"{cmd.duree_garantie_valeur} {cmd.duree_garantie_unite}",
                'Fin Garantie': fin_garantie,
                'Jours Restants': jours_restants,
                'Statut': 'En Garantie' if fin_garantie and jours_restants and jours_restants > 0 else 'Garantie Expirée'
            })
        
        return pd.DataFrame(data)

    def get_commande_info_data():
        """Récupère les données des commandes informatiques avec calcul de fin de garantie"""
        commandes = Commande.objects.select_related('fournisseur').all()
        
        data = []
        for cmd in commandes:
            fin_garantie = calculate_garantie_end_date(
                cmd.date_reception, 
                cmd.duree_garantie_valeur, 
                cmd.duree_garantie_unite
            )
            
            jours_restants = None
            if fin_garantie:
                jours_restants = (fin_garantie - datetime.now().date()).days
            
            data.append({
                'Type': 'Informatique',
                'Numéro': cmd.numero_commande,
                'Fournisseur': cmd.fournisseur.nom if cmd.fournisseur else 'N/A',
                'Date Commande': cmd.date_commande,
                'Date Réception': cmd.date_reception,
                'Durée Garantie': f"{cmd.duree_garantie_valeur} {cmd.duree_garantie_unite}",
                'Fin Garantie': fin_garantie,
                'Jours Restants': jours_restants,
                'Statut': 'En Garantie' if fin_garantie and jours_restants and jours_restants > 0 else 'Garantie Expirée'
            })
        
        return pd.DataFrame(data)
    
    def get_user_role(username):
        """Détermine le rôle de l'utilisateur basé sur ses groupes"""
        try:
            # Utiliser le modèle utilisateur personnalisé
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            user = User.objects.get(username=username)
            groups = user.groups.all()
            
            if any(group.name == 'Super Admin' for group in groups):
                return 'super_admin'
            elif any(group.name == 'Gestionnaire Informatique' for group in groups):
                return 'gestionnaire_info'
            elif any(group.name == 'Gestionnaire Bureau' for group in groups):
                return 'gestionnaire_bureau'
            else:
                return 'employe'
        except Exception:
            return None
    
    def detect_current_user():
        """Détecte automatiquement l'utilisateur connecté via plusieurs méthodes"""
        try:
            # Méthode 1: Paramètres de requête Streamlit (priorité haute)
            params = st.query_params

            username = params.get('username', None)
            
            if username:
                # Décoder et nettoyer le nom d'utilisateur
                import urllib.parse
                try:
                    username = urllib.parse.unquote(username)
                except:
                    pass
                username = username.strip()

                
                from django.contrib.auth import get_user_model
                User = get_user_model()
                try:
                    user = User.objects.get(username=username)

                    return user
                except User.DoesNotExist:

                    # Essayer de trouver l'utilisateur par nom partiel
                    try:
                        users = User.objects.filter(username__icontains=username)
                        if users.count() == 1:
                            user = users.first()

                            return user
                        elif users.count() > 1:
                            pass
                        else:
                            pass

                    except Exception as e:
                        pass
                        
                    # Essayer de trouver par email ou nom complet
                    try:
                        # Chercher par email
                        users_by_email = User.objects.filter(email__icontains=username)
                        if users_by_email.count() == 1:
                            user = users_by_email.first()
                            return user
                        
                        # Chercher par nom complet
                        users_by_name = User.objects.filter(first_name__icontains=username) | User.objects.filter(last_name__icontains=username)
                        if users_by_email.count() == 1:
                            user = users_by_name.first()
                            return user
                            
                    except Exception as e:
                        pass
                except Exception as e:
                    pass

            else:
                pass
            
            # Méthode 2: Session Streamlit existante (priorité moyenne)
            if 'username' in st.session_state and st.session_state.get('authenticated', False):
                from django.contrib.auth import get_user_model
                User = get_user_model()
                try:
                    user = User.objects.get(username=st.session_state['username'])
                    return user
                except User.DoesNotExist:
                    pass
                except Exception as e:
                    pass
            
            # Méthode 3: Variable d'environnement (priorité basse)
            env_username = os.environ.get('DJANGO_USER', None)
            if env_username:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                try:
                    user = User.objects.get(username=env_username)
                    return user
                except User.DoesNotExist:
                    pass
                except Exception as e:
                    pass
            
            # Méthode 4: Détection automatique des utilisateurs autorisés
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            # Chercher d'abord un Super Admin
            super_admin = User.objects.filter(groups__name='Super Admin').first()
            if super_admin:
                st.success(f"Super Admin trouvé automatiquement: {super_admin.username}")
                return super_admin
            
            # Chercher un Gestionnaire Informatique
            gestionnaire_info = User.objects.filter(groups__name='Gestionnaire Informatique').first()
            if gestionnaire_info:
                st.success(f"Gestionnaire Informatique trouvé automatiquement: {gestionnaire_info.username}")
                return gestionnaire_info
            else:

                # Lister tous les utilisateurs et leurs groupes pour debug
                all_users = User.objects.all()

                for user in all_users:
                    groups = [g.name for g in user.groups.all()]
                    st.info(f"  - {user.username}: {groups}")
            
            # Chercher un Gestionnaire Bureau
            gestionnaire_bureau = User.objects.filter(groups__name='Gestionnaire Bureau').first()
            if gestionnaire_bureau:
                st.success(f"Gestionnaire Bureau trouvé automatiquement: {gestionnaire_bureau.username}")
                return gestionnaire_bureau
            else:

                # Essayer de trouver par nom d'utilisateur contenant "bureau"
                bureau_users = User.objects.filter(username__icontains='bureau')
                if bureau_users.exists():

                    for user in bureau_users:
                        groups = [g.name for g in user.groups.all()]
                        st.info(f"  - {user.username}: Groupes={groups}")
                        # Si l'utilisateur a un nom contenant "bureau", l'utiliser
                        if 'bureau' in user.username.lower():
                            st.success(f"Utilisateur 'bureau' sélectionné automatiquement: {user.username}")
                            return user
            
            # Méthode 5: Sélection automatique de l'utilisateur le plus approprié

            
            # Lister tous les utilisateurs disponibles
            from django.contrib.auth import get_user_model
            User = get_user_model()
            users = User.objects.all()
            
            if users.count() > 1:
                st.info(f"{users.count()} utilisateurs trouvés dans la base de données")
                
                # Filtrer les utilisateurs autorisés (Super Admin, Gestionnaire Info, Gestionnaire Bureau)
                authorized_users = []
                for user in users:
                    role = get_user_role(user.username)
                    if role in ['super_admin', 'gestionnaire_info', 'gestionnaire_bureau']:
                        authorized_users.append(user)
                
                if authorized_users:
                    st.success(f"{len(authorized_users)} utilisateur(s) autorisé(s) trouvé(s)")
                    
                    # Sélectionner automatiquement le premier utilisateur autorisé
                    auto_selected_user = authorized_users[0]
                    st.success(f"Utilisateur sélectionné automatiquement: {auto_selected_user.username} ({get_user_role(auto_selected_user.username)})")
                    
                    # Afficher tous les utilisateurs autorisés disponibles
                    st.info("Utilisateurs autorisés disponibles:")
                    for i, user in enumerate(authorized_users):
                        role = get_user_role(user.username)
                        st.info(f"  {i+1}. {user.username} ({role})")
                    
                    # Option de changement manuel si plusieurs utilisateurs autorisés
                    if len(authorized_users) > 1:
                        st.info("Vous pouvez changer d'utilisateur si nécessaire:")
                        user_options = {f"{user.username} ({get_user_role(user.username)})": user for user in authorized_users}
                        selected_user_key = st.selectbox(
                            "👤 Changer d'utilisateur:",
                            options=list(user_options.keys()),
                            index=0
                        )
                        
                        if selected_user_key:
                            selected_user = user_options[selected_user_key]
                            st.success(f"Utilisateur changé pour: {selected_user.username}")
                            return selected_user
                    
                    return auto_selected_user
                else:
                    st.error("Aucun utilisateur autorisé trouvé dans la base de données")
                    st.info("Seuls les Super Admin, Gestionnaire Informatique et Gestionnaire Bureau peuvent accéder au dashboard")
                    
                    # Afficher tous les utilisateurs pour debug

                    for user in users:
                        groups = [g.name for g in user.groups.all()]
                        role = get_user_role(user.username)
                        st.info(f"  - {user.username}: Groupes={groups}, Rôle={role}")
                        
                    # Forcer la sélection du premier utilisateur autorisé trouvé
                    for user in users:
                        role = get_user_role(user.username)
                        if role in ['super_admin', 'gestionnaire_info', 'gestionnaire_bureau']:
                            st.success(f"Utilisateur autorisé trouvé et sélectionné: {user.username}")
                            return user
                    
                    st.error("Aucun utilisateur avec les permissions nécessaires")
                    return None
            elif users.count() == 1:
                user = users.first()
                role = get_user_role(user.username)
                if role in ['super_admin', 'gestionnaire_info', 'gestionnaire_bureau']:
                    st.info(f"Utilisateur unique autorisé trouvé: {user.username}")
                    return user
                else:
                    st.error(f"L'utilisateur unique '{user.username}' n'a pas les permissions nécessaires")
                    return None
            else:
                st.error("Aucun utilisateur dans la base de données")
                return None
                
        except Exception as e:
            st.error(f"Erreur générale lors de la détection: {e}")
        
        return None
    
    def redirect_based_on_role(user_role):
        """Redirige l'utilisateur vers la section appropriée selon son rôle"""
        if user_role == 'super_admin':
            pass
            return 'all'
        elif user_role == 'gestionnaire_info':
            return 'info'
        elif user_role == 'gestionnaire_bureau':
            return 'bureau'
        else:
            # Employés et autres rôles non autorisés
            return 'unauthorized'
    

    

    
    # Nettoyer la session si elle contient un utilisateur non autorisé
    if 'username' in st.session_state and st.session_state.get('authenticated', False):
        current_role = get_user_role(st.session_state['username'])
        if current_role not in ['super_admin', 'gestionnaire_info', 'gestionnaire_bureau']:
            st.warning(f"Session existante avec utilisateur non autorisé: {st.session_state['username']}")
            st.info("Nettoyage de la session...")
            st.session_state.clear()
            st.rerun()
    
    # Détection automatique de l'utilisateur connecté
    current_user = detect_current_user()
    
    if current_user:
        # Utilisateur détecté automatiquement
        st.session_state['authenticated'] = True
        st.session_state['username'] = current_user.username
        st.session_state['user_role'] = get_user_role(current_user.username)
        st.session_state['user'] = current_user
        
        with st.sidebar:
            st.success(f"Connecté automatiquement")
            
            if st.button("Se déconnecter"):
                st.session_state['authenticated'] = False
                st.rerun()
    else:
        # Fallback : authentification manuelle (seulement si aucune détection automatique)
        with st.sidebar:
            st.header("Authentification Manuelle")
            st.info("Le système n'a pas pu détecter automatiquement votre utilisateur")
            
            # Bouton pour forcer la détection automatique
            if st.button("Forcer la détection automatique"):
                st.session_state.clear()
                st.rerun()
            
            st.markdown("---")
            
            username = st.text_input("Nom d'utilisateur", value="test_superadmin")
            password = st.text_input("Mot de passe", type="password", value="testpass123")
            
            if st.button("Se connecter"):
                user = authenticate(username=username, password=password)
                if user:
                    st.success(f"Connecté en tant que {username}")
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    st.session_state['user_role'] = get_user_role(username)
                    st.session_state['user'] = user
                    st.rerun()
                else:
                    st.error("Identifiants incorrects")
                    st.session_state['authenticated'] = False
            
            if 'authenticated' in st.session_state and st.session_state['authenticated']:
                st.success(f"Rôle: {st.session_state['user_role']}")
                
                # Bouton de déconnexion
                if st.button("Se déconnecter"):
                    st.session_state['authenticated'] = False
                    st.rerun()
    
    # Vérification de l'authentification
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.warning("Aucun utilisateur détecté automatiquement")
        st.info("Pour une détection automatique, accédez au dashboard depuis votre dashboard utilisateur Django")
        st.info("Ou utilisez l'authentification manuelle dans la barre latérale")
        return
    
    user_role = st.session_state['user_role']
    
    # Redirection intelligente selon le rôle
    dashboard_type = redirect_based_on_role(user_role)
    
    # Récupération et affichage des données selon le type de dashboard
    if dashboard_type == 'all':
        
        df_bureau = get_commande_bureau_data()
        df_info = get_commande_info_data()
        df_all = pd.concat([df_bureau, df_info], ignore_index=True)
        
        # Calculs intelligents pour les métriques
        total_commandes = len(df_all)
        en_garantie = len(df_all[df_all['Statut'] == 'En Garantie'])
        expirees = len(df_all[df_all['Statut'] == 'Garantie Expirée'])
        
        # En-tête personnalisé pour Super Admin
        st.markdown("""
        <div class="main-header" style="background: linear-gradient(135deg, #1e40af 0%, #3b82f6 25%, #60a5fa 50%, #93c5fd 75%, #dbeafe 100%); border-bottom: 3px solid #fbbf24; padding: 15px 20px; margin-bottom: 20px;">
            <div>
                <h1 style="margin: 0; font-size: 1.8em; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                     Dashboard Garanties - Super Admin
                </h1>
                <p style="margin: 5px 0 0 0; font-size: 1em; opacity: 0.9; font-weight: 400; letter-spacing: 0.3px;">
                    Vue globale de toutes les garanties (Informatique et Bureautique)
                </p>
                <div style="margin-top: 10px; display: flex; gap: 15px; opacity: 0.85;">
                    <span style="background: rgba(255,255,255,0.15); padding: 5px 12px; border-radius: 15px; font-size: 0.8em; font-weight: 500; border: 1px solid rgba(255,255,255,0.2);">
                        Accès complet à toutes les données
                    </span>
                    <span style="background: rgba(255,255,255,0.15); padding: 5px 12px; border-radius: 15px; font-size: 0.8em; font-weight: 500; border: 1px solid rgba(255,255,255,0.2);">
                        Surveillance globale des garanties
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Tableau de bord principal pour le suivi des garanties
        create_garantie_timeline_dashboard(df_all, "Dashboard Garanties - Vue Globale", "all")
        
        # Tableau interactif avec tri et filtres
        st.subheader("Données Détaillées - Tableau Interactif")
        
        # Filtres avancés
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            statut_filter = st.selectbox(
                "Filtrer par Statut",
                ["Tous", "En Garantie", "Garantie Expirée", "Urgente (≤15j)", "Attention (≤30j)", "Normale (≤90j)"]
            )
        with col2:
            type_filter = st.selectbox(
                "Filtrer par Type",
                ["Tous", "Bureautique", "Informatique"]
            )
        with col3:
            fournisseur_filter = st.selectbox(
                "Filtrer par Fournisseur",
                ["Tous"] + list(df_all['Fournisseur'].unique())
            )
        with col4:
            tri_colonne = st.selectbox(
                "Trier par",
                ["Jours Restants", "Date Réception", "Fin Garantie", "Numéro", "Fournisseur"]
            )
        
        # Appliquer les filtres et le tri
        df_filtered = df_all.copy()
        
        # Filtres
        if statut_filter != "Tous":
            if statut_filter == "Urgente (≤15j)":
                df_filtered = df_filtered[(df_filtered['Jours Restants'] > 0) & (df_filtered['Jours Restants'] <= 15)]
            elif statut_filter == "Attention (≤30j)":
                df_filtered = df_filtered[(df_filtered['Jours Restants'] > 15) & (df_filtered['Jours Restants'] <= 30)]
            elif statut_filter == "Normale (≤90j)":
                df_filtered = df_filtered[(df_filtered['Jours Restants'] > 30) & (df_filtered['Jours Restants'] <= 90)]
            else:
                df_filtered = df_filtered[df_filtered['Statut'] == statut_filter]
        
        if type_filter != "Tous":
            df_filtered = df_filtered[df_filtered['Type'] == type_filter]
        
        if fournisseur_filter != "Tous":
            df_filtered = df_filtered[df_filtered['Fournisseur'] == fournisseur_filter]
        
        # Tri
        if tri_colonne == "Jours Restants":
            df_filtered = df_filtered.sort_values('Jours Restants', ascending=True)
        elif tri_colonne == "Date Réception":
            df_filtered = df_filtered.sort_values('Date Réception', ascending=False)
        elif tri_colonne == "Fin Garantie":
            df_filtered = df_filtered.sort_values('Fin Garantie', ascending=True)
        elif tri_colonne == "Numéro":
            df_filtered = df_filtered.sort_values('Numéro')
        elif tri_colonne == "Fournisseur":
            df_filtered = df_filtered.sort_values('Fournisseur')
        
        # Afficher le nombre de résultats
        st.info(f"{len(df_filtered)} commande(s) trouvée(s) avec les filtres appliqués")
        
        display_colored_dataframe(df_filtered, "Détail des Commandes (Filtré et Trié)")
        
    elif dashboard_type == 'info':
        # Gestionnaire Informatique - Vue informatique uniquement
        df_info = get_commande_info_data()
        
        # En-tête personnalisé pour Gestionnaire Informatique
        st.markdown("""
        <div class="main-header" style="background: linear-gradient(135deg, #059669 0%, #10b981 25%, #34d399 50%, #6ee7b7 75%, #a7f3d0 100%); border-bottom: 3px solid #f59e0b; padding: 15px 20px; margin-bottom: 20px;">
            <div>
                <h1 style="margin: 0; font-size: 1.8em; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                    Dashboard Garanties - Gestionnaire Informatique
                </h1>
                <p style="margin: 5px 0 0 0; font-size: 1em; opacity: 0.9; font-weight: 400; letter-spacing: 0.3px;">
                    Gestion des garanties des équipements informatiques uniquement
                </p>
                <div style="margin-top: 10px; display: flex; gap: 15px; opacity: 0.85;">
                    <span style="background: rgba(255,255,255,0.15); padding: 5px 12px; border-radius: 15px; font-size: 0.8em; font-weight: 500; border: 1px solid rgba(255,255,255,0.2);">
                        Équipements informatiques
                    </span>
                    <span style="background: rgba(255,255,255,0.15); padding: 5px 12px; border-radius: 15px; font-size: 0.8em; font-weight: 500; border: 1px solid rgba(255,255,255,0.2);">
                        Surveillance spécialisée
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Tableau de bord principal pour le suivi des garanties
        create_garantie_timeline_dashboard(df_info, "Dashboard Garanties - Équipements Informatiques", "info")
        
        # Tableau interactif avec tri et filtres
        st.subheader("Données Détaillées - Tableau Interactif")
        
        # Filtres avancés
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            statut_filter = st.selectbox(
                "Filtrer par Statut",
                ["Tous", "En Garantie", "Garantie Expirée", "Urgente (≤15j)", "Attention (≤30j)", "Normale (≤90j)"]
            )
        with col2:
            type_filter = st.selectbox(
                "Filtrer par Type",
                ["Tous", "Informatique"]
            )
        with col3:
            fournisseur_filter = st.selectbox(
                "Filtrer par Fournisseur",
                ["Tous"] + list(df_info['Fournisseur'].unique())
            )
        with col4:
            tri_colonne = st.selectbox(
                "Trier par",
                ["Jours Restants", "Date Réception", "Fin Garantie", "Numéro", "Fournisseur"]
            )
        
        # Appliquer les filtres et le tri
        df_filtered = df_info.copy()
        
        # Filtres
        if statut_filter != "Tous":
            if statut_filter == "Urgente (≤15j)":
                df_filtered = df_filtered[(df_filtered['Jours Restants'] > 0) & (df_filtered['Jours Restants'] <= 15)]
            elif statut_filter == "Attention (≤30j)":
                df_filtered = df_filtered[(df_filtered['Jours Restants'] > 15) & (df_filtered['Jours Restants'] <= 30)]
            elif statut_filter == "Normale (≤90j)":
                df_filtered = df_filtered[(df_filtered['Jours Restants'] > 30) & (df_filtered['Jours Restants'] <= 90)]
            else:
                df_filtered = df_filtered[df_filtered['Statut'] == statut_filter]
        
        if type_filter != "Tous":
            df_filtered = df_filtered[df_filtered['Type'] == type_filter]
        
        if fournisseur_filter != "Tous":
            df_filtered = df_filtered[df_filtered['Fournisseur'] == fournisseur_filter]
        
        # Tri
        if tri_colonne == "Jours Restants":
            df_filtered = df_filtered.sort_values('Jours Restants', ascending=True)
        elif tri_colonne == "Date Réception":
            df_filtered = df_filtered.sort_values('Date Réception', ascending=False)
        elif tri_colonne == "Fin Garantie":
            df_filtered = df_filtered.sort_values('Fin Garantie', ascending=True)
        elif tri_colonne == "Numéro":
            df_filtered = df_filtered.sort_values('Numéro')
        elif tri_colonne == "Fournisseur":
            df_filtered = df_filtered.sort_values('Fournisseur')
        
        # Afficher le nombre de résultats
        st.info(f"{len(df_filtered)} commande(s) trouvée(s) avec les filtres appliqués")
        
        display_colored_dataframe(df_filtered, "Détail des Commandes (Filtré et Trié)")
        
    elif dashboard_type == 'bureau':
        # Gestionnaire Bureau - Vue bureautique uniquement
        df_bureau = get_commande_bureau_data()
        
        # En-tête personnalisé pour Gestionnaire Bureau
        st.markdown("""
        <div class="main-header" style="background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 25%, #a78bfa 50%, #c4b5fd 75%, #ddd6fe 100%); border-bottom: 3px solid #f59e0b; padding: 15px 20px; margin-bottom: 20px;">
            <div>
                <h1 style="margin: 0; font-size: 1.8em; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                    Dashboard Garanties - Gestionnaire Bureau
                </h1>
                <p style="margin: 5px 0 0 0; font-size: 1em; opacity: 0.9; font-weight: 400; letter-spacing: 0.3px;">
                    Gestion des garanties des équipements bureautiques uniquement
                </p>
                <div style="margin-top: 10px; display: flex; gap: 15px; opacity: 0.85;">
                    <span style="background: rgba(255,255,255,0.15); padding: 5px 12px; border-radius: 15px; font-size: 0.8em; font-weight: 500; border: 1px solid rgba(255,255,255,0.2);">
                        Équipements bureautiques
                    </span>
                    <span style="background: rgba(255,255,255,0.15); padding: 5px 12px; border-radius: 15px; font-size: 0.8em; font-weight: 500; border: 1px solid rgba(255,255,255,0.2);">
                        Gestion spécialisée
                    </span>
            </div>
            </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Tableau de bord principal pour le suivi des garanties
        create_garantie_timeline_dashboard(df_bureau, "Dashboard Garanties - Équipements Bureautiques", "bureau")
        
        # Tableau interactif avec tri et filtres
        st.subheader("Données Détaillées - Tableau Interactif")
        
        # Filtres avancés
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            statut_filter = st.selectbox(
                "Filtrer par Statut",
                ["Tous", "En Garantie", "Garantie Expirée", "Urgente (≤15j)", "Attention (≤30j)", "Normale (≤90j)"]
            )
        with col2:
            type_filter = st.selectbox(
                "Filtrer par Type",
                ["Tous", "Bureautique"]
            )
        with col3:
            fournisseur_filter = st.selectbox(
                "Filtrer par Fournisseur",
                ["Tous"] + list(df_bureau['Fournisseur'].unique())
            )
        with col4:
            tri_colonne = st.selectbox(
                "Trier par",
                ["Jours Restants", "Date Réception", "Fin Garantie", "Numéro", "Fournisseur"]
            )
        
        # Appliquer les filtres et le tri
        df_filtered = df_bureau.copy()
        
        # Filtres
        if statut_filter != "Tous":
            if statut_filter == "Urgente (≤15j)":
                df_filtered = df_filtered[(df_filtered['Jours Restants'] > 0) & (df_filtered['Jours Restants'] <= 15)]
            elif statut_filter == "Attention (≤30j)":
                df_filtered = df_filtered[(df_filtered['Jours Restants'] > 15) & (df_filtered['Jours Restants'] <= 30)]
            elif statut_filter == "Normale (≤90j)":
                df_filtered = df_filtered[(df_filtered['Jours Restants'] > 30) & (df_filtered['Jours Restants'] <= 90)]
            else:
                df_filtered = df_filtered[df_filtered['Statut'] == statut_filter]
        
        if type_filter != "Tous":
            df_filtered = df_filtered[df_filtered['Type'] == type_filter]
        
        if fournisseur_filter != "Tous":
            df_filtered = df_filtered[df_filtered['Fournisseur'] == fournisseur_filter]
        
        # Tri
        if tri_colonne == "Jours Restants":
            df_filtered = df_filtered.sort_values('Jours Restants', ascending=True)
        elif tri_colonne == "Date Réception":
            df_filtered = df_filtered.sort_values('Date Réception', ascending=False)
        elif tri_colonne == "Fin Garantie":
            df_filtered = df_filtered.sort_values('Fin Garantie', ascending=True)
        elif tri_colonne == "Numéro":
            df_filtered = df_filtered.sort_values('Numéro')
        elif tri_colonne == "Fournisseur":
            df_filtered = df_filtered.sort_values('Fournisseur')
        
        # Afficher le nombre de résultats
        st.info(f"{len(df_filtered)} commande(s) trouvée(s) avec les filtres appliqués")
        
        display_colored_dataframe(df_filtered, "Détail des Commandes (Filtré et Trié)")
        
    elif dashboard_type == 'unauthorized':
        # Employés et autres rôles non autorisés
        st.markdown("""
        <div class="alert-critical">
            <div style="display: flex; align-items: center; justify-content: center;">
                <div style="text-align: center;">
                    <h2 style="margin: 0; font-size: 2.2em; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                        ACCÈS REFUSÉ
                    </h2>
                    <p style="margin: 15px 0 0 0; font-size: 1.2em; opacity: 0.95;">
                        Vous n'avez pas les permissions nécessaires pour accéder au Dashboard de Garanties.<br>
                        <strong>Rôles autorisés :</strong> Super Admin, Gestionnaire Informatique, Gestionnaire Bureau<br>
                        Veuillez contacter votre administrateur pour obtenir les droits d'accès appropriés.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        

        
    else:  # cas d'erreur
        st.markdown("""
        <div class="alert-critical">
                <div style="display: flex; align-items: center; justify-content: center;">
                    <div style="text-align: center;">
                    <h2 style="margin: 0; font-size: 2.2em; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                        ACCÈS NON AUTORISÉ
                        </h2>
                    <p style="margin: 15px 0 0 0; font-size: 1.2em; opacity: 0.95;">
                        Vous n'avez pas les permissions nécessaires pour accéder au Dashboard de Garanties.<br>
                        Veuillez contacter votre administrateur pour obtenir les droits d'accès appropriés.
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            


if __name__ == "__main__":
    main()
