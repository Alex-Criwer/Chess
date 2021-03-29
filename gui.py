import pygame
import numpy as np
import os
import time
import json
from ai import AI
from board import Board
from player import Player

WIN_SIZE = (WIDTH, HEIGHT) = (512, 512)
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
FIGURE_1 = (100, 100, 100) 
FIGURE_2 = (255, 255, 255)


def game_loop():
        game_data = {}
        selected = None
        moveto = None
        player_turn = player_1
        while(True):
            gameboard.draw_board(player_turn)
            player_1.draw()
            player_2.draw()
           
            if selected:
                draw_selected(window, selected, player_turn)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not selected:
                        selected = select_piece(window, player_turn, selected, moveto, event)
                    elif selected:
                        tmp = select_piece(window, player_turn, selected, moveto, event)
                        if tmp != selected:
                            moveto = tmp
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        with open("data.json", "w", encoding="utf8") as f:
                            game_data['pieces_position_1'] = np.array(player_1.pieces_position).tolist()
                            game_data['pieces_position_2'] = np.array(player_2.pieces_position).tolist()
                            json.dump(game_data, f)   
                    if event.key == pygame.K_l:
                        with open("data.json", "r", encoding="utf8") as f: 
                            game_data = json.load(f)
                            player_1.pieces_position = np.asarray(game_data['pieces_position_1'])
                            player_2.pieces_position = np.asarray(game_data['pieces_position_2'])
                           

            if player_turn == player_1:
                board = copy_board(gameboard.board)
                try:
                    valMove, aiMove = AIPlayer.minimax(board, 5, True)
                    selected = aiMove[0]
                    moveto = aiMove[1]
                except TypeError:
                    Selected = None
                    moveto = None
                  
            if moveto is not None:
                if player_turn == player_1:
                    tmp = player_1.do_move(selected, moveto, gameboard.board)
                    player_2.update_dead(tmp)
                elif player_turn == player_2:
                    tmp = player_2.do_move(selected, moveto, gameboard.board)
                    player_1.update_dead(tmp)
                gameboard.update_board(player_1.pieces_position, player_2.pieces_position)

                if tmp is not False:
                    clear_window()
                    if type(tmp) == tuple:
                        player_turn = switch(gameboard, player_turn, moveto)
                    else:
                        if player_turn == player_1:
                            player_turn = player_2
                        else:
                            player_turn = player_1

                moveto = None
                selected = None

            pygame.display.flip()


def select_piece(surface, player, selected, moveto, event):
    pos = event.__dict__['pos']
    posgrid = (int(pos[0]/player.square_size[0]), int(pos[1]/player.square_size[1]))
    if selected is None and moveto is None:
        if player.pieces_position[posgrid[0], posgrid[1]]:
            return posgrid
        else:
            return False
    elif selected is not None and moveto is None:
        return posgrid
    else:
        return False


def draw_selected(surface, posgrid, player):
    if player.pieces_position[posgrid[0], posgrid[1]]:
        color = (player.color[0], player.color[1], player.color[2])
        rect = (posgrid[0]*player.square_size[0], posgrid[1]*player.square_size[1],
                player.square_size[0], player.square_size[1])
        pygame.draw.rect(surface, color, rect, 3)
        pygame.display.flip()

def choice_player(board, type_state, near_enemy, dir_enemy, board_figure, select,x,y,turn, enemy_side):
    if board_figure.state == 1 or board_figure.state == 2:
        near_enemy.append((select[0]+x, select[1]+y))
        dir_enemy.append((x, y))
        newpos = (near_enemy[-1][0]+dir_enemy[-1][0],
                  near_enemy[-1][1]+dir_enemy[-1][1])
        if newpos[0] >= 0 and newpos[0] < 8 and newpos[1] >= 0 and newpos[1] < 8:
            if board.board[newpos[0]][newpos[1]] == 0:
                if type == 1 and dir_enemy[-1][1] == -1:
                    pass
                else:
                    return turn
    
def switch(board, turn, select):
    if turn == player_1:
        near_enemy = list()
        dir_enemy = list()
        type_state = board.board[select[0]][select[1]].state
        for x in (-1, 1):
            for y in (-1, 1):
                if (select[0]+x >= 0 and select[0]+x < 8) and (select[1]+y >= 0 and select[1]+y < 8):
                    board_figure = board.board[select[0]+x][select[1]+y]               
                    if (board_figure != 0):
                        if (board_figure.player_num == 2):
                            choice_player(board, type_state, near_enemy, dir_enemy, board_figure, select,x,y,turn, -1)
        return player_2
    elif turn == player_2:
        near_enemy = list()
        dir_enemy = list()
        type_state = board.board[select[0]][select[1]].state
        for x in (-1, 1):
            for y in (-1, 1):
                if (select[0]+x >= 0 and select[0]+x < 8) and (select[1]+y >= 0 and select[1]+y < 8):
                    board_figure = board.board[select[0]+x][select[1]+y]               
                    if (board_figure != 0):
                        if (board_figure.player_num == 1):
                            choice_player(board, type_state, near_enemy, dir_enemy, board_figure, select,x,y,turn, 1)
        return player_1


def copy_board(board):
    copy = [[0 for x in range(8)] for y in range(8)]
    for x in range(8):
        for y in range(8):
            copy[x][y] = board[x][y]
    return copy


def clear_window():
    os.system('cls')

if __name__ == "__main__":

    pygame.display.init()
    clear_window()
    window = pygame.display.set_mode(WIN_SIZE)

    gameboard = Board(window, WIN_SIZE, BLACK, WHITE)
    player_1 = Player(window, WIN_SIZE, 1, FIGURE_1)
    player_2 = Player(window, WIN_SIZE, 2, FIGURE_2)
    AIPlayer = AI(1)
    AIPlayer2 = AI(2)

    gameboard.update_board(player_1.pieces_position, player_2.pieces_position)

    game_loop()
