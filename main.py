# Importation des modules nécessaires
import sys
import pygame
from BibForMenu.button import Button
from BibForMenu.exp import flappy_bird, game_connect4, gps_tool, pong_game, snake_game
import subprocess
import os

# Initialisation de Pygame
pygame.init()

# Initialisation du module de son de Pygame
pygame.mixer.init()

# Chargement et lecture de la musique d'arrière-plan
background_music = pygame.mixer.Sound('assets/audio/mainbgs.mp3')
background_music.set_volume(0.5)
background_music.play(-1)

# Chargement du son de clic
click_sound = pygame.mixer.Sound('assets/audio/click_sound.mp3')
click_sound.set_volume(2)

# Récupération du chemin du dossier courant du script
base_path = os.path.dirname(os.path.abspath(__file__))

# Configuration de l'écran en mode plein écran
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Menu")

# Récupération des dimensions de l'écran
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

# Chargement et redimensionnement de l'image de fond
BG = pygame.image.load(os.path.join(base_path, "assets", "Background.png"))
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Fonction pour obtenir une police de caractères avec une taille spécifiée
def get_font(size): 
    return pygame.font.Font(os.path.join(base_path, "assets", "font.ttf"), size)

# Création d'un bouton de retour en arrière (back)
PLAY_BACK = Button( image=None, 
                    pos=(SCREEN_WIDTH - 125, SCREEN_HEIGHT - 50), 
                    text_input="BACK", 
                    font=get_font(50), base_color="White", hovering_color="Green")

# Fonction qui affiche la liste des jeux disponibles
def games():
    # Liste des jeux avec leurs noms et actions associées
    gamex = [
        {"text": "Puissance 4", "action": lambda: subprocess.Popen(["python", os.path.join(base_path, "gamesss", "connect4", "connect4.py")])},
        {"text": "Flappy Bird", "action": lambda: subprocess.Popen(["python", os.path.join(base_path, "gamesss", "flappy-bird", "flappy.py")])},
        {"text": "GPS analyse", "action": lambda: subprocess.Popen(["python", os.path.join(base_path, "gamesss", "gps", "gps_csv.py")])},
        {"text": "Beta Minecraft", "action": lambda: subprocess.Popen(["python", os.path.join(base_path, "gamesss", "minecraft", "minecraft.py")])},
        {"text": "Pong Game", "action": lambda: subprocess.Popen(["python", os.path.join(base_path, "gamesss", "pong", "pong_game.py")])},
        {"text": "Snake", "action": lambda: subprocess.Popen(["python", os.path.join(base_path, "gamesss", "snake", "snake_game.py")])},
        {"text": "Space Shooter", "action": lambda: subprocess.Popen(["python", os.path.join(base_path, "gamesss", "SpaceShooter", "main.py")])},
        {"text": "AeroBlaster", "action": lambda: subprocess.Popen(["python", os.path.join(base_path, "gamesss", "AeroblasterSource", "Aeroblaster.py")])},
    ]

    # Espacement des boutons
    button_spacing = 20

    while True:
        # Récupération de la position de la souris
        GAME_MOUSE_POS = pygame.mouse.get_pos()

        # Affichage de l'image de fond
        SCREEN.blit(BG, (0, 0))

        # Affichage du texte d'information
        GAME_TEXT = get_font(42).render("It is ecran of games.", True, "White")
        GAME_RECT = GAME_TEXT.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8))
        SCREEN.blit(GAME_TEXT, GAME_RECT)

        # Séparation des jeux en deux colonnes
        column1_buttons = gamex[:5]
        column2_buttons = gamex[5:]

        # Position des boutons dans les colonnes
        button_spacing = 20
        column1_x = SCREEN_WIDTH // 3
        column2_x = SCREEN_WIDTH -  SCREEN_WIDTH // 3

        # Affichage des boutons de la première colonne
        for i, button_info in enumerate(column1_buttons):
            button = Button(image=None, pos=(column1_x, SCREEN_HEIGHT // 4 + i * (60 + button_spacing)),
                            text_input=button_info['text'],
                            font=get_font(30),
                            base_color="Yellow",
                            hovering_color="Green")

            button.changeColor(GAME_MOUSE_POS)
            button.update(SCREEN)

            if button.checkForInput(GAME_MOUSE_POS):
                if pygame.mouse.get_pressed()[0]:
                    if button_info["text"] != "GAMES":
                        background_music.set_volume(0)
                    click_sound.play()
                    subprocess_game = button_info["action"]()
                    subprocess_game.wait()
                    background_music.set_volume(0.5)

        # Affichage des boutons de la deuxième colonne
        for i, button_info in enumerate(column2_buttons):
            button = Button(image=None, pos=(column2_x, SCREEN_HEIGHT // 4 + i * (60 + button_spacing)),
                            text_input=button_info['text'],
                            font=get_font(30),
                            base_color="Yellow",
                            hovering_color="Green")

            button.changeColor(GAME_MOUSE_POS)
            button.update(SCREEN)

            if button.checkForInput(GAME_MOUSE_POS):
                if pygame.mouse.get_pressed()[0]:
                    if button_info["text"] != "GAMES":
                        background_music.set_volume(0)
                    click_sound.play()
                    subprocess_game = button_info["action"]()
                    subprocess_game.wait()
                    background_music.set_volume(0.5)

        # Mise à jour et affichage du bouton de retour en arrière (back)
        PLAY_BACK.changeColor(GAME_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        # Gestion des événements Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(GAME_MOUSE_POS):
                    if pygame.mouse.get_pressed()[0]:
                        click_sound.play()  
                        return

        # Mise à jour de l'écran
        pygame.display.update()

# Fonction qui affiche le guide pour un jeu spécifique
def guide(game_name):
    # Liste des boutons de guide avec leurs noms et actions associées
    guide_buttons = [
        {"text": "Puissance 4", "action": lambda: show_explanation(game_connect4)},
        {"text": "Flappy Bird", "action": lambda: show_explanation(flappy_bird)},
        {"text": "GPS analyse", "action": lambda: show_explanation(gps_tool)},
        {"text": "Beta Minecraft", "action": lambda: show_explanation("Je pense que vous n'avez pas besoin de savoir comment jouer")},
        {"text": "Pong Game", "action": lambda: show_explanation(pong_game)},
        {"text": "Snake", "action": lambda: show_explanation(snake_game)},
        {"text": "Space Shooter", "action": lambda: show_explanation(snake_game)},
        {"text": "Aeroblaster", "action": lambda: show_explanation(snake_game)},
    ]

    while True:
        # Récupération de la position de la souris
        GUIDE_MOUSE_POS = pygame.mouse.get_pos()

        # Affichage de l'image de fond
        SCREEN.blit(BG, (0, 0))

        # Affichage du texte d'information
        GUIDE_TEXT = get_font(45).render(f"Ceci est l'écran GUIDE de {game_name}.", True, "White")
        GUIDE_RECT = GUIDE_TEXT.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8))
        SCREEN.blit(GUIDE_TEXT, GUIDE_RECT)

        # Affichage des boutons de guide
        for i, button_info in enumerate(guide_buttons):
            button = Button(image=None, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + i * 60),
                            text_input=button_info['text'],
                            font=get_font(30),
                            base_color="Yellow",
                            hovering_color="Green")

            button.changeColor(GUIDE_MOUSE_POS)
            button.update(SCREEN)

            if button.checkForInput(GUIDE_MOUSE_POS):
                if pygame.mouse.get_pressed()[0]:
                    click_sound.play()
                    button_info["action"]()

        # Mise à jour et affichage du bouton de retour en arrière (back)
        PLAY_BACK.changeColor(GUIDE_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        # Gestion des événements Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(GUIDE_MOUSE_POS):
                    if pygame.mouse.get_pressed()[0]:
                        click_sound.play()
                        return

        # Mise à jour de l'écran
        pygame.display.update()

# Fonction qui affiche une explication spécifique
        
def show_explanation(explanation_text):
    # Découpe le texte d'explication en lignes
    explanation_lines = explanation_text.strip().split('\n')

    # Configuration de la police et de la fenêtre d'explication
    explanation_font = get_font(10)
    explanation_window = pygame.Surface((SCREEN_WIDTH // 1.5, SCREEN_HEIGHT // 1.5))
    explanation_window.blit(BG, (0, 0))

    # Position de départ du texte
    y_position = 10  
    
    # Boucle pour afficher chaque ligne d'explication
    for line in explanation_lines:
        explanation_surface = explanation_font.render(line, True, "White")
        explanation_rect = explanation_surface.get_rect(topleft=(10, y_position))  # Alignement à gauche
        explanation_window.blit(explanation_surface, explanation_rect)
        y_position += explanation_rect.height + 5 

    # Position du bouton de retour en arrière (BACK)
    button_position = (int(SCREEN_WIDTH * 0.9), int(SCREEN_HEIGHT * 0.9))
    explanation_back_button = Button(image=None,
                                     pos=button_position,
                                     text_input="BACK",
                                     font=get_font(20),
                                     base_color="White",
                                     hovering_color="Green")

    while True:
        # Gestion des événements Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                button_clicked = explanation_back_button.checkForInput(pygame.mouse.get_pos())
                if button_clicked and pygame.mouse.get_pressed()[0]:
                    click_sound.play()
                    return

        # Affichage de la fenêtre d'explication et du bouton de retour en arrière (BACK)
        SCREEN.blit(explanation_window, (10, SCREEN_HEIGHT // 4))
        explanation_back_button.changeColor(pygame.mouse.get_pos())
        explanation_back_button.update(SCREEN)

        # Mise à jour de l'écran
        pygame.display.update()

def main_menu():
    # Liste des boutons du menu principal avec leurs noms et actions associées
    buttonss = [
        {"text": "GAMES", "action": games},
        {"text": "GUIDE", "action": lambda: guide("GAME")},
        {"text": "QUIT", "action": pygame.quit}
    ]

    while True:
        # Affichage de l'image de fond
        SCREEN.blit(BG, (0, 0))

        # Récupération de la position de la souris
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Affichage du texte du menu principal
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Affichage des boutons du menu principal
        for i, button_info in enumerate(buttonss):
            button = Button(image=pygame.image.load(os.path.join(base_path, "assets", f"{button_info['text']} Rect.png")),
                            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + i * 150),
                            text_input=button_info['text'],
                            font=get_font(75),
                            base_color="#d7fcd4",
                            hovering_color="Green")

            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

            # Gestion du clic sur le bouton
            if button.checkForInput(MENU_MOUSE_POS):
                if pygame.mouse.get_pressed()[0]:
                    click_sound.play() 
                    button_info["action"]()

        # Gestion des événements Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Mise à jour de l'écran
        pygame.display.update()

# Lancement du menu principal
main_menu()
