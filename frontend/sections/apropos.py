import streamlit as st

def lancer_a_propos():
    st.title("ℹ️ À propos de l'application")
    st.markdown("---")

    st.subheader("🚗 Contexte du projet")
    st.write("""
    Cette application a été développée dans le cadre du **Kaggle Playground Series - Season 5, Episode 10 (Octobre 2025)**.  
    Le défi visait à **prédire le risque d’accident routier** à partir de caractéristiques de la route, de la météo, 
    de l’éclairage et d’autres facteurs liés à la sécurité routière.

    Ce projet s’inscrit dans la continuité des séries Kaggle Playground, 
    qui permettent de pratiquer le **machine learning sur des cas concrets** et accessibles.  
    Il s’agissait également de la seconde partie d’un challenge en deux temps, 
    en collaboration avec **Stack Overflow**, invitant les participants à développer une **application web interactive**.
    """)

    st.markdown("---")

    st.subheader("🎯 Objectif du projet")
    st.write("""
    L’objectif principal de cette application est de **modéliser et visualiser le risque d’accident routier** 
    à travers une interface interactive, permettant :
    - L’**exploration visuelle** des variables et de leurs relations avec le risque d’accident,  
    - La **prédiction personnalisée** du risque selon des paramètres choisis,  
    - Et un **mini-jeu interactif** pour tester son intuition face au modèle.

    L’ensemble vise à rendre le **machine learning plus pédagogique et ludique**.
    """)

    st.markdown("---")

    st.subheader("🧰 Outils et technologies utilisés")
    st.markdown("Voici la stack technique utilisée pour le projet :")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image("https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg", width=60)
        st.caption("Python")
    with col2:
        st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=80)
        st.caption("Streamlit")
    with col3:
        st.image("https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg", width=60)
        st.caption("Pandas")
    with col4:
        st.image("https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg", width=60)
        st.caption("NumPy")
    with col5:
        st.image("https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg", width=60)
        st.caption("Scikit-learn")

    col6, col7, col8, col9, col10 = st.columns(5)
    with col6:
        st.image("https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg", width=60)
        st.caption("GitHub")
    with col7:
        st.image("https://upload.wikimedia.org/wikipedia/commons/3/3c/Flask_logo.svg", width=130)
        st.caption("Flask")
    with col8:
        st.image("https://raw.githubusercontent.com/lucaswsss/risk_accident_prediction/main/frontend/assets/render.svg", width=150)
        st.caption("Render")
    with col9:
        st.image("https://seaborn.pydata.org/_images/logo-mark-lightbg.svg", width=60)
        st.caption("Seaborn")
    with col10:
        st.image("https://upload.wikimedia.org/wikipedia/commons/8/84/Matplotlib_icon.svg", width=60)
        st.caption("Matplotlib")
    st.markdown("---")

    st.subheader("☁️ Déploiement et architecture")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        #### 🧠 Backend — Modèle et API
        - Développée avec **Flask** et **DuckDB**  
        - Hébergée sur **Render**
        - Conçue pour être légère, rapide et facilement intégrable
        - Le modèle est chargé via **Joblib** et retourne la probabilité d’accident  

        """)
    with col2:
        st.markdown("""
        #### 💻 Frontend — Interface Streamlit
        - Interface intuitive et réactive  
        - Communication avec l’API via la bibliothèque **Requests**  
        - Pages dédiées : *Accueil*, *Exploration*, *Prédiction* et *Jeu interactif*  
        - Visualisations dynamiques 
        """)

    st.markdown("L’application Streamlit interagit en temps réel avec l’API FastAPI hébergée sur Render pour afficher les prédictions.")

    st.markdown("---")

    st.subheader("👨‍💻 Auteur du projet")

    col1, col2 = st.columns([0.2, 0.8])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/174/174857.png", width=60)  # Logo LinkedIn
    with col2:
        st.markdown("""
        **Lucas Labbé**  
        📅 Création : *Octobre 2025*  
        🔗 [Mon profil LinkedIn](https://www.linkedin.com/in/lucas-labb%C3%A9-0b8370174/)  
        """)

    st.markdown("""
    ---
    ✨ *Merci d’avoir exploré cette application !*  
    Découvrez les différentes fonctionnalités depuis le menu latéral :  
    **Exploration**, **Prédiction**, et **Jeu interactif**.
    """)


    st.caption("© Lucas Labbé — Application développée avec Streamlit | Octobre 2025")
