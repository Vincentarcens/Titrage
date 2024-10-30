import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Configurer le nom et l'icône de la page
st.set_page_config(page_title="Simulation d'un titrage", page_icon="⚗️")

# Titre principal
st.markdown("<h1 style='font-size: 36px;'>Simulation d'un titrage</h1>", unsafe_allow_html=True)

# Demande des noms des réactifs et produits avec instructions pour LaTeX
st.markdown(
    "Entrez les noms des réactifs et produits en utilisant `^` pour les exposants et `_` pour les indices. "
    "Par exemple, entrez `H_2O` pour H₂O ou `Mg^{2+}` pour Mg²⁺."
)

# Demande des noms des réactifs et produits
titrant = st.text_input("Nom du réactif titrant", "H^+")
titre = st.text_input("Nom du réactif titré", "OH^-")
produit1 = st.text_input("Nom du premier produit formé", "H_2O")
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
bars = ax.bar(labels, quantities, color=colors)
y_max = max(quantite_initiale_titre, quantite_produit1[-1], quantite_produit2[-1], quantite_titrant[-1]) * 1.1
ax.set_ylim(0, y_max)

# Génération de l'équation de réaction avec suppression des coefficients de 1 et en LaTeX
equation_text = (
    f"{'' if coeff_titrant == 1 else int(coeff_titrant)}{titrant} + "
    f"{'' if coeff_titre == 1 else int(coeff_titre)}{titre} \\rightarrow "
    f"{'' if coeff_produit1 == 1 else int(coeff_produit1)}{produit1}"
)
if produit2:
    equation_text += f" + {'' if coeff_produit2 == 1 else int(coeff_produit2)}{produit2}"

# Appliquer LaTeX dans l'équation
ax.set_title(rf"${equation_text}$", pad=20)

# Ajouter les noms des réactifs et produits sous les barres en utilisant LaTeX
for i, (label, bar) in enumerate(zip(labels, bars)):
    # Utiliser LaTeX pour les labels et les placer sous les barres
    ax.text(bar.get_x() + bar.get_width() / 2, -y_max * 0.05, f"${label}$", ha='center', va='top', fontsize=12)

# Afficher les quantités juste au-dessus des barres
for bar, quantity in zip(bars, quantities):
    ax.text(bar.get_x() + bar.get_width() / 2, quantity + 0.02 * y_max, f'{quantity:.2f}', ha='center')

# Afficher le graphique dans Streamlit
st.pyplot(fig)
