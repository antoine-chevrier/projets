import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Nom du fichier de démonstration
DEMO_FILE = "fichier_demo_resultats_course_pour_app_streamlit.csv"

# Titre de l'application
titre_de_cette_application_du_tonnerre = "Ta course de trail: toi, et les autres"
st.title(titre_de_cette_application_du_tonnerre)

# Texte d'introduction
texte_section_intro = (
    f"Sur cette page, tu peux:    \n"
    f"- soit charger un fichier de résultats d'une course de trail - voir info et boutons de téléchargement ci-dessous    \n"
    f"- soit utiliser les données de démonstration - voir bouton ci-dessous"
)

st.markdown(texte_section_intro)

# Bouton pour charger les données de démonstration
if st.button("Pas de fichier ?: essaye avec les données de démonstration"):
    try:
        df = pd.read_csv(DEMO_FILE)
        st.info(f"Affichage des données de démonstration")
        uploaded_file = True
    except FileNotFoundError:
        st.error(f"Le fichier de démonstration '{DEMO_FILE}' n'a pas été trouvé. Veuillez vous assurer qu'il se trouve dans le même répertoire que ce script.")
        df = None
        uploaded_file = False
    except Exception as e:
        st.error(f"Une erreur est survenue lors de la lecture du fichier de démonstration : {e}")
        df = None
        uploaded_file = False
else:
    uploaded_file = False
    df = None

# Instructions pour le fichier CSV
st.info(
    "Veuillez charger votre propre fichier CSV (avec les colonnes : "
    "`categorie_age`, `vitesse_moyenne`, `classement`, `femmes_hommes`) "
    "ou utilisez les données de démonstration ci-dessous."
)

# Upload du fichier CSV (toujours affiché)
uploaded_file_input = st.file_uploader("Choisissez votre fichier CSV", type="csv")
if uploaded_file_input is not None:
    try:
        df = pd.read_csv(uploaded_file_input)
        uploaded_file = True
    except pd.errors.EmptyDataError:
        st.error("Le fichier CSV est vide ou n'a pas pu être lu correctement.")
        df = None
        uploaded_file = False
    except Exception as e:
        st.error(f"Une erreur est survenue lors de la lecture de votre fichier CSV : {e}")
        st.info("[Contactez le support](#contact)")
        df = None
        uploaded_file = False

if uploaded_file and df is not None:
    # Vérification des colonnes
    required_columns = ["categorie_age", "vitesse_moyenne", "classement", "femmes_hommes", "nom_evenement", "date_de_la_course", "distance_course"]
    if not all(col in df.columns for col in required_columns):
        st.error(
            "Le fichier CSV ne contient pas toutes les colonnes requises. "
            f"Veuillez vous assurer qu'il contient : {', '.join(required_columns)}. "
            "[Contactez le support](#contact)"
        )
    else:
        # Informations de la course pour le titre
        nom_evenement = df["nom_evenement"].iloc[0]
        date_course = df["date_de_la_course"].iloc[0]
        distance_course = df["distance_course"].iloc[0]

        # Sélection de la catégorie d'âge
        categories_age = ["Toutes catégories"] + list(df["categorie_age"].unique())
        categorie_age_selectionnee = st.selectbox("Sélectionnez une catégorie d'âge", categories_age)

        # Sélection du genre
        genre_options = ["Tous les participants", "Hommes seulement", "Femmes seulement"]
        genre_selectionnee = st.selectbox("Afficher les résultats pour", genre_options)

        # Filtrage des données par catégorie d'âge
        if categorie_age_selectionnee == "Toutes catégories":
            df_filtre_age = df
        else:
            df_filtre_age = df[df["categorie_age"] == categorie_age_selectionnee]

        # Filtrage des données par genre
        if genre_selectionnee == "Hommes seulement":
            df_filtre = df_filtre_age[df_filtre_age["femmes_hommes"] == "H"]
        elif genre_selectionnee == "Femmes seulement":
            df_filtre = df_filtre_age[df_filtre_age["femmes_hommes"] == "F"]
        else:
            df_filtre = df_filtre_age

        # Création du graphique
        fig, ax = plt.subplots(layout="constrained")
        fig.suptitle(f"{nom_evenement} - {date_course}\n({distance_course})", fontsize=16)

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
st.markdown("Me contacter : `contact.a.chevrier@gmail.com`")
