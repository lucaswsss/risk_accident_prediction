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
    df=df.drop["id"]

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
        st.header("📈 Lien entre variables numériques et risque d'accident")

        if "accident_risk" not in df.columns:
            st.warning("⚠️ La variable 'accident_risk' n'est pas présente dans le dataset.")
        else:
            var_num_corr = st.selectbox("Choisissez une variable numérique :", colonnes_num, key="cor_num")
            fig, ax = plt.subplots(figsize=(7, 4))
            sns.scatterplot(
                x=df[var_num_corr],
                y=df["accident_risk"],
                hue=df["accident_risk"],
                palette="coolwarm",
                ax=ax,
            )
            ax.set_title(f"Relation entre {var_num_corr} et le risque d'accident", fontsize=14)
            st.pyplot(fig)

            # Matrice de corrélation globale
            st.subheader("🔗 Matrice de corrélation (variables numériques)")
            corr = df[colonnes_num + ["accident_risk"]].corr()
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(corr, annot=True, cmap="magma", fmt=".2f", ax=ax)
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
