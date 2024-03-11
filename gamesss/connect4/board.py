import numpy as np  # Importation du module numpy pour manipuler des tableaux multidimensionnels

class Board:
    def __init__(self, row_count, column_count):
        # Initialisation de la classe Board avec le nombre de lignes et de colonnes spécifié
        self.row_count = row_count  # Nombre de lignes dans le tableau
        self.column_count = column_count  # Nombre de colonnes dans le tableau
        self.grid = np.zeros((row_count, column_count))  # Création d'un tableau de zéros pour représenter le plateau de jeu

    def is_valid_location(self, column):
        # Vérifie si la dernière ligne dans la colonne est vide
        return self.grid[self.row_count - 1, column] == 0

    def get_next_open_row(self, column):
        # Retourne la première instance où la ligne est vide
        for row in range(self.row_count):
            if self.grid[row, column] == 0:
                return row

    def drop_piece(self, row, column, turn):
        # Remplit le point spécifié avec le tour actuel
        self.grid[row, column] = turn

    def has_four_in_a_row(self, turn):
        # Vérifie horizontalement
        for r in range(self.row_count):
            for c in range(self.column_count - 3):
                if self.grid[r, c] == turn and self.grid[r, c + 1] == turn and self.grid[r, c + 2] == turn and self.grid[r, c + 3] == turn:
                    return True

        # Vérifie verticalement
        for r in range(self.row_count - 3):
            for c in range(self.column_count):
                if self.grid[r, c] == turn and self.grid[r + 1, c] == turn and self.grid[r + 2, c] == turn and self.grid[r + 3, c] == turn:
                    return True

        # Vérifie en diagonale vers le haut
        for r in range(self.row_count - 3):
            for c in range(self.column_count - 3):
                if self.grid[r, c] == turn and self.grid[r + 1, c + 1] == turn and self.grid[r + 2, c + 2] == turn and self.grid[r + 3, c + 3] == turn:
                    return True

        # Vérifie en diagonale vers le bas
        for r in range(3, self.row_count):
            for c in range(self.column_count - 3):
                if self.grid[r, c] == turn and self.grid[r - 1, c + 1] == turn and self.grid[r - 2, c + 2] == turn and self.grid[r - 3, c + 3] == turn:
                    return True

        return False

    def is_full(self):
        # Détermine si chaque emplacement dans la grille est rempli
        return self.grid.all()

    def reset(self):
        # Remplit la grille de zéros pour une nouvelle manche
        self.grid = np.zeros((self.row_count, self.column_count))

    def print_grid(self):
        # Affiche l'état du jeu dans la console
        print(np.flip(self.grid, 0))  # Utilisation de np.flip pour inverser l'ordre des lignes et rendre l'affichage plus intuitif