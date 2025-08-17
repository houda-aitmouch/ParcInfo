
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Garantie - Mode Simple",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.title("🛡️ Dashboard de Garantie - Mode Simple")
st.markdown("---")

# Message d'information
st.info("""
⚠️ **Mode Simple Activé**

Ce dashboard fonctionne en mode simplifié car les dépendances Django ne sont pas disponibles.
Pour accéder au dashboard complet avec les données réelles, veuillez installer les dépendances manquantes.
""")

# Données de démonstration
@st.cache_data
def generate_demo_data():
    """Génère des données de démonstration"""
    random.seed(42)
    
    # Dates de base
    base_date = datetime.now()
    
    # Générer des données de garantie
    data = []
    for i in range(50):
        date_reception = base_date - timedelta(days=random.randint(0, 365))
        duree_garantie = random.randint(12, 36)
        fin_garantie = date_reception + timedelta(days=duree_garantie * 30)
        jours_restants = (fin_garantie - datetime.now()).days
        
        data.append({
            'Type': random.choice(['Informatique', 'Bureautique']),
            'Numéro': f"CMD-{2024}-{i:03d}",
            'Fournisseur': random.choice(['HP', 'Dell', 'Lenovo', 'Apple', 'Samsung']),
            'Date Commande': date_reception - timedelta(days=7),
            'Date Réception': date_reception,
            'Durée Garantie': f"{duree_garantie} mois",
            'Fin Garantie': fin_garantie,
            'Jours Restants': jours_restants,
            'Statut': 'En Garantie' if jours_restants > 0 else 'Garantie Expirée'
        })
    
    return pd.DataFrame(data)

# Générer les données
df = generate_demo_data()

# Métriques principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Équipements",
        value=len(df),
        delta=f"{len(df[df['Statut'] == 'En Garantie'])} en garantie"
    )

with col2:
    en_garantie = len(df[df['Statut'] == 'En Garantie'])
    st.metric(
        label="En Garantie",
        value=en_garantie,
        delta=f"{en_garantie/len(df)*100:.1f}%"
    )

with col3:
    expires_30j = len(df[(df['Jours Restants'] <= 30) & (df['Jours Restants'] > 0)])
    st.metric(
        label="Expire dans 30j",
        value=expires_30j,
        delta="⚠️ Attention" if expires_30j > 0 else "✅ OK"
    )

with col4:
    expires = len(df[df['Statut'] == 'Garantie Expirée'])
    st.metric(
        label="Garantie Expirée",
        value=expires,
        delta=f"{expires/len(df)*100:.1f}%"
    )

# Graphiques
st.markdown("---")
st.subheader("📊 Visualisations")

col1, col2 = st.columns(2)

with col1:
    # Répartition par type
    fig_type = px.pie(
        df, 
        names='Type', 
        title='Répartition par Type d'Équipement',
        color_discrete_sequence=['#1f77b4', '#ff7f0e']
    )
    st.plotly_chart(fig_type, use_container_width=True)

with col2:
    # Répartition par fournisseur
    fig_fournisseur = px.bar(
        df['Fournisseur'].value_counts().reset_index(),
        x='index',
        y='Fournisseur',
        title='Répartition par Fournisseur',
        labels={'index': 'Fournisseur', 'Fournisseur': 'Nombre'}
    )
    st.plotly_chart(fig_fournisseur, use_container_width=True)

# Tableau des données
st.markdown("---")
st.subheader("📋 Liste des Équipements")

# Filtres
col1, col2, col3 = st.columns(3)

with col1:
    type_filter = st.selectbox(
        "Type d'équipement",
        ['Tous'] + list(df['Type'].unique())
    )

with col2:
    statut_filter = st.selectbox(
        "Statut",
        ['Tous'] + list(df['Statut'].unique())
    )

with col3:
    fournisseur_filter = st.selectbox(
        "Fournisseur",
        ['Tous'] + list(df['Fournisseur'].unique())
    )

# Appliquer les filtres
filtered_df = df.copy()

if type_filter != 'Tous':
    filtered_df = filtered_df[filtered_df['Type'] == type_filter]

if statut_filter != 'Tous':
    filtered_df = filtered_df[filtered_df['Statut'] == statut_filter]

if fournisseur_filter != 'Tous':
    filtered_df = filtered_df[filtered_df['Fournisseur'] == fournisseur_filter]

# Afficher le tableau
st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# Informations de contact
st.markdown("---")
st.markdown("""
### 📞 Support Technique

Si vous avez besoin d'aide pour configurer le dashboard complet avec Django :

1. **Installer les dépendances** : `pip install pgvector django`
2. **Configurer la base de données** : Vérifiez les paramètres Django
3. **Relancer le dashboard** : Utilisez le script de lancement complet

---
*Dashboard de Garantie ParcInfo - Mode Simple*
""")
