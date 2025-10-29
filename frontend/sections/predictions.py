import streamlit as st
import pandas as pd
import joblib
import numpy as np

def lancer_prediction():
    st.title("Prédiction du risque d'accident 🚦")
    st.subheader("Entrez les paramètres de la route pour obtenir une prédiction")

    # --- Charger le modèle ---
    model = joblib.load("models/meilleure_modele.pkl")

    # --- Inputs utilisateur ---
    road_type = st.selectbox("Type de route", ["highway", "rural", "urban"])
    num_lanes = st.selectbox("Nombre de voies", [1, 2, 3, 4, 5, 6])
    curvature = st.slider("Courbure de la route", 0.0, 1.0, 0.1, 0.01)
    speed_limit = st.selectbox("Limite de vitesse", [25, 35, 45, 60, 70])
    lighting = st.selectbox("Éclairage", ["daylight", "dim", "night"])
    weather = st.selectbox("Météo", ["clear", "rainy", "foggy"])
    num_reported_accidents = st.slider("Nombre d'accidents rapportés", 0, 10, 0)

    # --- Calcul des features du modèle ---
    curv_speed_ratio = curvature * speed_limit
    risk_per_lane = num_reported_accidents / (num_lanes + 1)
    is_bad_weather = int(weather in ['rainy', 'foggy'])
    is_daylight = int(lighting == 'daylight')
    lighting_night = int(lighting == 'night')
    lighting_dim = int(lighting == 'dim')
    weather_foggy = int(weather == 'foggy')

    features = pd.DataFrame([{
        "curv_speed_ratio": curv_speed_ratio,
        "curvature": curvature,
        "lighting_night": lighting_night,
        "speed_limit": speed_limit,
        "lighting_dim": lighting_dim,
        "is_daylight": is_daylight,
        "num_reported_accidents": num_reported_accidents,
        "is_bad_weather": is_bad_weather,
        "risk_per_lane": risk_per_lane,
        "weather_foggy": weather_foggy
    }])

    # --- Bouton prédiction ---
    if st.button("Prédire le risque"):
        pred = model.predict(features)[0] * 100
        st.metric("Risque prédit (%)", f"{pred:.2f}%")

        # --- Classification du risque ---
        if pred < 25:
            niveau = "Faible ✅"
            couleur = "green"
        elif pred < 50:
            niveau = "Moyen ⚠️"
            couleur = "orange"
        else:
            niveau = "Élevé ❌"
            couleur = "red"

        st.markdown(f"### Niveau de risque : <span style='color:{couleur}'>{niveau}</span>", unsafe_allow_html=True)

        # --- Affichage clair ---
        st.write("#### Détails de la route saisie :")
        st.table({
            "Paramètre": ["Type de route", "Nombre de voies", "Courbure", "Limite de vitesse", "Éclairage", "Météo", "Accidents rapportés"],
            "Valeur": [road_type, num_lanes, curvature, speed_limit, lighting, weather, num_reported_accidents]
        })
