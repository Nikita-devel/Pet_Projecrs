import turtle  # Importation de la bibliothèque turtle pour la création d'animations graphiques
import tkinter as tk  # Importation de tkinter pour créer une interface utilisateur
from tkinter import messagebox  # Importation de la boîte de dialogue du module tkinter
import pygame  # Importation de pygame pour gérer les sons
import os  # Importation du module os pour manipuler les chemins d'accès
from threading import Thread  # Importation de la classe Thread pour exécuter la musique en arrière-plan de manière asynchrone

# Définir le répertoire de travail pour le script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Initialiser le module de mixage pygame
pygame.mixer.init()

# Charger les sons avec os.path.join pour assurer la portabilité du code entre les plateformes
ball_bounce_sound = pygame.mixer.Sound(os.path.join(script_dir, "jump.wav"))
score_sound = pygame.mixer.Sound(os.path.join(script_dir,"scoree.wav"))
background_music = pygame.mixer.Sound(os.path.join(script_dir, "backgr.wav"))

# Fonction pour jouer de la musique de fond dans un thread séparé
def play_background_music():
    background_music.play(-1)  # -1 indique la boucle infinie

# Démarrer le thread de musique de fond
bg_music_thread = Thread(target=play_background_music)
bg_music_thread.start()

wn = turtle.Screen()
wn.title("Pong par @Nikita")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Score
score_a = 0
score_b = 0

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.7
ball.dy = -0.7

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Joueur A: 0 Joueur B: 0", align="center", font=("Courier", 24, "normal"))

# Fonction pour jouer le son de rebond de la balle
def play_ball_bounce_sound():
    ball_bounce_sound.play()

# Fonction pour jouer le son de point
def play_score_sound():
    score_sound.play()

# Fonction pour jouer la musique de fond
def play_background_music():
    background_music.play()

# Fonction de sortie
def exit_game():
    wn.bye()

# Vérifier les conditions de victoire
def check_win_conditions():
    global score_a, score_b
    if score_a == 7 or score_b == 7:
        winner = "Joueur A" if score_a == 7 else "Joueur B"
        response = messagebox.askquestion("Partie terminée", f"{winner} gagne !\nVoulez-vous rejouer ?")
        if response == "yes":
            reset_game()
        else:
            exit_game()

# Réinitialiser le jeu
def reset_game():
    global score_a, score_b
    score_a = 0
    score_b = 0
    pen.clear()
    pen.write("Joueur A: 0 Joueur B: 0", align="center", font=("Courier", 24, "normal"))
    paddle_a.goto(-350, 0)
    paddle_b.goto(350, 0)
    ball.goto(0, 0)
    ball.dx = 0.7
    ball.dy = -0.7

# Liaisons clavier pour les mouvements des raquettes
wn.listen()
wn.onkeypress(lambda: paddle_a.sety(paddle_a.ycor() + 20), "z")
wn.onkeypress(lambda: paddle_a.sety(paddle_a.ycor() - 20), "s")
wn.onkeypress(lambda: paddle_b.sety(paddle_b.ycor() + 20), "Up")
wn.onkeypress(lambda: paddle_b.sety(paddle_b.ycor() - 20), "Down")
wn.onkeypress(exit_game, "Escape")  # Bouton de sortie

# Boucle principale du jeu
while True:
    wn.update()

    # Déplacer la balle
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Collision entre la raquette A et la balle
    if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() - 50):
        ball.setx(-340)
        ball.dx *= -1
        play_ball_bounce_sound()

    # Collision entre la raquette B et la balle
    if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() - 50):
        ball.setx(340)
        ball.dx *= -1
        play_ball_bounce_sound()

    # Vérification des bordures
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
        pen.clear()
        pen.write("Joueur A: {} Joueur B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))
        play_score_sound()
        check_win_conditions()

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        pen.clear()
        pen.write("Joueur A: {} Joueur B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))
        play_score_sound()
        check_win_conditions()