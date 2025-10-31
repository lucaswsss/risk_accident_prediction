import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Activation du style global seaborn
sns.set(style="whitegrid", palette="viridis")

def lancer_EDA():
    st.title("🔍 Exploration des données")

    st.write("""
    Cette section te permet d'explorer la répartition des variables du jeu de données, 
    aussi bien **numériques** que **catégorielles**, et d’analyser leur lien 
    avec la variable cible : **`accident_risk`** 🚧.
    """)

    # --- Chargement du jeu de données

    df = pd.read_csv("data/train.csv")
    df.drop("id", axis=1, inplace=True)

    # --- Identification des types de variables
    colonnes_num = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    colonnes_cat = df.select_dtypes(exclude=["int64", "float64"]).columns.tolist()

    st.write(f"**Variables numériques détectées :** {', '.join(colonnes_num)}")
    st.write(f"**Variables catégorielles détectées :** {', '.join(colonnes_cat)}")

    # --- Onglets d’exploration
    tab1, tab2, tab3 = st.tabs([
        "📊 Répartition des variables",
        "📈 Corrélation avec accident_risk",
        "🎭 Analyse par catégorie"
    ])

    # ============================
    # 📊 Répartition des variables
    # ============================
    with tab1:
        st.header("📊 Répartition des variables")

        sous_tab1, sous_tab2 = st.tabs(["🔢 Numériques", "🔠 Catégorielles"])

        # Numériques
        with sous_tab1:
            st.subheader("Distribution des variables numériques")
            var_num = st.selectbox("Choisissez une variable numérique :", colonnes_num, key="dist_num")
            fig, ax = plt.subplots(figsize=(7, 4))
            sns.histplot(df[var_num], kde=True, color="#4C72B0", ax=ax)
            ax.set_title(f"Distribution de {var_num}", fontsize=14)
            st.pyplot(fig)

        # Catégorielles
        with sous_tab2:
            st.subheader("Répartition des variables catégorielles")
            var_cat = st.selectbox("Choisissez une variable catégorielle :", colonnes_cat, key="repar_cat")
            fig, ax = plt.subplots(figsize=(7, 4))
            order = df[var_cat].value_counts().index
            sns.countplot(y=var_cat, data=df, order=order, palette="mako", ax=ax)
            ax.set_title(f"Répartition de {var_cat}", fontsize=14)
            st.pyplot(fig)

    # =================================================
    # 📈 Corrélation entre les variables numériques et la cible
    # =================================================
    with tab2:
        st.header("📈 Corrélation entre les variables numériques")

        if "accident_risk" not in df.columns:
            st.warning("⚠️ La variable 'accident_risk' n'est pas présente dans le dataset.")
        else:
            # Calcul de la matrice de corrélation
            corr = df[colonnes_num].corr()

            # Création de la figure
            fig, ax = plt.subplots(figsize=(10, 6))

            # Heatmap style feu tricolore
            sns.heatmap(
                corr,
                annot=True,                
                fmt=".2f",                 
                cmap="RdYlGn_r",           
                center=0,                  
                linewidths=0.5,            
                cbar_kws={"shrink": 0.8},  
                ax=ax
            )

            ax.set_title("Matrice de corrélation entre variables numériques et risque d'accident", fontsize=14, pad=12)
            st.pyplot(fig)

    # =================================================
    # 🎭 Variables catégorielles vs accident_risk
    # =================================================
    with tab3:
        st.header("🎭 Comparaison des variables catégorielles avec le risque d'accident")

        if "accident_risk" not in df.columns:
            st.warning("⚠️ La variable 'accident_risk' n'est pas présente dans le dataset.")
        else:
            var_cat_box = st.selectbox("Choisissez une variable catégorielle :", colonnes_cat, key="cor_cat")
            fig, ax = plt.subplots(figsize=(7, 4))
            sns.boxplot(x=var_cat_box, y="accident_risk", data=df, palette="cubehelix", ax=ax)
            ax.set_title(f"Distribution du risque selon {var_cat_box}", fontsize=14)
            st.pyplot(fig)
