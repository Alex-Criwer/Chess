from random import shuffle
from itertools import product

class AI():
    def __init__(self, player_num):
        self.player = player_num
        self.piece_strength = 10
        self.king_strength = 50
        self.side_strength = 20
        self.wall_strength = 10

    def get_possible_moves(self, board):
        moves = []
        for x, y in product(range(8), range(8)):
            if board[x][y] != 0 and board[x][y].player_num == int(self.player):
                for dx, dy in product((-1,1), (-1,1)):
                    if x+dx >= 0 and x+dx < 8 and y+dy >= 0 and y+dy < 8:
                        if self.player == 1:
                            if board[x][y].state == 2 or dy > 0:
                                moves += self.check_possible_move_for_player(board, x, y, dx, dy)
                        elif self.player == 2:
                            if board[x][y].state == 2 or dy < 0:
                                moves += self.check_possible_move_for_player(board, x, y, dx, dy)
        shuffle(moves)
        return moves
    
    def check_possible_move_for_player(self, board, x,y,dx,dy):
        moves = []
        if board[x+dx][y+dy] == 0:
            moves.append(((x, y), (x+dx, y+dy)))
        elif board[x+dx][y+dy].player_num != int(self.player):
            if x+2*dx >= 0 and x+2*dx < 8 and y+2*dy >= 0 and y+2*dy < 8:
                if board[x+2*dx][y+2*dy] == 0:
                    moves.append(((x, y), (x+2*dx, y+2*dy)))
    
        shuffle(moves)
        return moves
        
    # Функция оценки
    def position_evaluation(self, board):
        value = 0
        n1 = 0
        n2 = 0
        for x in range(8):
            for y in range(8):
                if not board[x][y] == 0:
                    if board[x][y].player_num == int(self.player):
                        n1 += 1
                        if x < 4:
                            value += int(1/(x+1))*self.side_strength
                        else:
                            value += int(1/(abs(x-8)))*self.side_strength
                        value += int((y+1)/8)*self.wall_strength
                        if board[x][y].state == 1:
                            value += self.piece_strength
                        elif board[x][y].state == 2:
                            value += self.king_strength
                    else:
                        n2 += 1
                        if x < 4:
                            value -= int(1/(x+1))*self.side_strength
                        else:
                            value -= int(1/(abs(x-8)))*self.side_strength
                        value -= int(abs(y-8)/8)*self.wall_strength
                        if board[x][y].state == 1:
                            value -= self.piece_strength
                        elif board[x][y].state == 2:
                            value -= self.king_strength
        if n2 == 0 and n1 > 0:
            value = 10000
        elif n1 == 0 and n2 > 0:
            value = -10000
        return value


    # Минимакс для перебора в глубину
    def minimax(self, board, depth, isMax):
        current_strength = self.position_evaluation(board)
        moves = self.get_possible_moves(board)
        if abs(current_strength) == 1000:
            return current_strength, None
            
        if depth <= 0:
            return current_strength, None
        
        
        
        if isMax:
            best_strength = -100000
            cmp_func = max
            return self.best_move_strength(board, cmp_func, moves, depth, best_strength)
        else:
            best_strength = 100000
            cmp_func = min
            return self.best_move_strength(board, cmp_func, moves, depth, best_strength)
            

    def best_move_strength(self, board, cmp_func, moves, depth, best_strength):
        best_move = None
        for move in moves:
            board = self.update_board(board, move)
            move_strength = self.minimax(board, depth-1, True)
            tmp = best_strength
            best_strength = cmp_func(best_strength, move_strength[0])
            if tmp != best_strength:
                best_move = move
        return best_strength, best_move
    
    def update_board(self, board, move):
        selected_x, selected_y = move[0]
        to_x, to_y = move[1]
        if abs(selected_x-to_x) == 2 and abs(selected_y-to_y) == 2:
            dir = (to_x - selected_x, to_y - selected_y)
            board[selected_x + dir[0]][selected_y + dir[1]] = 0
        piece = board[selected_x][selected_y]
        board[to_x][to_y] = piece
        board[selected_x][selected_y] = 0
        return board 