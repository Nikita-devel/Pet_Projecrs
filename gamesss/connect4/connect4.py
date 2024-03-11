import sys  # Importation du module système pour gérer les fonctionnalités système
import tkinter  # Importation du module tkinter pour créer une interface graphique
import tkinter.messagebox  # Importation de la boîte de dialogue du module tkinter

import pygame  # Importation du module pygame pour créer des jeux en Python

import board  # Importation du module board, qui semble contenir la logique du jeu

# Constantes de couleur
NOIR = (0, 0, 0)
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
JAUNE = (255, 255, 0)


class Pane:
    def __init__(self, row_count, column_count, square_size):
        # Initialisation de la classe Pane avec la configuration du plateau et la taille des cases
        self.board = board.Board(row_count, column_count)  # Initialisation de l'objet Board pour gérer l'état du jeu
        self.square_size = square_size  # Taille de chaque case du plateau
        self.radius = square_size // 2 - 5  # Rayon du cercle représentant une pièce dans une case
        self.width = column_count * square_size  # Largeur totale du plateau
        self.height = (row_count + 1) * square_size  # Hauteur totale du plateau (avec une rangée supplémentaire pour la pièce suivante en haut)
        self.row_offset = square_size  # Décalage vertical pour prendre en compte la rangée supplémentaire en haut
        self.circle_offset = square_size // 2  # Décalage pour centrer le cercle à l'intérieur de chaque case de la grille
        self.screen = pygame.display.set_mode((self.width, self.height))  # Initialisation de la fenêtre du jeu avec la taille du plateau

    def draw_background(self):
        # Dessine le fond du plateau avec des rectangles bleus et des cercles noirs au centre de chaque case
        for r in range(self.board.row_count):
            for c in range(self.board.column_count):
                left = c * self.square_size
                top = r * self.square_size + self.row_offset
                pygame.draw.rect(self.screen, BLEU, (left, top, self.square_size, self.square_size))
                pygame.draw.circle(self.screen, NOIR, (left + self.circle_offset, top + self.circle_offset), self.radius)
        pygame.display.update()

    def fill_in_pieces(self):
        # Remplit chaque case du plateau avec la couleur de la pièce à cet emplacement
        for r in range(self.board.row_count):
            for c in range(self.board.column_count):
                if self.board.grid[r, c] == 1:
                    current_color = ROUGE
                elif self.board.grid[r, c] == 2:
                    current_color = JAUNE
                else:
                    current_color = NOIR
                x_position = c * self.square_size + self.circle_offset
                y_position = self.height - (r * self.square_size + self.circle_offset)  # Inversion car les pièces doivent venir du bas vers le haut
                pygame.draw.circle(self.screen, current_color, (x_position, y_position), self.radius)
        pygame.display.update()

    def track_mouse_motion(self, x_position, current_color):
        # Déplace la position x de la prochaine pièce le long du haut du panneau lorsque l'utilisateur déplace la souris
        pygame.draw.rect(self.screen, NOIR, (0, 0, self.width, self.square_size))  # Réinitialise le haut du panneau en noir
        pygame.draw.circle(self.screen, current_color, (x_position, self.circle_offset), self.radius)
        pygame.display.update()

    def try_drop_piece(self, x_position, turn):
        # Convertit la position x de la souris de l'utilisateur en une sélection de colonne
        # Remplit cette colonne si elle n'est pas pleine
        # Renvoie si l'opération a été effectuée ou non
        column_selection = x_position // self.square_size
        if self.board.is_valid_location(column_selection):
            row = self.board.get_next_open_row(column_selection)
            self.board.drop_piece(row, column_selection, turn)
            return True
        return False

    def reset(self):
        # Prépare le Pane pour une autre partie
        self.screen = pygame.display.set_mode((self.width, self.height))  # Redonne le focus à Pygame
        self.board.reset()
        self.draw_background()
        self.fill_in_pieces()


def prompt_player(winner=False):
    # Lance une boîte de dialogue tkinter montrant le résultat de la fin du jeu
    # Demande à l'utilisateur de rejouer et renvoie le choix de l'utilisateur
    title = 'Game Over!'
    if winner:
        message = f'Player {winner} win ! Do you want to play again ?'
    else:
        message = 'No winner, Do you want to play again ?'
    return tkinter.messagebox.askyesno(title=title, message=message)

def main():
    # Configuration du jeu
    tkinter.Tk().wm_withdraw()  # Masque la fenêtre principale de tkinter, n'utilise que la boîte de dialogue
    pygame.init()
    pygame.display.set_caption('Connect 4')  # Définit le titre de la fenêtre du jeu
    pane = Pane(6, 7, 90)  # Crée un objet Pane avec un plateau de 6 lignes, 7 colonnes et des cases de 90 pixels
    pane.draw_background()  # Dessine le fond du plateau
    continue_playing = True  # Variable pour contrôler la poursuite du jeu
    turn = 1  # Variable pour suivre le tour actuel (1 ou 2)
    current_color = ROUGE  # Couleur de la pièce pour le joueur actuel

    # Début du jeu
    while continue_playing:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                pane.track_mouse_motion(event.pos[0], current_color)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pane.try_drop_piece(event.pos[0], turn):
                    pane.fill_in_pieces()
                    if pane.board.has_four_in_a_row(turn):  # Vérifie si le joueur actuel a gagné
                        continue_playing = prompt_player(turn)
                        pane.reset()
                    elif pane.board.is_full():  # Vérifie s'il y a un match nul
                        continue_playing = prompt_player()
                        pane.reset()
                    else:  # Prépare le prochain tour
                        turn = 1 if turn == 2 else 2  # Alterne le tour entre 1 et 2 après chaque sélection valide
                        current_color = ROUGE if turn == 1 else JAUNE  # La couleur du joueur 1 est rouge, celle du joueur 2 est jaune
                        pane.track_mouse_motion(event.pos[0], current_color)  # Change la couleur de la prochaine pièce

if __name__ == "__main__":
    main()