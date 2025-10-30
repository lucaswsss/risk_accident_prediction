import pandas as pd
import streamlit as st
import requests
import joblib
import numpy as np
import random
import loguru as logger

def lancer_accueil():

    st.title("Bienvenue sur l'application de prédictions des accidents routiers")

    st.subheader("L'application se décompose en 4 parties")
    st.write("- Une exploration des données afin de mieux comprendre quels facteurs influencent le plus le risque d'accidents")
    st.write("- Une page de prédiction du risque d'accident avec les paramètres de votre choix")
    st.write("- Un jeu de prédiction pour voir à quel point vous avez compris ce qui impactait les risques d'accidents. Vous essayerez de faire le score le plus proche de notre modèle parmi tous les participants !")
    st.write("- Une page d'informations concernant le contexte du projet et les outils utilisés")

    st.write("**Naviguez à votre guise sur le menu à gauche afin de découvrir les différentes pages !")