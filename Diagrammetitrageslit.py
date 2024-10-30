import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Configurer le nom et l'icône de la page
st.set_page_config(page_title="Simulation de titrage chimique", page_icon="⚗️")

# Titre principal
st.markdown("<h1 style='font-size: 36px; color: #333333;'>Simulation de titrage chimique</h1>", unsafe_allow_html=True)

# Demande des noms des réactifs et produits
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
quantite_initiale_titrant = 0.0  # Titrant commence à 0

# Calcul de l'avancement à l'équivalence
avancement_equivalence = quantite_initiale_titre / coeff_titre

# Définir le pas d'avancement
goutte = avancement_equivalence / 25
n_points = 150
avancement = np.linspace(0, avancement_equivalence * 2, n_points)

# Calcul des quantités en fonction de l'avancement
quantite_titre = np.maximum(quantite_initiale_titre - coeff_titre * avancement, 0)
quantite_titrant = np.where(avancement <= avancement_equivalence, 0, coeff_titrant * (avancement - avancement_equivalence))
quantite_produit1 = np.minimum(coeff_produit1 * avancement, coeff_produit1 * avancement_equivalence)
quantite_produit2 = np.minimum(coeff_produit2 * avancement, coeff_produit2 * avancement_equivalence) if produit2 else np.zeros_like(avancement)

# Slider pour l'avancement
avancement_slider = st.slider("Avancement de la réaction", 0.0, avancement_equivalence * 2, value=st.session_state.get("avancement", 0.0), step=goutte)
st.session_state["avancement"] = avancement_slider

# Bouton pour ajouter une goutte
if st.button("Ajouter une goutte"):
    st.session_state["avancement"] = min(st.session_state["avancement"] + goutte, avancement_equivalence * 2)

# Bouton pour remise à zéro
if st.button("Remise à zéro"):
    st.session_state["avancement"] = 0.0

# Valeur de l'avancement actuel
avancement_val = st.session_state["avancement"]
frame = int((avancement_val / (avancement_equivalence * 2)) * (n_points - 1))

# Calcul des quantités actuelles
quantite_A = quantite_titrant[frame]
quantite_B = quantite_titre[frame]
quantite_C = quantite_produit1[frame]
quantite_D = quantite_produit2[frame] if produit2 else 0

# Préparation des données du graphique avec vérification de produit2
labels = [titrant, titre, produit1]
quantities = [quantite_A, quantite_B, quantite_C]
colors = ['blue', 'orange', 'green']

# Ajouter produit2 si défini
if produit2:
    labels.append(produit2)
    quantities.append(quantite_D)
    colors.append('red')

# Préparation du graphique
fig, ax = plt.subplots()
ax.bar(labels, quantities, color=colors)
y_max = max(quantite_initiale_titre, quantite_produit1[-1], quantite_produit2[-1], quantite_titrant[-1]) * 1.1
ax.set_ylim(0, y_max)
equation_text = f"{int(coeff_titrant)}{titrant} + {int(coeff_titre)}{titre} → {int(coeff_produit1)}{produit1}"
if produit2:
    equation_text += f" + {int(coeff_produit2)}{produit2}"
ax.set_title(equation_text)

# Afficher les quantités au-dessus des barres
for i, (height, label) in enumerate(zip(quantities, labels)):
    ax.text(i, height + 0.1, f'{height:.2f}', ha='center')

# Afficher le graphique dans Streamlit
st.pyplot(fig)
