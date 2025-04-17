import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Nom du fichier de démonstration
DEMO_FILE = "fichier_demo_resultats_course_pour_app_streamlit.csv"

# Titre de l'application (hyper cool et amical)
titre_de_cette_application_du_tonnerre = "Résultats de ta course de trail, toi, et les autres !"
st.title(titre_de_cette_application_du_tonnerre)

# Section d'introduction
texte_section_intro = (
    f"Bienvenue sur cette page super sympa pour explorer tes résultats de course de trail et ceux des autres !\n\n"
    f"Tu as deux options principales pour commencer :\n"
    f"- **Télécharger ton propre fichier CSV** de résultats (si tu en as un).\n"
    f"- **Essayer avec les données de démonstration** si tu n'as pas encore ton fichier sous la main."
)
st.markdown(texte_section_intro)
st.markdown("---")

# Upload du fichier CSV (avec les infos en dessous)
uploaded_file_input = st.file_uploader("Choisis ton fichier CSV de résultats de trail (format .csv)", type="csv")
st.info(
    "ℹ️ **Info fichier CSV :**\n"
    "Ton fichier doit contenir les colonnes suivantes, avec des noms exacts :\n"
    "`categorie_age` (ex: '18-25', '35-45', etc.),\n"
    "`vitesse_moyenne` (nombre avec un point comme séparateur décimal),\n"
    "`classement` (nombre entier),\n"
    "`femmes_hommes` ('H' pour homme, 'F' pour femme),\n"
    "`nom_evenement` (texte, nom de la course),\n"
    "`date_de_la_course` (format AAAA-MM-JJ),\n"
    "`distance_course` (nombre, distance en kilomètres)."
)

# Bouton pour charger les données de démonstration
if st.button("Pas de fichier ? Essaye avec les données de démonstration !"):
    try:
        df = pd.read_csv(DEMO_FILE)
        st.info(f"📊 Affichage des données de démonstration de la course : {df['nom_evenement'].iloc[0]} du {df['date_de_la_course'].iloc[0]} ({df['distance_course'].iloc[0]} km)")
        uploaded_file = True
    except FileNotFoundError:
        st.error(f"⚠️ Le fichier de démonstration '{DEMO_FILE}' n'a pas été trouvé. Assure-toi qu'il est dans le même répertoire que ce script.")
        df = None
        uploaded_file = False
    except Exception as e:
        st.error(f"⚠️ Une erreur est survenue lors de la lecture du fichier de démonstration : {e}")
        df = None
        uploaded_file = False
else:
    uploaded_file = False
    df = None

if uploaded_file_input is not None:
    try:
        df = pd.read_csv(uploaded_file_input)
        uploaded_file = True
    except pd.errors.EmptyDataError:
        st.error("⚠️ Le fichier CSV est vide ou n'a pas pu être lu correctement.")
        df = None
        uploaded_file = False
    except Exception as e:
        st.error(f"⚠️ Une erreur est survenue lors de la lecture de votre fichier CSV : {e}")
        st.info("[Contactez le support](#contact)")
        df = None
        uploaded_file = False

if uploaded_file and df is not None:
    # Vérification des colonnes
    required_columns = ["categorie_age", "vitesse_moyenne", "classement", "femmes_hommes", "nom_evenement", "date_de_la_course", "distance_course"]
    if not all(col in df.columns for col in required_columns):
        st.error(
            "⚠️ Le fichier CSV ne contient pas toutes les colonnes requises. "
            f"Veuillez vérifier qu'il contient bien : {', '.join(required_columns)}. "
            "[Contact](#contact)"
        )
    else:
        # Informations de la course pour le titre
        nom_evenement = df["nom_evenement"].iloc[0]
        date_course = df["date_de_la_course"].iloc[0]
        distance_course = df["distance_course"].iloc[0]

        # Sélection de la catégorie d'âge
        categories_age = ["Toutes catégories"] + list(df["categorie_age"].unique())
        categorie_age_selectionnee = st.selectbox("🏃‍♂️ Sélectionne la catégorie d'âge", categories_age)

        # Sélection du genre
        genre_options = ["Tous les participants", "Hommes seulement", "Femmes seulement"]
        genre_selectionne = st.selectbox("🧑‍🤝‍🧑‍➡️ Afficher les résultats pour", genre_options)

        # Filtrage des données par catégorie d'âge
        if categorie_age_selectionnee == "Toutes catégories":
            df_filtre_age = df
        else:
            df_filtre_age = df[df["categorie_age"] == categorie_age_selectionnee]

        # Filtrage des données par genre
        if genre_selectionne == "Hommes seulement":
            df_filtre = df_filtre_age[df_filtre_age["femmes_hommes"] == "H"]
        elif genre_selectionnee == "Femmes seulement":
            df_filtre = df_filtre_age[df_filtre_age["femmes_hommes"] == "F"]
        else:
            df_filtre = df_filtre_age

        # Création du graphique
        fig, ax = plt.subplots(layout="constrained")
        fig.suptitle(f"{nom_evenement}\n{date_course} - Trail de {distance_course} km", fontsize=14, fontweight="bold")

        # Affichage de tous les points en arrière-plan (gris clair, plus petit et transparent)
        ax.scatter(df["classement"], df["vitesse_moyenne"], color="lightgray", alpha=0.3, s=10, label="Tous les participants")

        # Affichage des points sélectionnés (plus petits et transparents)
        for genre, data in df_filtre.groupby("femmes_hommes"):
            if genre == "H":
                ax.scatter(data["classement"], data["vitesse_moyenne"], label="Hommes", color="blue", alpha=0.6, s=20)
            elif genre == "F":
                ax.scatter(data["classement"], data["vitesse_moyenne"], label="Femmes", color="red", alpha=0.6, s=20)

        ax.set_xlabel("Classement")
        ax.set_ylabel("Vitesse moyenne")
        ax.legend()

        # Affichage du graphique dans Streamlit
        st.pyplot(fig)

# Section Contact
st.markdown("---")
st.markdown("<h2 id='contact'>Contact</h2>", unsafe_allow_html=True)
st.markdown("Pour toute question ou suggestion, contacte : `contact.a.chevrier@gmail.com`")
