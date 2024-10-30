# Créé par vince, le 30/10/2024 en Python 3.7
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Initialisation des valeurs de session
if "avancement" not in st.session_state:
    st.session_state.avancement = 0.0

# Demande des noms des réactifs pour le titrage
st.title("Simulation de titrage chimique")
titrant = st.text_input("Nom du réactif titrant", "Titrant")
titre = st.text_input("Nom du réactif titré", "Titre")
produit1 = st.text_input("Nom du premier produit formé", "Produit 1")
produit2 = st.text_input("Nom du deuxième produit formé (laisser vide si aucun)", "")

# Demande des coefficients stoechiométriques
coeff_titrant = st.number_input(f"Coefficient stœchiométrique de {titrant}", value=1.0)
coeff_titre = st.number_input(f"Coefficient stœchiométrique de {titre}", value=1.0)
coeff_produit1 = st.number_input(f"Coefficient stœchiométrique de {produit1}", value=1.0)
coeff_produit2 = 0.0
if produit2:
    coeff_produit2 = st.number_input(f"Coefficient stœchiométrique de {produit2}", value=1.0)

# Quantité initiale du réactif titré fixée à 100
quantite_initiale_titre = 100.0

# Le réactif titrant démarre avec une quantité nulle et augmente à chaque goutte
quantite_initiale_titrant = 0.0  # Fixé à 0 avant le titrage

# Calcul de l'avancement à l'équivalence
avancement_equivalence = quantite_initiale_titre / coeff_titre

# Définir le pas d'avancement pour chaque goutte ajoutée
goutte = avancement_equivalence / 25  # Chaque goutte représente 4 % de l'équivalence

# Quantités en fonction de l'avancement, avec gestion avant et après équivalence
n_points = 150  # Nombre de points pour une bonne résolution
avancement = np.linspace(0, avancement_equivalence * 2, n_points)  # Permettre d'aller jusqu'à 200% de l'équivalence

quantite_titre = np.maximum(quantite_initiale_titre - coeff_titre * avancement, 0)  # Diminue jusqu'à 0
quantite_titrant = np.where(avancement <= avancement_equivalence, 0, coeff_titrant * (avancement - avancement_equivalence))  # Nulle avant équivalence, augmente après
quantite_produit1 = np.minimum(coeff_produit1 * avancement, coeff_produit1 * avancement_equivalence)  # Augmente jusqu'à l'équivalence, puis reste constant
quantite_produit2 = np.minimum(coeff_produit2 * avancement, coeff_produit2 * avancement_equivalence) if produit2 else np.zeros_like(avancement)

# Slider pour contrôler l'avancement manuel
avancement_slider = st.slider(
    "Avancement de la réaction",
    0.0,
    avancement_equivalence * 2,
    value=st.session_state.avancement,
    step=goutte
)

# Synchroniser le slider avec la session state
st.session_state.avancement = avancement_slider

# Bouton pour ajouter une goutte
if st.button("Ajouter une goutte"):
    st.session_state.avancement += goutte  # Incrémente de 4% de l'équivalence
    st.session_state.avancement = min(st.session_state.avancement, avancement_equivalence * 2)  # Limite au double de l'équivalence

# Bouton pour remettre à zéro
if st.button("Remise à zéro"):
    st.session_state.avancement = 0.0

# Utiliser la valeur de session pour l'avancement
avancement_val = st.session_state.avancement
frame = int((avancement_val / (avancement_equivalence * 2)) * (n_points - 1))

# Calcul des quantités pour chaque espèce chimique
quantite_A = quantite_titrant[frame]
quantite_B = quantite_titre[frame]
quantite_C = quantite_produit1[frame]
quantite_D = quantite_produit2[frame] if produit2 else 0

# Calcul du maximum pour l'axe des ordonnées
y_max = max(quantite_initiale_titre, quantite_produit1[-1], quantite_produit2[-1], quantite_titrant[-1]) * 1.1

# Préparation du graphique
fig, ax = plt.subplots()
ax.bar([titrant, titre, produit1] + ([produit2] if produit2 else []), [quantite_A, quantite_B, quantite_C, quantite_D],
       color=['blue', 'orange', 'green', 'red'][:len([quantite_A, quantite_B, quantite_C, quantite_D])])
ax.set_ylim(0, y_max)
equation_text = f"{int(coeff_titrant)}{titrant} + {int(coeff_titre)}{titre} → {int(coeff_produit1)}{produit1}"
if produit2:
    equation_text += f" + {int(coeff_produit2)}{produit2}"
ax.set_title(equation_text)

# Afficher les quantités au-dessus des barres
for i, (height, label) in enumerate(zip([quantite_A, quantite_B, quantite_C, quantite_D], [titrant, titre, produit1, produit2])):
    if label:  # Afficher seulement si le produit est défini
        ax.text(i, height + 0.1, f'{height:.4f}', ha='center')

# Afficher le graphique dans Streamlit
st.pyplot(fig)

