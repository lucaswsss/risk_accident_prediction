import pandas as pd
import streamlit as st
import requests
import joblib
import numpy as np
import random
import loguru as logger
from frontend.pages.jeu import generer_route, jeu
from frontend.pages.accueil import accueil


st.set_page_config(page_title="Risques d'accidents", layout="wide", page_icon="🚗")


st.sidebar.title("Navigation")
pages=st.sidebar.radio(["Accueil", "Explorations des données", "Prédiction des accidents", "Jeu des prédictions", "A propos de l'application"])

if pages == "Accueil":
    accueil.accueil()
if pages == "Jeu des prédictions":
    jeu.jeu()