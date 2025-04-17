import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Nom du fichier de démonstration
DEMO_FILE = "fichier_demo_resultats_course_pour_app_streamlit.csv"

# Titre de l'application
st.title("Visualisation des performances de course à pied")

# Instructions pour le fichier CSV
st.info(
    "Veuillez charger votre propre fichier CSV (avec les colonnes : "
    "`categorie_age`, `vitesse_moyenne`, `classement`, `femmes_hommes`) "
    "ou utilisez les données de démonstration ci-dessous."
)

# Bouton pour charger les données de démonstration
if st.button("Charger les données de démonstration"):
    try:
        df = pd.read_csv(DEMO_FILE)
        st.info(f"Affichage des données de la course : {df['nom_evenement'].iloc[0]} du {df['date_de_la_course'].iloc[0]} ({df['distance_course'].iloc[0]})")
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
    # ... (le reste de votre code pour la vérification des colonnes et l'affichage du graphique)
