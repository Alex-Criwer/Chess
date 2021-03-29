import numpy as np
from pygame import draw, surface
from figure import FigureState


class Board():
    def __init__(self, surface, size, color_1, color_2):
        self.surface = surface
        self.window_size = size
        self.square_size = (int(size[0]/8), int(size[1]/8))
        self.color_1 = color_1
        self.color_2 = color_2
        self.board = [[0 for x in range(8)] for y in range(8)]

    def draw_board(self, turn):
        self.surface.fill(self.color_2)
        for i in range(0, self.window_size[0], 2*self.square_size[0]):
            for j in range(0, self.window_size[1], 2*self.square_size[1]):
                draw.rect(self.surface, self.color_1,
                                 (i, j, self.square_size[0], self.square_size[1]))
        for i in range(self.square_size[0], self.window_size[0], 2*self.square_size[0]):
            for j in range(self.square_size[1], self.window_size[1], 2*self.square_size[1]):
                draw.rect(self.surface, self.color_1,
                                 (i, j, self.square_size[0], self.square_size[1]))
        draw.rect(self.surface, turn.color, ((0, 0), self.window_size), 3)

    def update_board(self, player_1, player_2):
        for x in range(8):
            for y in range(8):
                if player_1[x][y] > 0:
                    self.board[x][y] = FigureState(1, player_1[x][y])
                elif player_2[x][y] > 0:
                    self.board[x][y] = FigureState(2, player_2[x][y])
                else:
                    self.board[x][y] = 0
                    
    @staticmethod
    def init_pos(self, n):
        self.pieces_position = np.zeros(shape=(8, 8))
        if n == 1:
            for i in range(3):
                for j in range(0, 8, 2):
                    if (i == 0 or i == 2):
                        self.pieces_position[i][j] = 1
                    elif i == 1:
                        self.pieces_position[i][j+1] = 1
        if n == 2:
            for i in range(3):
                for j in range(0, 8, 2):
                    if (i == 0 or i == 2):
                        self.pieces_position[7-i][j+1] = 1
                    elif i == 1:
                        self.pieces_position[7-i][j] = 1
        self.pieces_position = self.pieces_position.transpose()
