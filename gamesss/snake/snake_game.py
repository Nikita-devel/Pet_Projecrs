# Importation des bibliothèques nécessaires
import pygame
import time
import random
import os

# Initialisation de Pygame
pygame.init()

# Définition des couleurs en RGB
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)

# Obtention du chemin de base du script
base_path = os.path.dirname(os.path.abspath(__file__))

# Configuration de l'écran de jeu
dis = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
dis_width, dis_height = pygame.display.get_surface().get_size()

pygame.display.set_caption('Jeu de serpent')

# Initialisation de l'horloge Pygame
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 25

# Chargement de la police personnalisée
custom_font = pygame.font.Font(os.path.join(base_path, 'assets', 'font.ttf'), 25)

# Chargement des effets sonores
game_over_sound = pygame.mixer.Sound(os.path.join(base_path, 'audio', 'gameover.mp3'))
eat_sound = pygame.mixer.Sound(os.path.join(base_path, 'audio', 'eat.mp3'))

# Chargement de la musique de fond
pygame.mixer.music.load(os.path.join(base_path, 'audio', 'backsound.mp3'))
pygame.mixer.music.play(-1)

# Chargement des images
background_img = pygame.image.load(os.path.join(base_path, 'assets', 'background.jpg'))
snake_head_img = pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets', 'Head.png')), (snake_block, snake_block))
snake_body_img = pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets', 'Body.png')), (snake_block, snake_block))
food_img = pygame.transform.scale(pygame.image.load(os.path.join(base_path, 'assets', 'Food.png')), (snake_block, snake_block))

# Initialisation de l'angle et du son de fin de jeu
angle = 0
global game_over_sound_played
game_over_sound_played = False

# Fonction pour afficher le score
def Your_score(score):
    value = custom_font.render("Votre score : " + str(score), True, yellow)
    dis.blit(value, [(dis_width - value.get_width()) // 2, 10])

# Fonction pour afficher un message
def message(msg, color):
    mesg = custom_font.render(msg, True, color)
    dis.blit(mesg, [(dis_width - mesg.get_width()) // 2, (dis_height - mesg.get_height()) // 2])

# Fonction pour afficher le serpent
def our_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        if i == 0:
            dis.blit(snake_head_img, (x[0], x[1]))
        else:
            dis.blit(snake_body_img, (x[0], x[1]))

# Fonction pour générer de la nourriture
def spawn_food():
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    return foodx, foody

# Chemin du fichier contenant le score le plus élevé
score_file_path = os.path.join(base_path, 'highest_score.txt')
highest_score = 0

# Fonction pour charger le score le plus élevé
def load_highest_score():
    global highest_score
    if os.path.exists(score_file_path):
        with open(score_file_path, 'r') as file:
            highest_score = int(file.read())

# Fonction pour sauvegarder le score le plus élevé
def save_highest_score():
    with open(score_file_path, 'w') as file:
        file.write(str(highest_score))

# Chargement du score le plus élevé
load_highest_score()

# Fonction pour afficher le score
def show_score(score, record):
    score_text = custom_font.render(f"Score : {score} Record : {record}", True, yellow)
    dis.blit(score_text, [10, 10])

# Boucle principale du jeu
def gameLoop():
    global game_over
    global game_over_sound_played
    global highest_score
    game_over = False
    game_close = False
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1
    foods = [spawn_food() for _ in range(5)]

    while not game_over:
        while game_close == True:
            dis.blit(background_img, (0, 0))

            # Mise à jour du score le plus élevé
            if Length_of_snake - 1 > highest_score:
                highest_score = Length_of_snake - 1
                save_highest_score()

            # Affichage du message de fin de jeu et du score
            message(f"Vous avez perdu ! Votre score : {Length_of_snake - 1} Score le plus élevé : {highest_score}", red)

            # Lecture du son de fin de jeu s'il n'a pas déjà été joué
            if not game_over_sound_played:
                game_over_sound.play()
                game_over_sound_played = True
            
            pygame.display.update()
            
            # Gestion des événements pour les boutons de l'utilisateur
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_over_sound_played = False
                        gameLoop()

        # Gestion des événements pour les boutons de l'utilisateur
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Gestion des collisions avec les bords
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.blit(background_img, (0, 0))

        # Affichage de la nourriture
        for food in foods:
            dis.blit(food_img, (food[0], food[1]))

        # Affichage du serpent et du score
        our_snake(snake_block, snake_List)
        show_score(Length_of_snake - 1, highest_score)
        pygame.display.update()

        # Gestion de la consommation de la nourriture
        for food in foods:
            if x1 == food[0] and y1 == food[1]:
                foods.remove(food)
                foods.append(spawn_food())
                Length_of_snake += 1
                eat_sound.play()

        # Mise à jour de la position de la tête du serpent
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)

        snake_List.insert(0, snake_Head)

        # Gestion de la longueur du serpent
        if len(snake_List) > Length_of_snake:
            del snake_List[Length_of_snake:]

        # Gestion des collisions avec le corps du serpent
        for x in snake_List[1:]:
            if x == snake_Head:
                game_close = True

        clock.tick(snake_speed)

    # Arrêt de la musique de fond et fermeture de Pygame
    pygame.mixer.music.stop()
    pygame.quit()
    save_highest_score()
    quit()

# Chargement du score le plus élevé
load_highest_score()

# Début de la boucle de jeu
gameLoop()
