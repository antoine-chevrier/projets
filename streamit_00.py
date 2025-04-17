import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Titre de l'application
st.title("V02 - H/F Visualisation des performances de course à pied")

# Upload du fichier CSV
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

if uploaded_file is not None:
    # Lecture du fichier CSV
    df = pd.read_csv(uploaded_file)

    # Vérification des colonnes
    if "categorie_age" not in df.columns or "vitesse_moyenne" not in df.columns or "classement" not in df.columns or "femmes_hommes" not in df.columns:
        st.error("Le fichier CSV doit contenir les colonnes 'categorie_age', 'vitesse_moyenne', 'classement' et 'femmes_hommes'.")
    else:
        # Sélection de la catégorie d'âge
        categories_age = df["categorie_age"].unique()
        categorie_age_selectionnee = st.selectbox("Sélectionnez une catégorie d'âge", categories_age)

        # Sélection du genre
        genre_options = ["Tous", "Hommes", "Femmes"]
        genre_selectionne = st.selectbox("Afficher les résultats pour", genre_options)

        # Filtrage des données par catégorie d'âge
        df_filtre_age = df[df["categorie_age"] == categorie_age_selectionnee]

        # Filtrage des données par genre
        if genre_selectionne == "Hommes":
            df_filtre = df_filtre_age[df_filtre_age["femmes_hommes"] == "H"]
        elif genre_selectionne == "Femmes":
            df_filtre = df_filtre_age[df_filtre_age["femmes_hommes"] == "F"]
        else:
            df_filtre = df_filtre_age

        # Création du graphique avec différenciation des couleurs par genre
        fig, ax = plt.subplots()
        for genre, data in df_filtre.groupby("femmes_hommes"):
            if genre == "H":
                ax.scatter(data["classement"], data["vitesse_moyenne"], label="Hommes", color="blue")
            elif genre == "F":
                ax.scatter(data["classement"], data["vitesse_moyenne"], label="Femmes", color="red")

        ax.set_xlabel("Classement")
        ax.set_ylabel("Vitesse moyenne")
        ax.set_title(f"Vitesse moyenne en fonction du classement ({categorie_age_selectionnee})")
        ax.legend()

        # Affichage du graphique dans Streamlit
        st.pyplot(fig)
else:
    st.write("Veuillez charger un fichier CSV.")
