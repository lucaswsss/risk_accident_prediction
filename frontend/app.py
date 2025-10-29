import pandas as pd
import streamlit as st
import requests
import joblib
import numpy as np
import random

st.set_page_config(page_title="Risques d'accidents", layout="wide")

model = joblib.load("models/meilleure_modele.pkl")

API_URL = "https://risk-accident-prediction.onrender.com"

if "routes" not in st.session_state:
    st.session_state.routes = []
if "user_predictions" not in st.session_state:
    st.session_state.user_predictions = []
if "tour" not in st.session_state:
    st.session_state.tour = 0

st.title("Jeu : Prédire le risque d'accident et faites le meilleure score")
st.subheader("Entrez votre pseudo, démarrez une nouvelle partie puis générez 3 parties et essayer de faire le meilleure score de prédiction moyen !")

pseudo = st.text_input("Ton pseudo")

# --- Bouton pour réinitialiser la partie ---
if st.button("Nouvelle partie"):
    st.session_state.routes = []
    st.session_state.user_predictions = []
    st.session_state.tour = 0
    st.success("Nouvelle partie démarrée !")

def generer_route():
    road_type = random.choice(['highway','rural','urban'])
    num_lanes = random.randint(1, 6)
    curvature = round(random.uniform(0.0, 1.0), 2)
    speed_limit = random.choice([25, 35, 45, 60, 70])
    lighting = random.choice(['daylight','dim','night'])
    weather = random.choice(['clear','rainy','foggy'])
    road_signs = random.choice(['Oui','Non'])
    public_road = random.choice(['Oui','Non'])
    time_of_day = random.choice(['morning','afternoon','evening'])
    holiday = random.choice(['Oui','Non'])
    school_season = random.choice(['Oui','Non'])
    num_reported_accidents = random.randint(0, 6)
    
    
    curv_speed_ratio = curvature * speed_limit
    risk_per_lane = num_reported_accidents / (num_lanes + 1)
    is_bad_weather = int(weather in ['rainy','foggy'])
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
        "road_signs_presents":road_signs,
        "public_road":public_road,
        "time_of_day":time_of_day,
        "holiday":holiday,
        "school_season":school_season
    }
    return route
truc_machin=True
if st.button("Générer une route"):
    truc_machin=False
    if pseudo == "":
        st.warning("Merci de saisir ton pseudo avant de jouer !")
    else:
        route = generer_route()
        st.session_state.current_route = route
        st.session_state.tour += 1
        st.session_state.current_pred = 50
        st.write(f"### Route {st.session_state.tour}")
        
        
if "current_route" in st.session_state:
    route=st.session_state.current_route    
    data = {
                "Caractéristique": [
                    "Type de route", "Nombre de voies", "Courbure",
                    "Limite de vitesse", "Éclairage", "Météo", "Accidents rapportés", "Présence de panneaux", "Route publique", "Moment de la journée","Vacances","Saison écolière"
                ],
                "Valeur": [
                    route["road_type"], route["num_lanes"], route["curvature"],
                    route["speed_limit"], route["lighting"], route["weather"],
                    route["num_reported_accidents"], route["road_signs_presents"], route["public_road"],route["time_of_day"],route["holiday"],route["school_season"]
                ]
            }

    df = pd.DataFrame(data)
    st.table(df)

        # Slider pour prédiction utilisateur
    st.session_state.current_pred = st.number_input("Ton estimation du risque (%)")
        
    if st.button("Soumettre ta prédiction") :
        
        st.session_state.user_predictions.append(st.session_state.current_pred)
        st.session_state.routes.append(route)
        route=st.session_state.routes[-1]
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

            
        diff = abs(st.session_state.current_pred - pred_model)
        st.write(f"**Prédiction du modèle:** {pred_model:.2f}%")
        st.write(f"**Écart avec ta prédiction:** {diff:.2f}%")
        truc_machin=1
        del st.session_state.current_route


if st.session_state.tour == 3 and truc_machin==1:
    diffs = [abs(u - model.predict(pd.DataFrame([{
        "curv_speed_ratio": r["curv_speed_ratio"],
        "curvature": r["curvature"],
        "lighting_night": r["lighting_night"],
        "speed_limit": r["speed_limit"],
        "lighting_dim": r["lighting_dim"],
        "is_daylight": r["is_daylight"],
        "num_reported_accidents": r["num_reported_accidents"],
        "is_bad_weather": r["is_bad_weather"],
        "risk_per_lane": r["risk_per_lane"],
        "weather_foggy": r["weather_foggy"]
    }]))[0]) for r, u in zip(st.session_state.routes, st.session_state.user_predictions)]
    
    score_final = max(0, np.mean(diffs))  # score inversé pour leaderboard
    st.success(f"Score final de la partie : {score_final:.2f}")

    # Envoyer score au leaderboard
    requests.post(f"{API_URL}/add_score", json={"pseudo": pseudo, "score": score_final})

    # Réinitialiser pour nouvelle partie
    st.session_state.routes = []
    st.session_state.user_predictions = []
    st.session_state.tour = 0

# --- Affichage leaderboard ---
st.subheader("Leaderboard")
res = requests.get(f"{API_URL}/leaderboard")
if res.status_code == 200:
    try:
        leaderboard = res.json()
    except:
        leaderboard = []
else:
    leaderboard = []

df = pd.DataFrame(leaderboard, columns=["pseudo", "score"])

if not df.empty:
    df = df.sort_values(by="score", ascending=True)

st.dataframe(df)
