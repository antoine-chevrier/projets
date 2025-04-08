import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Titre de l'application
st.title("Visualisation des performances de course à pied")

# Upload du fichier CSV
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

if uploaded_file is not None:
    # Lecture du fichier CSV
    df = pd.read_csv(uploaded_file)

    # Vérification des colonnes
    if "categorie_age" not in df.columns or "vitesse_moyenne" not in df.columns or "classement" not in df.columns:
        st.error("Le fichier CSV doit contenir les colonnes 'categorie_age', 'vitesse_moyenne' et 'classement'.")
    else:
        # Sélection de la catégorie d'âge
        categories_age = df["categorie_age"].unique()
        categorie_age_selectionnee = st.selectbox("Sélectionnez une catégorie d'âge", categories_age)

        # Filtrage des données
        df_filtre = df[df["categorie_age"] == categorie_age_selectionnee]

        # Création du graphique
        fig, ax = plt.subplots()
        ax.scatter(df_filtre["classement"], df_filtre["vitesse_moyenne"])
        ax.set_xlabel("Classement")
        ax.set_ylabel("Vitesse moyenne")
        ax.set_title(f"Vitesse moyenne en fonction du classement ({categorie_age_selectionnee})")

        # Affichage du graphique dans Streamlit
        st.pyplot(fig)
else:
    st.write("Veuillez charger un fichier CSV.")
