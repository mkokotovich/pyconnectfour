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
                log.debug("player {0} finds column {1} to have room, length {2}".format(self.mark, i, len(self.columns[i])))
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
                log.debug("player {0} finds column {1} to have room, length {2}".format(self.mark, i, len(self.columns[i])))
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
        while move_int < 1 or move_int > constants.num_cols:
            move = self.display.get_move(message)
            log.info("Player " + self.mark + " inputed " + move)
            try:
                move_int = int(move)
            except:
                message = "Player " + self.mark + "'s turn, please enter a valid move between 1 and 7"
                pass
        # Now we need to translate it from human (1-7) to computer (0-6)
        move_int = move_int - 1

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
        for row in range(constants.num_rows - 1, -1, -1):
            if board[row][col] == None:
                return row
        return None


    def check_for_winning_move(self, board):
        for col in range(0, constants.num_cols):
            row = self.find_first_empty_row(board, col)
            if row == None:
                continue
            if utils.check_for_winner(board, col, row, self.mark):
                log.info("check_for_winning_move: player {} finds winning move in column {}".format(self.mark, col))
                return col
        return None


    def check_for_opponent_winning_move(self, board):
        for col in range(0, constants.num_cols):
            row = self.find_first_empty_row(board, col)
            if row == None:
                continue
            if utils.check_for_winner(board, col, row, self.other_player):
                log.info("check_for_opponent_winning_move: player {} finds opponents winning move in column {}, choosing it to block".format(self.mark, col))
                return col
        return None


    def count_winning_moves(self, board, mark):
        winning_moves = 0
        for col in range(0, constants.num_cols):
            row = self.find_first_empty_row(board, col)
            if row == None:
                continue
            if utils.check_for_winner(board, col, row, mark):
                log.debug("player {} finds winning move in column {}".format(mark, col))
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
            winning_moves = self.count_winning_moves(board, self.mark)
            if winning_moves > 1:
                best_move = col
            # reset move for next col
            board[row][col] = None
            if best_move is not None:
                log.info("check_for_move_that_wins_in_two_moves: player {} finds move in column {} that allows them to win in two moves".format(self.mark, col))
                break
        return best_move


    def check_for_move_that_blocks_opponent_in_two_moves(self, board):
        block_it = None
        for col in range(0, constants.num_cols):
            row = self.find_first_empty_row(board, col)
            if row == None:
                continue
            # If we play here
            board[row][col] = self.mark
            # Can the opponent win?
            opponent_win = self.check_for_opponent_winning_move(board)
            # Reset board
            board[row][col] = None
            # If the opponent can win, skip this move
            if opponent_win != None:
                continue
            # If opponent plays here
            board[row][col] = self.other_player
            # can the opponent have two winning moves?
            winning_moves = self.count_winning_moves(board, self.other_player)
            if winning_moves > 1:
                block_it = col
            # reset move for next col
            board[row][col] = None
            if block_it is not None:
                log.info("check_for_move_that_blocks_opponent_in_two_moves: player {} finds move in column {} that prevents the computer from winning in two moves".format(self.mark, col))
                break
        return block_it


    def other_could_win_after_this_move(self, board, col, row):
        # If we play here
        board[row][col] = self.mark
        # Can the opponent win?
        opponent_can_win = self.check_for_opponent_winning_move(board)
        # Reset the board
        board[row][col] = None
        return opponent_can_win


    def find_a_move_that_does_not_give_opponent_win_in_two_moves(self, board):
        move = None
        random_cols = range(0, constants.num_cols)
        random.shuffle(random_cols)
        for col in random_cols:
            row = self.find_first_empty_row(board, col)
            if row == None:
                continue
            # If we play here
            board[row][col] = self.mark
            # Can the opponent win?
            opponent_win = self.check_for_opponent_winning_move(board)
            # If the opponent can win, skip this move
            if opponent_win != None:
                # Reset board
                board[row][col] = None
                continue
            # If we are at the top of the board, it can't hurt
            if row == 0:
                move = col
                # Reset board
                board[row][col] = None
                break
            # If opponent plays above us:
            board[row-1][col] = self.other_player
            # can the opponent have two winning moves?
            winning_moves = self.count_winning_moves(board, self.other_player)
            if winning_moves > 1:
                # If so, skip this move
                # Reset board
                board[row][col] = None
                board[row-1][col] = None
                continue
            # If we've made it this far, the move is safe
            move = col
            # Reset board
            board[row][col] = None
            board[row-1][col] = None
            break

        if move is not None:
            log.info("find_a_move_that_does_not_give_opponent_win_in_two_moves: player {} finds move in column {} that does not allow the computer to win in two moves".format(self.mark, col))
        return move


    def find_a_move_that_does_not_give_the_opponent_a_win(self, board):
        random_cols = range(0, constants.num_cols)
        random.shuffle(random_cols)
        for col in random_cols:
            row = self.find_first_empty_row(board, col)
            if row == None:
                continue
            if self.other_could_win_after_this_move(board, col, row):
                continue
            log.info("find_a_move_that_does_not_give_the_opponent_a_win: player {} finds column {} to have room and not give opponent a winning move".format(self.mark, col))
            return col
        return None


    def find_any_available_move(self, board):
        random_cols = range(0, constants.num_cols)
        random.shuffle(random_cols)
        for col in random_cols:
            row = self.find_first_empty_row(board, col)
            if row == None:
                continue
            log.info("find_any_available_move: player {} finds column {} to have room, length {}".format(self.mark, col, len(self.columns[col])))
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
        # Then check to see if I need to block my opponent from winning in two moves
        move = self.check_for_move_that_blocks_opponent_in_two_moves(board)
        if move != None:
            return move


        ###
        # At this point, filter out moves that are undesirable before choosing a move
        ###
        # First remove all moves that give the oppenent an immediate winning move
        # Then remove all moves that give the opponent a winning move in two moves

        # Then pick a move that blocks opponent from getting three in a row?
        # Or pick a move that gives me two or three in a row (especially if it can't just be blocked)

        # Pick any move that will not give the opponent a winning move in two moves
        move = self.find_a_move_that_does_not_give_opponent_win_in_two_moves(board)
        if move != None:
            return move
        # If none available, pick any move that will not give the opponent a winning move
        move = self.find_a_move_that_does_not_give_the_opponent_a_win(board)
        if move != None:
            return move
        # Fall back to any available move
        move = self.find_any_available_move(board)
        if move != None:
            return move
        return -1


class JohnPlayer(Player):

    def move(self, board, previous_move):
        if previous_move != None:
            self.columns[previous_move].append(self.other_player)
        self.possible_moves(self.columns)
        for i in range(0, constants.num_cols):
            if len(self.columns[i]) < constants.num_rows:
                log.debug("player {0} finds column {1} to have room, length {2}".format(self.mark, i, len(self.columns[i])))
                self.columns[i].append(self.mark)
                return i

    def possible_moves(self, board):
        moves = []

        for col in range(0, constants.num_cols):
            for row in range(constants.num_rows - 1, 0, -1):
                log.debug('col {0}, row {1}'.format(col, row))
                if board[col][row] == None:
                    moves.append((col, row))
                    break

        log.info("possible moves: {0}, {1}, {2}, {3}, {4}, {5}, {6}".format(moves[0], moves[1], moves[2], moves[3], moves[4], moves[5], moves[6]))

        return moves

