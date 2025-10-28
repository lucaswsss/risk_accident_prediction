import pandas as pd
import streamlit as st
import requests

st.set_page_config(page_title="Risques d'accidents", layout="wide")

st.subheader("Prédiction du risque d'accident selon les caractéristiques des routes")

API_URL = "https://risk-accident-prediction.onrender.com"

# Ajouter un score
requests.post(f"{API_URL}/add_score", json={"pseudo": "Sarayandm", "score": 12})

# Récupérer le leaderboard
res = requests.get(f"{API_URL}/leaderboard")

if res.status_code == 200:
    try:
        leaderboard = res.json()
    except requests.exceptions.JSONDecodeError:
        leaderboard = [] 
else:
    leaderboard = []

if st.button("Réinitialiser le leaderboard"):
    response = requests.post(f"{API_URL}/reset_leaderboard")
    if response.status_code == 200:
        st.success("Leaderboard réinitialisé !")
    else:
        st.error("Impossible de réinitialiser le leaderboard")

df = pd.DataFrame(leaderboard)
st.subheader("Leaderboard")
st.dataframe(df) 