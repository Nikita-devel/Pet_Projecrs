import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import pandas as pd
from tkinter import ttk

def analyse_donnees_gps(chemin_fichier, vitesse_moyenne):
    try:
        # Lecture du fichier CSV
        df = pd.read_csv(chemin_fichier, delimiter=';')

        # Calcul de la distance totale parcourue
        distance_totale = df['Distance (m)'].sum()

        # Calcul du dénivelé positif et négatif
        denivele_positif = max(0, df['Altitude (m)'].diff().clip(lower=0).sum())
        denivele_negatif = max(0, -df['Altitude (m)'].diff().clip(upper=0).sum())

        # Trouver l'altitude maximale
        altitude_maximale = df['Altitude (m)'].max()

        # Calcul du temps de parcours en fonction de la vitesse moyenne
        temps_de_parcours = round(distance_totale / vitesse_moyenne, 2)

        # Calcul de la dépense calorique approximative
        df['Calories Brûlées'] = df['Distance (m)'] * 0.05  # Utilisez votre propre coefficient
        calories_brulees = round(df['Calories Brûlées'].sum(), 2)

        # Affichage des résultats
        texte_resultat = f"Distance totale parcourue : {distance_totale} m\n"
        texte_resultat += f"Dénivelé positif : {denivele_positif} m\n"
        texte_resultat += f"Dénivelé négatif : {denivele_negatif} m\n"
        texte_resultat += f"Altitude maximale : {altitude_maximale} m\n"
        texte_resultat += f"Temps de parcours à {vitesse_moyenne} m/s : {temps_de_parcours} s\n"
        texte_resultat += f"Dépense de calories : {calories_brulees} cal"

        # Effacement et affichage des résultats dans le champ de texte
        champ_texte.delete(1.0, tk.END)
        champ_texte.insert(tk.END, texte_resultat)

    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'analyse des données : {str(e)}")

# Fonction appelée lors du clic sur le bouton "Démarrer"
def demarrer_clic():
    chemin_fichier = filedialog.askopenfilename(title="Choisir un fichier CSV", filetypes=[("Fichiers CSV", "*.csv")])
    if chemin_fichier:
        # Sélection de la vitesse
        fenetre_vitesse = tk.Toplevel(root)
        fenetre_vitesse.title("Entrez la vitesse moyenne")

        etiquette_vitesse = tk.Label(fenetre_vitesse, text="Entrez la vitesse moyenne (m/s) :")
        etiquette_vitesse.pack(pady=10)

        entree_vitesse = ttk.Entry(fenetre_vitesse)
        entree_vitesse.pack(pady=10)

        def analyser_avec_vitesse():
            vitesse = float(entree_vitesse.get())
            analyse_donnees_gps(chemin_fichier, vitesse)
            fenetre_vitesse.destroy()

        bouton_vitesse = tk.Button(fenetre_vitesse, text="Analyser avec la vitesse donnée", command=analyser_avec_vitesse)
        bouton_vitesse.pack(pady=10)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Analyse des données GPS")

# Création du bouton "Démarrer"
bouton_demarrer = tk.Button(root, text="Démarrer", command=demarrer_clic)
bouton_demarrer.pack(pady=20)

# Création du champ de texte pour afficher les résultats
champ_texte = scrolledtext.ScrolledText(root, width=40, height=15)
champ_texte.pack(padx=20, pady=20)

# Création du bouton de sortie
bouton_sortie = tk.Button(root, text="Quitter", command=root.destroy)
bouton_sortie.pack(pady=20)

# Lancement de la boucle principale de l'interface graphique
root.mainloop()
