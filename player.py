import pygame
from pygame import draw
from itertools import product
import numpy as np
from board import Board

class Player():
    def __init__(self, surface, size, num, color):
        self.surface = surface
        self.win_size = size
        self.square_size = (int(size[0]/8), int(size[1]/8))
        self.n_men = 15
        self.n_kings = 0
        self.n_eaten = 0
        self.color = color
        self.player = num
        Board.init_pos(self, self.player)
        
    
    def do_move(self, selected, moveto, board):
        moves = self.check_forced_move(board)
        if ((selected, moveto) in moves) or (len(moves) == 0):
            dead = self.check_eating_move(selected, moveto, board)
            if not dead:
                if self.check_valid_move(selected, moveto, board):
                    self.pieces_position[moveto[0]][moveto[1]] = self.pieces_position[selected[0]][selected[1]]
                    self.pieces_position[selected[0]][selected[1]] = 0
                    if self.player == 1 and moveto[1] == 7:
                        self.promote_king(moveto)
                    elif self.player == 2 and moveto[1] == 0:
                        self.promote_king(moveto)
                    return True
                else:
                    return False
            else:
                self.n_eaten = self.n_eaten + 1
                self.pieces_position[moveto[0]][moveto[1]] = self.pieces_position[selected[0]][selected[1]]
                self.pieces_position[selected[0]][selected[1]] = 0
                if self.player == 1 and moveto[1] == 7:
                    self.promote_king(moveto)
                elif self.player == 2 and moveto[1] == 0:
                    self.promote_king(moveto)
                return dead
        else:
            return False

    def check_forced_move(self, board):
        moves = list()
        for x, y in product(range(8), range(8)):
            if self.pieces_position[x][y] != 0:
                selected = (x, y)
                for dx, dy in product((-2,2),(-2,2)):
                    moveto = (dx+x, dy+y)
                    dead = None
                    if moveto[0] >= 0 and moveto[0] < 8 and moveto[1] >= 0 and moveto[1] < 8:
                        dead = self.check_eating_move(selected, moveto, board)
                    if dead:
                        moves.append((selected, moveto))
                
                        
        return moves

    def check_eating_move(self, selected, moveto, board):
        dir = (np.sign(moveto[0]-selected[0]), np.sign(moveto[1]-selected[1]))
        if self.player == 1 and self.pieces_position[selected[0]][selected[1]] == 1:
            if dir[1] < 0:
                return False
        elif self.player == 2 and self.pieces_position[selected[0]][selected[1]] == 1:
            if dir[1] > 0:
                return False
        check_eat = board[selected[0]+dir[0]][selected[1]+dir[1]]
        if check_eat != 0: 
            if int(check_eat.player_num) != int(self.player):
                if int(check_eat.state) != 1 or int(check_eat.state) != 2:
                    if abs(selected[0]-moveto[0]) == 2 and abs(selected[1]-moveto[1]) == 2 and board[moveto[0]][moveto[1]] == 0:
                        return (selected[0]+dir[0], selected[1]+dir[1])
                    else:
                        return False
        else:
            return False

    def check_valid_move(self, selected, moveto, board):
        if board[moveto[0]][moveto[1]] == 0 and board[selected[0]][selected[1]] != 0:
            if board[selected[0]][selected[1]].state == 2:
                if abs(moveto[0]-selected[0]) == 1 and abs(moveto[1]-selected[1]) == 1:
                    return True
            elif board[selected[0]][selected[1]].state == 1:
                if abs(moveto[0]-selected[0]) == 1:
                    if self.player == 1 and (moveto[1]-selected[1]) == 1:
                        return True
                    elif self.player == 2 and (moveto[1]-selected[1]) == -1:
                        return True
            return False
        else:
            return False

    def promote_king(self, pos):
        self.pieces_position[pos[0]][pos[1]] = 2

    def update_dead(self, dead):
        if not (dead is True or dead is False):
            self.pieces_position[dead[0]][dead[1]] = 0

    def draw(self):
        for i in range(8):
            for j in range(8):
                if self.pieces_position[i][j] == 1:
                    centre = (i*self.square_size[0]+int(self.square_size[0]/2),
                              j*self.square_size[1]+int(self.square_size[1]/2))
                    radius = int(self.square_size[0]/2*(7/8))
                    draw.circle(self.surface, self.color, centre, radius)
                elif self.pieces_position[i][j] == 2:
                    centre = (i*self.square_size[0]+int(self.square_size[0]/2),
                              j*self.square_size[1]+int(self.square_size[1]/2))
                    radius = int(self.square_size[0]/2*(7/8))
                    draw.circle(self.surface, self.color, centre, radius)
                    invert_color = (255-self.color[0], 255-self.color[1], 255-self.color[2])
                    radius = int(self.square_size[0]/2*(2/8))
                    draw.circle(self.surface, invert_color, centre, radius)
                    draw.circle(self.surface, invert_color, (centre[0]+8, centre[1]), radius)
                    draw.circle(self.surface, invert_color, (centre[0], centre[1]+8), radius)
                    draw.circle(self.surface, invert_color, (centre[0]-8, centre[1]), radius)
                    draw.circle(self.surface, invert_color, (centre[0], centre[1]-8), radius)


