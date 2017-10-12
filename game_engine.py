import utils
import constants
from player import *
from move import *
import log

class GameEngine(object):
    def __init__(self, display):
        self.board = utils.create_empty_board()
        self.last_move_col = None
        self.last_move_row = None
        self.display = display
        self.turns = 0
        self.player1_mark = "X"
        self.player2_mark = "O"
        self.player1 = SimplePlayer(self.player1_mark)
        self.player2 = SimplePlayer(self.player2_mark)
        self.display.start(self.board)


    def play_game(self):
        player1_turn = True
        self.player1.reset()
        self.player2.reset()

        while not self.board_is_full():
            self.display.update("{}'s turn".format( "Player 1" if player1_turn else "Player 2" ))
            self.make_move(player1_turn)
            if utils.check_for_winner(self.board, self.last_move_col, self.last_move_row, self.player1_mark if player1_turn else self.player2_mark):
                self.display.update("Game over, {} won!".format( "Player 1" if player1_turn else "Player 2" ))
                return
            player1_turn = not player1_turn

        # Board is full, it is a tie
        self.display.update("Game over, it is a tie!")
        return


    def board_is_full(self):
        return self.turns >= constants.num_rows * constants.num_cols


    def make_move(self, player1_turn):
        move = None
        row = None
        log.debug("Matt, passing last_move_col as {}".format(self.last_move_col))
        if player1_turn:
            move = self.player1.move(self.board, self.last_move_col)
        else:
            move = self.player2.move(self.board, self.last_move_col)

        log.debug("On turn {}, Player {} selects column {}".format(self.turns, "1" if player1_turn else "2", move))

        if move < 0 or move > 6:
            raise Exception("Invalid move, less than 0 or greater than 6: {}".format(move))
        success = False
        for i in range(0, constants.num_rows):
            row = constants.num_rows - 1 - i
            if self.board[row][move] == None:
                self.board[row][move] = self.player1_mark if player1_turn else self.player2_mark
                success = True
                break
        if success == False:
            raise Exception("Invalid move, could not find an empty spot")
        self.turns += 1
        self.last_move_col = move
        log.debug("Matt, updated last_move_col to {}".format(self.last_move_col))
        self.last_move_row = row


