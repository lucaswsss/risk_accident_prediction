import pandas as pd
import streamlit as st
import requests
import joblib
import numpy as np
import random
import logging

# --- Configuration du logger ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Risques d'accidents", layout="wide")

logger.info("Chargement du modèle...")
model = joblib.load("models/meilleure_modele.pkl")
logger.info("Modèle chargé avec succès.")

API_URL = "https://risk-accident-prediction.onrender.com"
logger.info(f"API_URL défini sur : {API_URL}")

# --- Initialisation des variables session ---
if "route" not in st.session_state:
    st.session_state.route = None
if "prediction_user" not in st.session_state:
    st.session_state.prediction_user = None
if "prediction_done" not in st.session_state:
    st.session_state.prediction_done = False

st.title("Jeu : Prédire le risque d'accident 🚗💥")
st.subheader("Entre ton pseudo, génère une route et tente de deviner le risque d’accident le plus proche du modèle !")

pseudo = st.text_input("Ton pseudo")

# --- Fonction de génération d'une route ---
def generer_route():
    road_type = random.choice(['highway', 'rural', 'urban'])
    num_lanes = random.randint(1, 6)
    curvature = round(random.uniform(0.0, 1.0), 2)
    speed_limit = random.choice([25, 35, 45, 60, 70])
    lighting = random.choice(['daylight', 'dim', 'night'])
    weather = random.choice(['clear', 'rainy', 'foggy'])
    road_signs = random.choice(['Oui', 'Non'])
    public_road = random.choice(['Oui', 'Non'])
    time_of_day = random.choice(['morning', 'afternoon', 'evening'])
    holiday = random.choice(['Oui', 'Non'])
    school_season = random.choice(['Oui', 'Non'])
    num_reported_accidents = random.randint(0, 6)

    curv_speed_ratio = curvature * speed_limit
    risk_per_lane = num_reported_accidents / (num_lanes + 1)
    is_bad_weather = int(weather in ['rainy', 'foggy'])
    is_daylight = int(lighting == 'daylight')
    lighting_night = int(lighting == 'night')
    lighting_dim = int(lighting == 'dim')
    weather_foggy = int(weather == 'foggy')

    route = {
        "road_type": road_type,
        "num_lanes": num_lanes,
        "curvature": curvature,
        "speed_limit": speed_limit,
        "lighting": lighting,
        "weather": weather,
        "num_reported_accidents": num_reported_accidents,
        "curv_speed_ratio": curv_speed_ratio,
        "risk_per_lane": risk_per_lane,
        "is_bad_weather": is_bad_weather,
        "is_daylight": is_daylight,
        "lighting_night": lighting_night,
        "lighting_dim": lighting_dim,
        "weather_foggy": weather_foggy,
        "road_signs_presents": road_signs,
        "public_road": public_road,
        "time_of_day": time_of_day,
        "holiday": holiday,
        "school_season": school_season
    }
    return route

# --- Bouton pour générer une route ---
if st.button("Générer une route"):
    if pseudo == "":
        st.warning("Merci de saisir ton pseudo avant de jouer !")
    else:
        st.session_state.route = generer_route()
        st.session_state.prediction_done = False
        logger.info(f"Nouvelle route générée pour {pseudo} : {st.session_state.route}")

# --- Si une route est active ---
if st.session_state.route:
    route = st.session_state.route
    st.write("### 🚦 Route générée :")
    data = {
        "Caractéristique": [
            "Type de route", "Nombre de voies", "Courbure",
            "Limite de vitesse", "Éclairage", "Météo",
            "Accidents rapportés", "Présence de panneaux",
            "Route publique", "Moment de la journée", "Vacances", "Saison écolière"
        ],
        "Valeur": [
            route["road_type"], route["num_lanes"], route["curvature"],
            route["speed_limit"], route["lighting"], route["weather"],
            route["num_reported_accidents"], route["road_signs_presents"],
            route["public_road"], route["time_of_day"],
            route["holiday"], route["school_season"]
        ]
    }
    df = pd.DataFrame(data)
    st.table(df)

    # --- Entrée de la prédiction utilisateur ---
    st.session_state.prediction_user = st.number_input("Ton estimation du risque (%)", min_value=0.0, max_value=100.0, step=0.1)

    if st.button("Soumettre ta prédiction"):
        st.session_state.prediction_done = True
        logger.info(f"Prédiction utilisateur soumise : {st.session_state.prediction_user}% pour {pseudo}")

# --- Après soumission de la prédiction ---
if st.session_state.prediction_done and st.session_state.route:
    route = st.session_state.route
    pred_user = st.session_state.prediction_user

    features_model = pd.DataFrame([{
        "curv_speed_ratio": route["curv_speed_ratio"],
        "curvature": route["curvature"],
        "lighting_night": route["lighting_night"],
        "speed_limit": route["speed_limit"],
        "lighting_dim": route["lighting_dim"],
        "is_daylight": route["is_daylight"],
        "num_reported_accidents": route["num_reported_accidents"],
        "is_bad_weather": route["is_bad_weather"],
        "risk_per_lane": route["risk_per_lane"],
        "weather_foggy": route["weather_foggy"]
    }])

    pred_model = model.predict(features_model)[0] * 100
    diff = abs(pred_user - pred_model)

    st.write(f"### 🧠 Prédiction du modèle : **{pred_model:.2f}%**")
    st.write(f"### 📏 Écart avec ta prédiction : **{diff:.2f}**")
    st.write(f"## 🎯 Ton score final : {diff:.0f}")

    logger.info(f"Score calculé pour {pseudo} : {diff:.2f} (utilisateur {pred_user:.2f}%, modèle {pred_model:.2f}%)")

    # --- Envoi au leaderboard ---
    try:
        res = requests.post(f"{API_URL}/add_score", json={"pseudo": pseudo, "score": diff})
        if res.status_code == 200:
            logger.info(f"Score envoyé avec succès au leaderboard pour {pseudo}.")
        else:
            logger.warning(f"Échec de l'envoi du score (status {res.status_code}).")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du score : {e}")

    # Réinitialisation
    st.session_state.route = None
    st.session_state.prediction_done = False

# --- Affichage leaderboard ---
if pseudo :
    st.subheader("🏆 Leaderboard")
    logger.info("Récupération du leaderboard depuis l'API...")
    try:
        res = requests.get(f"{API_URL}/leaderboard")
        if res.status_code == 200:
            leaderboard = res.json()
            logger.info(f"Leaderboard récupéré ({len(leaderboard)} entrées).")
        else:
            leaderboard = []
            logger.warning(f"Échec récupération leaderboard : {res.status_code}")
    except Exception as e:
        leaderboard = []
        logger.error(f"Erreur lors de la récupération du leaderboard : {e}")

    df = pd.DataFrame(leaderboard, columns=["pseudo", "score"])

    if not df.empty:
        df = df.sort_values(by="score", ascending=True)
        logger.info("Leaderboard trié par score.")
        df.index = np.arange(1, len(df) + 1)
        df.index.name = "Rang"

        # --- Attribution des médailles ---
        medals = {1: "🥇", 2: "🥈", 3: "🥉"}
        df.insert(0, "Médaille", [medals.get(i, "") for i in df.index])

        # --- Affichage final ---
        st.dataframe(df)
        logger.info("Leaderboard affiché avec médailles et index réinitialisé.")

    else:
        logger.info("Leaderboard vide.")
