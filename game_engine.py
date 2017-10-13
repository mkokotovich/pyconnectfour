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
        self.playerX_mark = "X"
        self.playerO_mark = "O"
        self.playerX = HumanPlayer(self.playerX_mark, self.display)
        self.playerO = RandomPlayer(self.playerO_mark)
        self.display.start(self.board)


    def play_game(self):
        try:
            self.play_one_game()
        except constants.UserQuit:
            log.info("User quit, exitting")


    def play_one_game(self):
        playerX_turn = True
        self.playerX.reset()
        self.playerO.reset()

        while not self.board_is_full():
            self.display.update("{}'s turn".format( "Player X" if playerX_turn else "Player O" ))
            successful_move = False
            while not successful_move:
                try:
                    self.make_move(playerX_turn)
                    successful_move = True
                except constants.InvalidMove:
                    self.display.update("{}'s turn, please make a valid move".format( "Player X" if playerX_turn else "Player O" ))

            if utils.check_for_winner(self.board, self.last_move_col, self.last_move_row, self.playerX_mark if playerX_turn else self.playerO_mark):
                self.display.update("Game over, {} won!".format( "Player X" if playerX_turn else "Player O" ))
                return
            playerX_turn = not playerX_turn

        # Board is full, it is a tie
        self.display.update("Game over, it is a tie!")
        return


    def board_is_full(self):
        return self.turns >= constants.num_rows * constants.num_cols


    def make_move(self, playerX_turn):
        move = None
        row = None
        if playerX_turn:
            move = self.playerX.move(self.board, self.last_move_col)
        else:
            move = self.playerO.move(self.board, self.last_move_col)

        log.debug("On turn {}, Player {} selects column {}".format(self.turns, "X" if playerX_turn else "O", move))

        if move < 0 or move > 6:
            raise constants.InvalidMove("Invalid move, less than 0 or greater than 6: {}".format(move))
        success = False
        for i in range(0, constants.num_rows):
            row = constants.num_rows - 1 - i
            if self.board[row][move] == None:
                self.board[row][move] = self.playerX_mark if playerX_turn else self.playerO_mark
                success = True
                break
        if success == False:
            raise constants.InvalidMove("Invalid move, could not find an empty spot in column {}".format(move))
        self.turns += 1
        self.last_move_col = move
        self.last_move_row = row


