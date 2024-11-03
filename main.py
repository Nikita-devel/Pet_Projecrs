# Importation des modules nécessaires
import sys
import pygame
from BibForMenu.button import Button
from BibForMenu.exp import flappy_bird, game_connect4, gps_tool, pong_game, snake_game
import subprocess
import os
import logging

# Initialisation de Pygame
pygame.init()

# Initialisation du module de son de Pygame
pygame.mixer.init()

# Configuration du système de log
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Chargement et lecture de la musique d'arrière-plan
try:
    background_music = pygame.mixer.Sound("assets/audio/mainbgs.mp3")
    background_music.set_volume(0.4)
    background_music.play(-1)
except pygame.error as e:
    logging.error("Erreur lors du chargement de la musique d'arrière-plan: %s", e)

# Chargement du son de clic
try:
    click_sound = pygame.mixer.Sound("assets/audio/click_sound.mp3")
    click_sound.set_volume(2)
except pygame.error as e:
    logging.error("Erreur lors du chargement du son de clic: %s", e)

# Récupération du chemin du dossier courant du script
base_path = os.path.dirname(os.path.abspath(__file__))

# Configuration de l'écran en mode plein écran
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Menu")

# Récupération des dimensions de l'écran
SCREEN_WIDTH, SCREEN_HEIGHT = (
    pygame.display.Info().current_w,
    pygame.display.Info().current_h,
)

# Chargement et redimensionnement de l'image de fond
BG = pygame.image.load(os.path.join(base_path, "assets", "Background.png"))
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))


# Fonction pour obtenir une police de caractères avec une taille spécifiée
def get_font(size):
    return pygame.font.Font(os.path.join(base_path, "assets", "font.ttf"), size)


# Création d'un bouton de retour en arrière (back)
PLAY_BACK = Button(
    image=None,
    pos=(SCREEN_WIDTH - 125, SCREEN_HEIGHT - 50),
    text_input="BACK",
    font=get_font(50),
    base_color="White",
    hovering_color="Green",
)

# Fonction qui affiche la liste des jeux disponibles
current_page = 0
games_per_page = 5  # Кількість ігор на одній сторінці


# Оновимо функцію games() з обробкою помилок і новими стрілками
def progrmas():
    gamex = [
        {
            "text": "Puissance 4",
            "action": lambda: launch_game("gamesss/connect4/connect4.py"),
        },
        {
            "text": "Flappy Bird",
            "action": lambda: launch_game("gamesss/flappy-bird/flappy.py"),
        },
        {
            "text": "GPS analyse",
            "action": lambda: launch_game("gamesss/gps/gps_csv.py"),
        },
        {
            "text": "Beta Minecraft",
            "action": lambda: launch_game("gamesss/minecraft/minecraft.py"),
        },
        {
            "text": "Pong Game",
            "action": lambda: launch_game("gamesss/pong/pong_game.py"),
        },
        {
            "text": "Snake",
            "action": lambda: launch_game("gamesss/snake/snake_game.py"),
        },
        {
            "text": "Space Shooter",
            "action": lambda: launch_game("gamesss/SpaceShooter/main.py"),
        },
        {
            "text": "AeroBlaster",
            "action": lambda: launch_game("gamesss/AeroblasterSource/Aeroblaster.py"),
        },
    ]

    global current_page
    total_pages = (len(gamex) + games_per_page - 1) // games_per_page

    while True:
        GAME_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        # Відображення ігор для поточної сторінки
        start_index = current_page * games_per_page
        end_index = start_index + games_per_page
        visible_games = gamex[start_index:end_index]

        for i, button_info in enumerate(visible_games):
            button = Button(
                image=None,
                pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + i * 100),
                text_input=button_info["text"],
                font=get_font(30),
                base_color="Yellow",
                hovering_color="Green",
            )

            button.changeColor(GAME_MOUSE_POS)
            button.update(SCREEN)

            if button.checkForInput(GAME_MOUSE_POS):
                if pygame.mouse.get_pressed()[0]:
                    click_sound.play()
                    button_info["action"]()

        # Додаємо стрілки
        left_arrow = Button(
            image=None,
            pos=(50, SCREEN_HEIGHT // 2),
            text_input="<",
            font=get_font(50),
            base_color="White",
            hovering_color="Green",
        )
        right_arrow = Button(
            image=None,
            pos=(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2),
            text_input=">",
            font=get_font(50),
            base_color="White",
            hovering_color="Green",
        )

        if current_page > 0:
            left_arrow.changeColor(GAME_MOUSE_POS)
            left_arrow.update(SCREEN)
            if (
                left_arrow.checkForInput(GAME_MOUSE_POS)
                and pygame.mouse.get_pressed()[0]
            ):
                current_page -= 1
                click_sound.play()

        if current_page < total_pages - 1:
            right_arrow.changeColor(GAME_MOUSE_POS)
            right_arrow.update(SCREEN)
            if (
                right_arrow.checkForInput(GAME_MOUSE_POS)
                and pygame.mouse.get_pressed()[0]
            ):
                current_page += 1
                click_sound.play()

        PLAY_BACK.changeColor(GAME_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (
                    PLAY_BACK.checkForInput(GAME_MOUSE_POS)
                    and pygame.mouse.get_pressed()[0]
                ):
                    click_sound.play()
                    return

        pygame.display.update()


# Fonction qui affiche le guide pour un jeu spécifique
# Функція, яка відображає посібник для конкретної гри
def guide(game_name):
    # Список кнопок з поясненнями та їх відповідними діями
    guide_buttons = [
        {"text": "Puissance 4", "action": lambda: show_explanation(game_connect4)},
        {"text": "Flappy Bird", "action": lambda: show_explanation(flappy_bird)},
        {"text": "GPS analyse", "action": lambda: show_explanation(gps_tool)},
        {
            "text": "Beta Minecraft",
            "action": lambda: show_explanation(
                "Je pense que vous n'avez pas besoin de savoir comment jouer"
            ),
        },
        {"text": "Pong Game", "action": lambda: show_explanation(pong_game)},
        {"text": "Snake", "action": lambda: show_explanation(snake_game)},
        {"text": "Space Shooter", "action": lambda: show_explanation(snake_game)},
        {"text": "Aeroblaster", "action": lambda: show_explanation(snake_game)},
    ]

    current_page = 0
    buttons_per_page = 5  # Кількість пояснень на одній сторінці
    total_pages = (len(guide_buttons) + buttons_per_page - 1) // buttons_per_page

    while True:
        GUIDE_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))

        # Відображення тексту заголовка
        GUIDE_TEXT = get_font(45).render(
            f"Ceci est l'écran GUIDE de {game_name}.", True, "White"
        )
        GUIDE_RECT = GUIDE_TEXT.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8))
        SCREEN.blit(GUIDE_TEXT, GUIDE_RECT)

        # Відображення кнопок для поточної сторінки
        start_index = current_page * buttons_per_page
        end_index = start_index + buttons_per_page
        visible_buttons = guide_buttons[start_index:end_index]

        for i, button_info in enumerate(visible_buttons):
            button = Button(
                image=None,
                pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + i * 60),
                text_input=button_info["text"],
                font=get_font(30),
                base_color="Yellow",
                hovering_color="Green",
            )

            button.changeColor(GUIDE_MOUSE_POS)
            button.update(SCREEN)

            if button.checkForInput(GUIDE_MOUSE_POS):
                if pygame.mouse.get_pressed()[0]:
                    click_sound.play()
                    button_info["action"]()

        # Додавання стрілок для навігації
        left_arrow = Button(
            image=None,
            pos=(50, SCREEN_HEIGHT // 2),
            text_input="<",
            font=get_font(50),
            base_color="White",
            hovering_color="Green",
        )
        right_arrow = Button(
            image=None,
            pos=(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2),
            text_input=">",
            font=get_font(50),
            base_color="White",
            hovering_color="Green",
        )

        if current_page > 0:
            left_arrow.changeColor(GUIDE_MOUSE_POS)
            left_arrow.update(SCREEN)
            if left_arrow.checkForInput(GUIDE_MOUSE_POS) and pygame.mouse.get_pressed()[0]:
                current_page -= 1
                click_sound.play()

        if current_page < total_pages - 1:
            right_arrow.changeColor(GUIDE_MOUSE_POS)
            right_arrow.update(SCREEN)
            if right_arrow.checkForInput(GUIDE_MOUSE_POS) and pygame.mouse.get_pressed()[0]:
                current_page += 1
                click_sound.play()

        PLAY_BACK.changeColor(GUIDE_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(GUIDE_MOUSE_POS):
                    if pygame.mouse.get_pressed()[0]:
                        click_sound.play()
                        return

        pygame.display.update()



def show_explanation(explanation_text):
    # Découpe le texte d'explication en lignes
    explanation_lines = explanation_text.strip().split("\n")

    # Configuration de la police et de la fenêtre d'explication
    explanation_font = get_font(10)
    explanation_window = pygame.Surface((SCREEN_WIDTH // 1.5, SCREEN_HEIGHT // 1.5))
    explanation_window.blit(BG, (0, 0))

    # Position de départ du texte
    y_position = 10

    # Boucle pour afficher chaque ligne d'explication
    for line in explanation_lines:
        explanation_surface = explanation_font.render(line, True, "White")
        explanation_rect = explanation_surface.get_rect(
            topleft=(10, y_position)
        )  # Alignement à gauche
        explanation_window.blit(explanation_surface, explanation_rect)
        y_position += explanation_rect.height + 5

    # Position du bouton de retour en arrière (BACK)
    button_position = (int(SCREEN_WIDTH * 0.9), int(SCREEN_HEIGHT * 0.9))
    explanation_back_button = Button(
        image=None,
        pos=button_position,
        text_input="BACK",
        font=get_font(20),
        base_color="White",
        hovering_color="Green",
    )

    while True:
        # Gestion des événements Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                button_clicked = explanation_back_button.checkForInput(
                    pygame.mouse.get_pos()
                )
                if button_clicked and pygame.mouse.get_pressed()[0]:
                    click_sound.play()
                    return

        # Affichage de la fenêtre d'explication et du bouton de retour en arrière (BACK)
        SCREEN.blit(explanation_window, (10, SCREEN_HEIGHT // 4))
        explanation_back_button.changeColor(pygame.mouse.get_pos())
        explanation_back_button.update(SCREEN)

        # Mise à jour de l'écran
        pygame.display.update()


def launch_game(game_path):
    try:
        # Stop the background music when a game starts
        background_music.stop()

        # Launch the game
        subprocess_game = subprocess.Popen(
            ["python", os.path.join(base_path, game_path)]
        )
        subprocess_game.wait()

        # Resume the background music after the game ends
        background_music.play(-1)

    except FileNotFoundError as e:
        logging.error("Erreur lors du lancement du jeu %s: %s", game_path, e)



def main_menu():
    buttonss = [
        {"text": "PROGRAMS", "action": progrmas},
        {"text": "GUIDE", "action": lambda: guide("GAME")},
        {"text": "QUIT", "action": pygame.quit},
    ]

    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for i, button_info in enumerate(buttonss):
            button = Button(
                image=None,
                pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + i * 150),
                text_input=button_info["text"],
                font=get_font(75),
                base_color="#d7fcd4",
                hovering_color="Green",
            )

            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

            if button.checkForInput(MENU_MOUSE_POS):
                if pygame.mouse.get_pressed()[0]:
                    click_sound.play()
                    button_info["action"]()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

main_menu()
