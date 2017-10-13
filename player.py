import constants
import time
import log
import random
import utils

class Player(object):
    def __init__(self, mark):
        pass

    def reset(self):
        pass

    def move(self, board, previous_move):
        pass


class SimplePlayer(Player):
    def __init__(self, mark):
        self.mark = mark
        self.other_player = "O" if self.mark == "X" else "X"
        self.columns = []
        self.reset()


    def reset(self):
        self.columns = []
        for i in range(0, constants.num_cols):
            self.columns.append([])


    def move(self, board, previous_move):
        if previous_move != None:
            self.columns[previous_move].append(self.other_player)
        for i in range(0, constants.num_cols):
            if len(self.columns[i]) < constants.num_rows:
                log.debug("player {} finds column {} to have room, length {}".format(self.mark, i, len(self.columns[i])))
                self.columns[i].append(self.mark)
                return i


class RandomPlayer(Player):
    def __init__(self, mark):
        self.mark = mark
        self.other_player = "O" if self.mark == "X" else "X"
        self.columns = []
        self.reset()


    def reset(self):
        self.columns = []
        for i in range(0, constants.num_cols):
            self.columns.append([])


    def move(self, board, previous_move):
        if previous_move != None:
            self.columns[previous_move].append(self.other_player)
        random_cols = range(0, constants.num_cols)
        random.shuffle(random_cols)
        for i in random_cols:
            if len(self.columns[i]) < constants.num_rows:
                log.debug("player {} finds column {} to have room, length {}".format(self.mark, i, len(self.columns[i])))
                self.columns[i].append(self.mark)
                return i


class HumanPlayer(Player):
    def __init__(self, mark, display):
        self.mark = mark
        self.other_player = "O" if self.mark == "X" else "X"
        self.display = display
        self.reset()


    def move(self, board, previous_move):
        move_int = -1
        message = "Player " + self.mark + "'s turn, please enter your move"
        while move_int < 0 or move_int > constants.num_cols:
            move = self.display.get_move(message)
            try:
                move_int = int(move)
            except:
                message = "Player " + self.mark + "'s turn, please enter a valid move between 0 and 6"
                pass
        return move_int


class MattAI(Player):
    def __init__(self, mark):
        self.mark = mark
        self.other_player = "O" if self.mark == "X" else "X"
        self.columns = []
        self.reset()


    def reset(self):
        self.columns = []
        for i in range(0, constants.num_cols):
            self.columns.append([])


    def find_first_empty_row(self, board, col):
        for row in range(constants.num_rows - 1, 0, -1):
            if board[row][col] == None:
                return row
        return None


    def check_for_winning_move(self, board):
        for col in range(0, constants.num_cols):
            row = self.find_first_empty_row(board, col)
            if row == None:
                continue
            if utils.check_for_winner(board, col, row, self.mark):
                log.debug("player {} finds winning move in column {}".format(self.mark, col))
                return col
        return None


    def check_for_opponent_winning_move(self, board):
        for col in range(0, constants.num_cols):
            row = self.find_first_empty_row(board, col)
            if row == None:
                continue
            if utils.check_for_winner(board, col, row, self.other_player):
                log.debug("player {} finds opponents winning move in column {}, choosing it to block".format(self.mark, col))
                return col
        return None


    def count_winning_moves(self, board):
        winning_moves = 0
        for col in range(0, constants.num_cols):
            row = self.find_first_empty_row(board, col)
            if row == None:
                continue
            if utils.check_for_winner(board, col, row, self.mark):
                log.debug("player {} finds winning move in column {}".format(self.mark, col))
                winning_moves += 1
        return winning_moves


    def check_for_move_that_wins_in_two_moves(self, board):
        best_move = None
        for col in range(0, constants.num_cols):
            row = self.find_first_empty_row(board, col)
            if row == None:
                continue
            # If we play here
            board[row][col] = self.mark
            opponent_win = self.check_for_opponent_winning_move(board)
            # If the opponent can win, skip this move
            if opponent_win != None:
                board[row][col] = None
                continue
            # Otherwise count how many winning moves there are for me
            winning_moves = self.count_winning_moves(board)
            if winning_moves > 0:
                best_move = col if best_move == None else max(best_move, col)
            board[row][col] = None
        return best_move


    def find_any_available_move(self, board):
        random_cols = range(0, constants.num_cols)
        random.shuffle(random_cols)
        for col in random_cols:
            row = self.find_first_empty_row(board, col)
            if row == None:
                continue
            log.debug("player {} finds column {} to have room, length {}".format(self.mark, col, len(self.columns[col])))
            return col
        return None


    def move(self, board, previous_move):
        if previous_move != None:
            self.columns[previous_move].append(self.other_player)
        # First check to see if I can win
        move = self.check_for_winning_move(board)
        if move != None:
            return move
        # Then check to see if I need to block my opponent from winning
        move = self.check_for_opponent_winning_move(board)
        if move != None:
            return move
        # Then check to see if I have a move that will make me win in two moves
        move = self.check_for_move_that_wins_in_two_moves(board)
        if move != None:
            return move
        # Fall back to any available move
        move = self.find_any_available_move(board)
        if move != None:
            return move
        return -1

