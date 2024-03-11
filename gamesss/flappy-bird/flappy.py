# Importation des bibliothèques
import pygame
import sys
import time
import random
import os

# Importation de Pygame Mixer
import pygame.mixer

# Initialisation de Pygame
pygame.init()
pygame.mixer.init()

# Obtenir le chemin de base du script
base_path = os.path.dirname(os.path.abspath(__file__))

# Charger les sons
die_sound = pygame.mixer.Sound(os.path.join(base_path, 'audio', 'die.wav'))
hit_sound = pygame.mixer.Sound(os.path.join(base_path, 'audio', 'hit.wav'))
point_sound = pygame.mixer.Sound(os.path.join(base_path, 'audio', 'point.wav'))
swoosh_sound = pygame.mixer.Sound(os.path.join(base_path, 'audio', 'swoosh.wav'))
wing_sound = pygame.mixer.Sound(os.path.join(base_path, 'audio', 'wing.wav'))

# Charger la musique de fond
pygame.mixer.music.load(os.path.join(base_path, 'audio', 'flappybg.mp3'))

# Fenêtre du jeu
largeur, hauteur = 350, 622
horloge = pygame.time.Clock()
ecran = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Flappy Bird")

# Configuration de l'image de fond et de la base
img_fond = pygame.image.load(os.path.join(base_path, 'assest', 'img_46.png'))
img_base = pygame.image.load(os.path.join(base_path, 'assest', 'img_50.png'))
x_base = 0

# Différentes étapes de l'oiseau
oiseau_haut = pygame.image.load(os.path.join(base_path, 'assest', 'img_47.png'))
oiseau_bas = pygame.image.load(os.path.join(base_path, 'assest', 'img_48.png'))
oiseau_milieu = pygame.image.load(os.path.join(base_path, 'assest', 'img_49.png'))
oiseaux = [oiseau_haut, oiseau_milieu, oiseau_bas]
index_oiseau = 0
evenement_battement = pygame.USEREVENT
pygame.time.set_timer(evenement_battement, 200)
img_oiseau = oiseaux[index_oiseau]
rect_oiseau = img_oiseau.get_rect(center=(67, 622 // 2))
mouvement_oiseau = 0
gravite = 0.17

# Charger l'image du tuyau
img_tuyau = pygame.image.load(os.path.join(base_path, 'assest', 'greenpipe.png'))
hauteur_tuyau = [400, 350, 533, 490]

# Pour que les tuyaux apparaissent
tuyaux = []
creer_tuyau = pygame.USEREVENT + 1
pygame.time.set_timer(creer_tuyau, 1200)

# Affichage de l'image de fin de jeu
game_over = False
img_game_over = pygame.image.load(os.path.join(base_path, 'assest', 'img_45.png')).convert_alpha()
rect_game_over = img_game_over.get_rect(center=(largeur // 2, hauteur // 2))

# Configuration des variables et de la police pour le score
score = 0
chemin_fichier_score = os.path.join(base_path, 'highest_score.txt')
meilleur_score = 0

temps_score = True
police_score = pygame.font.Font(os.path.join(base_path, 'assest', 'font.ttf'), 20)

# Configuration du bouton de sortie
rect_bouton_sortie = pygame.Rect(250, 10, 80, 40)  # Ajustez la position et la taille au besoin

# Commencer à jouer la musique de fond
pygame.mixer.music.play(-1)


# Fonction pour dessiner le sol
def dessiner_sol():
    ecran.blit(img_base, (x_base, 520))
    ecran.blit(img_base, (x_base + 448, 520))

# Fonction pour créer des tuyaux
def creer_tuyaux():
    y_tuyau = random.choice(hauteur_tuyau)
    tuyau_haut = img_tuyau.get_rect(midbottom=(467, y_tuyau - 200))
    tuyau_bas = img_tuyau.get_rect(midtop=(467, y_tuyau))
    return tuyau_haut, tuyau_bas

# Fonction pour l'animation des tuyaux
def animation_tuyaux():
    global game_over, temps_score
    for tuyau in tuyaux:
        if tuyau.top < 0:
            tuyau_inverse = pygame.transform.flip(img_tuyau, False, True)
            ecran.blit(tuyau_inverse, tuyau)
        else:
            ecran.blit(img_tuyau, tuyau)

        tuyau.centerx -= 3
        if tuyau.right < 0:
            tuyaux.remove(tuyau)

        if rect_oiseau.colliderect(tuyau):
            hit_sound.play()  # Jouer le son de collision
            game_over = True

# Fonction pour dessiner le score
def dessiner_score(etat_jeu):
    if etat_jeu == "game_on":
        texte_score = police_score.render(str(score), True, (255, 255, 255))
        rect_score = texte_score.get_rect(center=(largeur // 2, 66))
        ecran.blit(texte_score, rect_score)
    elif etat_jeu == "game_over":
        texte_score = police_score.render(f" Score: {score}", True, (255, 255, 255))
        rect_score = texte_score.get_rect(center=(largeur // 2, 66))
        ecran.blit(texte_score, rect_score)

        texte_meilleur_score = police_score.render(f"Best Score : {meilleur_score}", True, (255, 255, 255))
        rect_meilleur_score = texte_meilleur_score.get_rect(center=(largeur // 2, 506))
        ecran.blit(texte_meilleur_score, rect_meilleur_score)

# Charger le meilleur score
def charger_meilleur_score():
    global meilleur_score
    if os.path.exists(chemin_fichier_score):
        with open(chemin_fichier_score, 'r') as fichier:
            meilleur_score = int(fichier.read())

def sauvegarder_meilleur_score():
    with open(chemin_fichier_score, 'w') as fichier:
        fichier.write(str(meilleur_score))


charger_meilleur_score()

# Fonction pour mettre à jour le score
def mise_a_jour_score():
    global score, temps_score, meilleur_score
    if tuyaux:
        for tuyau in tuyaux:
            if 65 < tuyau.centerx < 69 and temps_score:
                score += 1
                temps_score = False
                point_sound.play()  # Jouer le son de pointage
            if tuyau.left <= 0:
                temps_score = True

    if score > meilleur_score:
        meilleur_score = score
        sauvegarder_meilleur_score()

# Fonction pour dessiner le bouton de sortie
def dessiner_bouton_sortie():
    surface_bouton_sortie = pygame.Surface((80, 40), pygame.SRCALPHA)
    pygame.draw.rect(surface_bouton_sortie, (0, 0, 0), (0, 0, 80, 40), border_radius=5)
    texte_sortie = police_score.render("Exit", True, (255, 255, 255))
    surface_bouton_sortie.blit(texte_sortie, ((80 - texte_sortie.get_width()) // 2, (40 - texte_sortie.get_height()) // 2))
    ecran.blit(surface_bouton_sortie, rect_bouton_sortie.topleft)


# Boucle de jeu
en_cours = True
while en_cours:
    horloge.tick(90)

    # Vérification des événements
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:  # Événement QUIT
            en_cours = False
            pygame.quit()
            sys.exit()

        if evenement.type == pygame.KEYDOWN:  # Événement de touche enfoncée
            if evenement.key == pygame.K_SPACE and not game_over:  # Si la touche Espace est pressée
                mouvement_oiseau = 0
                mouvement_oiseau = -5
                wing_sound.play()  # Jouer le son d'aile lorsque l'oiseau bat des ailes

            if evenement.key == pygame.K_SPACE and game_over:
                game_over = False
                tuyaux = []
                rect_oiseau = img_oiseau.get_rect(center=(67, 622 // 2))
                mouvement_oiseau = 0
                temps_score = True
                score = 0

        # Pour charger différentes étapes
        if evenement.type == evenement_battement:
            index_oiseau += 1

            if index_oiseau > 2:
                index_oiseau = 0

            img_oiseau = oiseaux[index_oiseau]
            rect_oiseau = oiseau_haut.get_rect(center=rect_oiseau.center)

        # Pour ajouter des tuyaux dans la liste
        if evenement.type == creer_tuyau:
            tuyaux.extend(creer_tuyaux())

        # Vérifier si le bouton de sortie est cliqué
        if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
            if rect_bouton_sortie.collidepoint(evenement.pos):
                en_cours = False 
                pygame.quit()
                sys.exit()

    ecran.blit(img_base, (x_base, 550))
    ecran.blit(img_fond, (0, 0))


        # Conditions de fin de jeu
    if not game_over:
        mouvement_oiseau += gravite
        rect_oiseau.centery += mouvement_oiseau
        oiseau_rotatif = pygame.transform.rotozoom(img_oiseau, mouvement_oiseau * -6, 1)

        if rect_oiseau.top < 5 or rect_oiseau.bottom >= 550:
            hit_sound.play()  # Jouer le son de collision
            game_over = True

        ecran.blit(oiseau_rotatif, rect_oiseau)
        animation_tuyaux()
        mise_a_jour_score()
        dessiner_score("game_on")
    elif game_over:
        ecran.blit(img_game_over, rect_game_over)
        dessiner_score("game_over")
        
        # Dessiner le bouton de sortie après la fin du jeu
        dessiner_bouton_sortie()

    # Pour déplacer la base
    x_base -= 1
    if x_base < -448:
        x_base = 0

    dessiner_sol()

    # Mettre à jour la fenêtre du jeu
    pygame.display.update()

# Arrêter la musique de fond et quitter Pygame
sauvegarder_meilleur_score()
pygame.mixer.music.stop()
pygame.quit()
sys.exit()
