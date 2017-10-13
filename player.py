import constants
import time
import log
import random

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

