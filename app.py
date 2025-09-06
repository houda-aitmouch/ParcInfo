import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="ParcInfo Dashboard",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 ParcInfo - Dashboard de Gestion")
st.markdown("---")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choisir une page",
    ["Accueil", "Matériel Informatique", "Matériel Bureautique", "Commandes", "Statistiques"]
)

if page == "Accueil":
    st.header("Bienvenue dans ParcInfo")
    st.markdown("""
    ### Gestion de Parc Informatique et Bureautique
    
    Ce dashboard vous permet de :
    - Gérer le matériel informatique
    - Suivre les commandes
    - Visualiser les statistiques
    - Administrer les utilisateurs
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Ordinateurs", "150", "5")
    
    with col2:
        st.metric("Imprimantes", "25", "2")
    
    with col3:
        st.metric("Commandes", "12", "3")

elif page == "Matériel Informatique":
    st.header("Matériel Informatique")
    
    # Données d'exemple
    data = {
        'Type': ['Ordinateur', 'Laptop', 'Serveur', 'Tablette'],
        'Quantité': [50, 30, 5, 15],
        'Disponible': [45, 25, 3, 12]
    }
    
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
    
    # Graphique
    fig = px.bar(df, x='Type', y='Quantité', title="Répartition du matériel informatique")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Matériel Bureautique":
    st.header("Matériel Bureautique")
    
    data = {
        'Type': ['Imprimante', 'Scanner', 'Photocopieuse', 'Fax'],
        'Quantité': [20, 10, 5, 2],
        'Disponible': [18, 8, 4, 1]
    }
    
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

elif page == "Commandes":
    st.header("Suivi des Commandes")
    
    data = {
        'Commande': ['CMD-001', 'CMD-002', 'CMD-003', 'CMD-004'],
        'Date': ['2025-09-01', '2025-09-02', '2025-09-03', '2025-09-04'],
        'Statut': ['En cours', 'Livrée', 'En attente', 'En cours'],
        'Montant': [1500, 2300, 800, 1200]
    }
    
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

elif page == "Statistiques":
    st.header("Statistiques")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Répartition par type")
        data = {'Type': ['Informatique', 'Bureautique'], 'Pourcentage': [70, 30]}
        fig = px.pie(data, values='Pourcentage', names='Type', title="Répartition du matériel")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Évolution des commandes")
        data = {
            'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun'],
            'Commandes': [10, 15, 12, 18, 20, 16]
        }
        df = pd.DataFrame(data)
        fig = px.line(df, x='Mois', y='Commandes', title="Évolution mensuelle")
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**ParcInfo Dashboard** - Gestion de Parc Informatique et Bureautique")
