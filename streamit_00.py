import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Titre de l'application
st.title("Visualisation des performances de course à pied")

# Instructions pour le fichier CSV
st.info(
    "Veuillez charger un fichier CSV avec les colonnes suivantes : "
    "`categorie_age` (texte), `vitesse_moyenne` (nombre), "
    "`classement` (nombre), `femmes_hommes` ('H' ou 'F')."
)

# Upload du fichier CSV
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

if uploaded_file is not None:
    try:
        # Lecture du fichier CSV
        df = pd.read_csv(uploaded_file)

        # Vérification des colonnes
        required_columns = ["categorie_age", "vitesse_moyenne", "classement", "femmes_hommes"]
        if not all(col in df.columns for col in required_columns):
            st.error(
                "Le fichier CSV ne contient pas les colonnes requises. "
                f"Veuillez vous assurer qu'il contient : {', '.join(required_columns)}. "
                "[Contactez le support](#contact)"  # Lien vers la section contact (à ajouter plus tard si souhaité)
            )
        else:
            # Sélection de la catégorie d'âge
            categories_age = ["Toutes catégories"] + list(df["categorie_age"].unique())
            categorie_age_selectionnee = st.selectbox("Sélectionnez une catégorie d'âge", categories_age)

            # Sélection du genre
            genre_options = ["Tous les participants", "Hommes seulement", "Femmes seulement"]
            genre_selectionne = st.selectbox("Afficher les résultats pour", genre_options)

            # Filtrage des données par catégorie d'âge
            if categorie_age_selectionnee == "Toutes catégories":
                df_filtre_age = df
            else:
                df_filtre_age = df[df["categorie_age"] == categorie_age_selectionnee]

            # Filtrage des données par genre
            if genre_selectionne == "Hommes seulement":
                df_filtre = df_filtre_age[df_filtre_age["femmes_hommes"] == "H"]
            elif genre_selectionne == "Femmes seulement":
                df_filtre = df_filtre_age[df_filtre_age["femmes_hommes"] == "F"]
            else:
                df_filtre = df_filtre_age

            # Création du graphique
            fig, ax = plt.subplots()

            # Affichage de tous les points en arrière-plan (gris clair)
            ax.scatter(df["classement"], df["vitesse_moyenne"], color="lightgray", alpha=0.5, label="Tous les participants")

            # Affichage des points sélectionnés avec des couleurs spécifiques
            for genre, data in df_filtre.groupby("femmes_hommes"):
                if genre == "H":
                    ax.scatter(data["classement"], data["vitesse_moyenne"], label="Hommes", color="blue")
                elif genre == "F":
                    ax.scatter(data["classement"], data["vitesse_moyenne"], label="Femmes", color="red")

            ax.set_xlabel("Classement")
            ax.set_ylabel("Vitesse moyenne")
            ax.set_title(f"Vitesse moyenne en fonction du classement ({categorie_age_selectionnee}, {genre_selectionne})")
            ax.legend()

            # Affichage du graphique dans Streamlit
            st.pyplot(fig)

    except pd.errors.EmptyDataError:
        st.error("Le fichier CSV est vide ou n'a pas pu être lu correctement.")
    except Exception as e:
        st.error(f"Une erreur est survenue lors de la lecture du fichier CSV : {e}")
        st.info("[Contactez le support](#contact)") # Lien en cas d'autre erreur

else:
    st.write("Veuillez charger un fichier CSV.")

# Section Contact (optionnelle, pour illustrer le lien)
st.markdown("---")
st.markdown("<h2 id='contact'>Contactez le support</h2>", unsafe_allow_html=True)
st.write("Si vous rencontrez des problèmes, veuillez contacter : votre.email@exemple.com")
