import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io


# ============================================================================
# 🧰 CONSTANTES ISSUS DU FICHIER DE DÉMO
# ============================================================================

CHEMIN_DEMO = Path("fichier_demo.csv")
NOM_DU_TRAIL_DEMO = pd.read_csv(CHEMIN_DEMO).nom_du_trail.unique()[0]
DATE_DU_TRAIL_DEMO = pd.read_csv(CHEMIN_DEMO).date_du_trail.unique()[0]

# ============================================================================
# 🧰 FONCTIONS DE CHARGEMENT DES DONNÉES
# ============================================================================

def charger_donnees(fichier_utilisateur, utiliser_demo):
    texte_demo = (
        #f"Choisis maintenant les catégories à afficher (Femmes / Hommes / Ages)"
        f"Pour la démo, on prend les résultats du sympathique événement **{NOM_DU_TRAIL_DEMO} du {DATE_DU_TRAIL_DEMO}**.   \n"
    )
    if fichier_utilisateur:
        df = pd.read_csv(fichier_utilisateur)
        st.markdown(f"Nickel ! Ton fichier est chargé avec succès !")
        
    elif utiliser_demo:
        if CHEMIN_DEMO.exists():
            df = pd.read_csv(CHEMIN_DEMO)
            st.markdown(f"{texte_demo}")
            
        else:
            st.error("❌ Fichier de démonstration introuvable.")
            df = None
    else:
        df = None
    return df

def charge_le_fichier_de_demo():
    return pd.read_csv(CHEMIN_DEMO)

# ============================================================================
# 🧰 FONCTIONS UTILITAIRES
# ============================================================================

# CLASSEMENT D'UNE SOUS-LISTE SELON UNE LISTE PRINCIPALE ORDONNÉE
# pour les catégories FFA
def reorder_subset(main_list, subset_list):
  """
  Reorders a subset list to match the order of a main list.

  Args:
    main_list: A list of unique strings, ordered.
    subset_list: A subset of main_list, but not necessarily in the same order.

  Returns:
    A new list containing the elements of subset_list, ordered as in main_list.
  """
  ordered_subset = []
  main_set = set(main_list) # for efficient lookup

  for item in main_list:
    if item in subset_list:
      ordered_subset.append(item)

  return ordered_subset

# AFFICHAGE DES 5 PREMIÈRES LIGNES DU TABLEAU DE DONNÉES 
def afficher_dataframe(df):
    if df is not None:
        st.markdown("Voici les premières ligne du tableau de résultats du trail: ")
        st.dataframe(df.head(5))
    return df

# ============================================================================
# 🧰 FONCTIONS DES SECTIONS DE LA PAGE
# ============================================================================

# ----------------------------------------------------------------------------
# BLOC D'EN TETE
# ----------------------------------------------------------------------------

def affiche_la_section_entete():
    # un nom pour l'app un peu évocateur 
    # sans se prendre la tête
    # sans se chopper le melon (parce qu'il y en a quand même 
    # qui ont bien choppé l'melon dans cet univers du trail ... c'est dingue !)
    nom_de_l_app = "GraphicTrailRunners" 
    titre_principal = (
        f"{nom_de_l_app}"
    )
    sous_titre = (
        f"Un simple graphique de résultats d'un trail: "
        f"vitesse/classement par catégorie d'âges + femmes/hommes    \n"
        f"🏃‍♀️🏃‍♂️🏃‍♀️🏃"
        )
    menu_haut_de_page = (
        f"[Explications](#explications)"
        f" | "
        f"[Contact](#contact)"
    )
    st.title(titre_principal)
    st.markdown(sous_titre)
    st.markdown(menu_haut_de_page)
    
# ----------------------------------------------------------------------------
# BLOC DE SÉLECTION DE FICHIER
# ----------------------------------------------------------------------------

def bloc_selection_donnees():
    st.markdown("## Étape 1. 📂 Choisis le fichier à utiliser:")
    st.markdown("""
    *Voir les [explications](#explications) pour connaître
    le format de fichier à utiliser. Ou [contacte-moi](#contact) 
    si tu as besoin d'aide.*
    """)
    choix_1 = "Téléversement de ton fichier de résultat de trail"
    choix_2= "Utilisation du fichier de démo"
    option = st.radio(
        "",
        [choix_1, choix_2 ],
        index=None,
        label_visibility="collapsed"
    )
    

    fichier = None
    use_demo = False

    if option == choix_1:
        fichier = st.file_uploader("📎 Téléverse ton fichier CSV :", type="csv")
    elif option == choix_2:
        use_demo = True
    else:
        st.warning("👆 Merci de faire un choix ci-dessus.")

    return fichier, use_demo


# ----------------------------------------------------------------------------
# BLOC DE SÉLECTION DES CATÉGORIES
# ----------------------------------------------------------------------------
    
def bloc_filtres_selection(df):
    # Sélection par sexe avec boutons horizontaux
    st.markdown("## Étape 2. Choisis la catégorie Femme ou Homme:")
    sexe_selection = st.radio(
        "2.Choisis la catégorie Femme ou Homme:",
        ["Hommes et Femmes", "Femmes", "Hommes"],
        horizontal=True,
        index=0,
        label_visibility="collapsed"
    )

    if sexe_selection == "Femmes":
        valeurs_sexe = ["F"]
    elif sexe_selection == "Hommes":
        valeurs_sexe = ["H"]
    else:
        valeurs_sexe = ["F", "H"]

    # Filtrage du DataFrame selon le sexe
    df_filtre_sexe = df[df["femme_ou_homme"].isin(valeurs_sexe)]

    # Sélection par catégorie d'âge
    liste_cat_age_ffa = [
        'BB', 'EA', 'PO', 'BE', 'MI', 
        'CA', 'JU', 'ES', 'SE', 'MA', 
        'M0', 'M1', 'M2', 'M3', 'M4', 
        'M5', 'M6', 'M7', 'M8', 'M9', 
        'M10']
    
    # categories_age_disponibles = df_filtre_sexe["categorie_age_ffa"].unique()
    # Extraire les catégories présentes dans le fichier
    categories_age_disponibles = df_filtre_sexe["categorie_age_ffa"].dropna().unique().tolist()
    # Trier selon la FFA
    categories_ordonnee = reorder_subset(liste_cat_age_ffa, categories_age_disponibles)

    st.markdown("## Étape 3. Choisis une catégorie d’âge :")
    categorie_selection = st.selectbox(
        "3.Choisis une catégorie d’âge :",
        options = ["Toutes les catégories"]+categories_ordonnee,
        #options=np.insert(categories_ordonnee, 0, "Toutes les catégories"),
        index=0,
        label_visibility="collapsed"
    )

    if categorie_selection != "Toutes les catégories":
        df_filtre = df_filtre_sexe[df_filtre_sexe["categorie_age_ffa"] == categorie_selection]
    else:
        df_filtre = df_filtre_sexe

    return df_filtre

# ----------------------------------------------------------------------------
# BLOC D'AFFICHAGE DU GRAPHIQUE
# ----------------------------------------------------------------------------

def bloc_graphique(df_selection, df_complet):

    # st.header("Graphique : vitesse moyenne et position à l’arrivée")
    st.markdown("## Étape 4. Visualise les résultats")
    
    if df_complet is None or df_complet.empty:
        st.warning("Pas de données à afficher.")
        return

    fig, (axe1, axe2) = plt.subplots(ncols=1, nrows=2, figsize=(7, 6.85))

    # Titre global
    nom_du_trail = df_selection.nom_du_trail.unique()[0]
    distance_du_trail = df_selection.distance_du_trail_en_kms.unique()[0]
    date_du_trail = df_selection.date_du_trail.unique()[0]

    # Gestion du sexe pour le titre
    sexes = df_selection.femme_ou_homme.unique()
    if len(sexes) == 2:
        sexe_label = "H & F"
    elif len(sexes) == 1:
        sexe_label = "Hommes" if sexes[0] == "H" else "Femmes"
    else:
        sexe_label = "Inconnu"

    # Gestion de la catégorie d'âge pour le titre
    categories = df_selection.categorie_age_ffa.unique()
    if len(categories) == 1:
        categorie_label = f"catégorie {categories[0]}"
    else:
        categorie_label = "toutes catégories d’âge"

    # Construction du titre final
    titre = (
        f"Visualisation de la course\n"
        f"{nom_du_trail} du {date_du_trail} \n"
        f"{categorie_label} - {sexe_label}"
    )
    fig.suptitle(titre, fontsize=12)


    # Calcul des déciles
    nb_total = len(df_complet)
    deciles = np.linspace(0, nb_total, 11).astype(int)
    y_max = df_complet["vitesse_moyenne"].max()
    y_text = y_max + 2

    # Lignes de décile
    for i, x in enumerate(deciles):
        axe1.axvline(
            x=x,
            color="sienna",
            linestyle='--',
            linewidth=0.5,
            alpha=0.7
        )
        axe1.text(
            x,
            y_text,
            f"{i * 10}%",
            ha='center',
            va='bottom',
            fontsize=10,
            bbox=dict(facecolor='white', edgecolor='sienna', boxstyle='round,pad=0.3')
        )

    # Tous les participants : fond gris
    sns.scatterplot(
        data=df_complet,
        x="classement_general",
        y="vitesse_moyenne",
        color="lightgray",
        alpha=0.5,
        s=15,
        ax=axe1
    )

    # Sélection : mise en valeur colorée
    if df_selection is not None and not df_selection.empty:
        palette = {
            "H": "#00BFA5",
            "F": "#6200EA"
        }
        sns.scatterplot(
            data=df_selection,
            x="classement_general",
            y="vitesse_moyenne",
            hue="femme_ou_homme",
            palette=palette,
            alpha=0.9,
            s=30,
            ax=axe1
        )

    axe1.set_title("Vitesse moyenne et classement à l’arrivée", fontsize=9, fontweight="bold")
    axe1.set_xlabel("Classement général", fontsize=9)
    axe1.set_ylabel("Vitesse (km/h)", fontsize=9)
    axe1.set_ylim(bottom=0, top=y_max + 4)
    axe1.set_xlim(right=df_complet["classement_general"].max() * 1.05)
    axe1.grid(True, linestyle='--', alpha=0.3)
    axe1.legend(title='Sexe', title_fontsize=7, loc='upper right')

    # Zone texte
    axe2.axis('off')
    nb_total_select = len(df_selection)
    nb_h_select = df_selection.query('femme_ou_homme == "H"').shape[0]
    nb_f_select = df_selection.query('femme_ou_homme == "F"').shape[0]
    pct_h_select = nb_h_select / nb_total_select * 100
    pct_f_select = nb_f_select / nb_total_select * 100
    v_max_select = df_selection.vitesse_moyenne.max()
    v_min_select = df_selection.vitesse_moyenne.min()
    
    axe2.text(0, 0.9, f"Chiffres pour {categorie_label} - {sexe_label} ", fontweight="bold")
    axe2.text(0, 0.8, f"- Nombre de personnes : {nb_total_select}")
    axe2.text(0, 0.7, f"- Vitesse moyenne de la 1ère position : {v_max_select:.2f} km/h")
    axe2.text(0, 0.6, f"- Vitesse moyenne de la dernière position : {v_min_select:.2f} km/h")
    axe2.text(0, 0.5, f"- Répartition H/F : Hommes {pct_h_select:.0f}% / Femmes {pct_f_select:.0f}%")
    axe2.text(0, 0.2, "Nota : Les lignes verticales indiquent les tranches de 10% à l’arrivée.")

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)

    st.pyplot(fig)
    # stockage de l'image en mémoire
    # buf = io.BytesIO() # création d'un buffer en mémoire
    # fig.savefig(buf, format="png") # sauvegarde de l'image en mémoire au format png
    # buf.seek(0) # on place le curseur au début du buffer pour que streamlit début au début du buffer

    # Affichage de l'image à partir du buffer, pour qu'elle soit zoomable
    # st.image(buf, caption="Graphique zoomable", use_column_width=True)
    # st.pyplot(fig) 
    # on utilise pas pyplot() car cela empêche parfois de zoomer l'image

    # Ajout d'un bouton pour télécharger l'image
    #st.download_button(
    #    label="Télécharge de graphe au format PNG",
    #    data=buf,
    #    file_name="ton-petit-graph-de-trail.png",
    #    mime="image/png"
    #)

# ----------------------------------------------------------------------------
# BLOC DES EXPLICATIONS
# ----------------------------------------------------------------------------

def bloc_explicatif_format():
    st.markdown("<a id='explications'></a>",  unsafe_allow_html=True)
    st.markdown("## 📘 Explications")
    st.markdown("""
    - [Format de fichier](#format-fichier)
    - [Ce que fait cette application](#ce-que-fait)
    - [Sous le capot, le code](#sous-le-capot)
    - [Pourquoi cette application](#pourquoi)
    - [Une question ? Besoin d'aide ?](#contact)
    """)

def affiche_le_bloc_explication_format_de_fichier():
    st.markdown("<a id='format-fichier'></a>",  unsafe_allow_html=True)
    st.markdown("""
    ### Format de fichier    
    Le fichier doit être un fichier CSV   .
    (*[Comment générer un fichier CSV](https://fr.wikihow.com/cr%C3%A9er-un-fichier-CSV)*).    
    Le fichier CSV doit contenir 7 colonnes.    

    **NOM DES COLONNES**    
    Les noms et l'ordre de ces 7 colonnes doivent être exactement les suivants:    
    - nom_du_trail
    - date_du_trail
    - distance_du_trail_en_kms
    - vitesse_moyenne
    - classement_general
    - femme_ou_homme
    - categorie_age_ffa        

    **CONTENU DES COLONNES**    
    - Dans chaque `colonne nom_du_trail`, `date_du_trail`, `distance_du_trail_en_kms`, 
    il faut répéter sur chaque ligne la même chose.    
    - Dans la colonne `femme_ou_homme`, on doit trouver uniquement les lettres H ou F.  
    - Dans la colonne `categorie_age_ffa`, on doit trouver uniquement les codes 
    des catégories officielles de la FFA ().  
    - Dans la colonne `vitesse_moyenne`, les chiffres avec décimales 
    doivent être écrits avec des points et PAS avec des virgules. Exemple: 10.5
    - La colonne `classement_general` doit être remplie de nombre entiers sans doublon

    **EXEMPLE**    
    Fichier exemple:    
    ```
    nom_du_trail,date_du_trail,distance_du_trail_en_kms,num_dossard,vitesse_moyenne,classement_general,femme_ou_homme,categorie_age_ffa
    Trail de Cheverny 35k,06/04/2025,34.7,7442,14.5,1,H,SE
    Trail de Cheverny 35k,06/04/2025,34.7,7329,13.5,2,H,M1
    Trail de Cheverny 35k,06/04/2025,34.7,7073,13.4,3,H,SE
    Trail de Cheverny 35k,06/04/2025,34.7,7403,13.3,4,H,M0
    Trail de Cheverny 35k,06/04/2025,34.7,7032,13.3,5,H,SE
    ```
    Visualisation du fichier exemple:     
    """)
    extrait_demo = charge_le_fichier_de_demo().head(5)
    st.dataframe(extrait_demo, use_container_width=True)

def affiche_explications_ce_que_fait():
    st.markdown("<a id='ce-que-fait'></a>",  unsafe_allow_html=True)
    st.markdown("""
    ### Ce que fait cette application
    Avec cette application tu peux afficher un graphique montrant 
    la vitesse et la position des personnes ayant participé à un trail 
    en choisissant les catégories femmes / homme / âge.

    Cela permet de se situer par catégorie.
    """)

def affiche_explications_sous_le_capot():
    st.markdown("<a id='sous-le-capot'></a>",  unsafe_allow_html=True)
    st.markdown("""
    ### Sous le capot, le code
    Cette application est écrit en `python`.    
    Elle utilise les librairies `python` suivantes:
    - `pandas` pour la préparation et les analyses data-science des données;
    - `matplotlib, seaborn` pour le graphique
    - `streamlit` pour le rendu sous forme d'application

    Pour plus d'informations sur le code, [me contacter SVP](#contact).
    """)

def affiche_explications_pourquoi():
    st.markdown("<a id='pourquoi'></a>",  unsafe_allow_html=True)
    st.markdown("""
    ### Pourquoi cette application ?
    Après mes trails, ou avant un trail, j'aime bien regarder où se situent 
    les personnes en fonction de leur catégorie.    
    J'ai d'abord conçu un code assez simple en python me donnant le graphique 
    que j'aimerais avoir.   
    En peaufinant, et parce que je voulais essayer `streamlit`, je me suis dit 
    que c'était l'occasion d'en faire une petite application qui puisse me servir 
    et qui puisse servir à toute autre personne.   

    Cette application est destinée aux traileuses et aux traileurs, quel que soit 
    le niveau.    

    Si vous êtes "orga" d'un trail, et que vous voudriez proposer cette application 
    aux personnes inscrites sur vos parcours, [contactez mois SVP](#contact), que 
    l'on étudie le truc ensemble (idem si vous êtes de la FFA). Ce serait chouette. 
    Merci d'avance.
    """)

def affiche_bloc_explications():
    bloc_explicatif_format()
    affiche_le_bloc_explication_format_de_fichier()
    affiche_explications_ce_que_fait()
    affiche_explications_sous_le_capot()
    affiche_explications_pourquoi()

# ----------------------------------------------------------------------------
# BLOC D'AFFICHAGE DES CONTACTS
# ----------------------------------------------------------------------------
    
def bloc_contact():
    st.markdown("<a id='contact'></a>",  unsafe_allow_html=True)
    lien_linkedin = (
        f"via [mon profil Linkedin]"
        f"(https://www.linkedin.com/in/data-analyst-antoine-chevrier-trails-runner)"
    )
    st.markdown(f"""
    ##  📬 Contact
    
    Pour toute question ou suggestion, **me contacter de préférence {lien_linkedin}**    

    Si vous n'avez pas LinkedIn, 
    ou si vous ne souhaitez pas utiliser LinkedIn 
    vous pouvez essayer de m'adresser un email sur mon adresse gmail.   
    Pour éviter de me faire pourir par des spams et les robots, 
    il vous faut reconstituer mon adresse en attachant 
    les parties ci-dessous (désolé pour le côté pas pratique de la chose):    
    - `contact` 
    - `.a` 
    - `.chevrier`
    - `@gmail.com`

    ## Merci à vous les amies traileuses et les amis traileurs !
    """)
    

# ============================================================================
# 🖼️ FONCTION QUI STRUCTURE DE LA PAGE PRINCIPALE EN APPELANT LES BLOCS
# ============================================================================

def affiche_l_application():
    affiche_la_section_entete()

    fichier, use_demo = bloc_selection_donnees()
    df = charger_donnees(fichier, use_demo)

    if df is not None:
        df_filtré = bloc_filtres_selection(df)
        bloc_graphique(df_filtré, df)
        df.pipe(afficher_dataframe)
    else:
        df_filtré = None

    affiche_bloc_explications()
    bloc_contact()

# ============================================================================
# 🚀 LANCEMENT DE L'APPLICATION
# ============================================================================

# affiche_l_application()
affiche_l_application()
