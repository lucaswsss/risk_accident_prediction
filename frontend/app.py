import pandas as pd
import streamlit as st
import requests

st.set_page_config(page_title="Risques d'accidents", layout="wide")

st.subheader("Prédiction du risque d'accident selon les caractéristiques des routes")

API_URL = "https://risk-accident-prediction.onrender.com"

# Ajouter un score
requests.post(f"{API_URL}/add_score", json={"username": "Sara", "score": 12})

# Récupérer le leaderboard
res = requests.get(f"{API_URL}/leaderboard")
leaderboard = res.json()
st.write(leaderboard)