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
        self.my_board_analysis = None
        self.other_board_analysis = None
        self.reset()


    def reset(self):
        pass


    # Checks against static board analysis
    def check_for_winning_move(self):
        move = None
        for col in range(0, constants.num_cols):
            result = self.my_board_analysis[col]
            if result == None:
                continue
            if result.winner:
                log.info("check_for_winning_move: player {} finds winning move in column {}".format(self.mark, col))
                move = col
                break
        log.debug("check_for_winning_move returning {}".format(move))
        return move


    # Checks against board
    def check_for_opponent_winning_move(self, board, caller=None):
        caller_str = ""
        if caller != None:
            caller_str = " (for {})".format(caller)

        move = None
        for col in range(0, constants.num_cols):
            row = utils.find_first_empty_row(board, col)
            if row == None:
                continue
            if utils.check_for_winner(board, col, row, self.other_player):
                log.info("check_for_opponent_winning_move{}: player {} finds opponents winning move in column {}".format(caller_str, self.mark, col))
                move = col
                break

        log.debug("check_for_opponent_winning_move returning {}".format(move))
        return move


    def count_winning_moves(self, board, mark, caller=None):
        caller_str = ""
        if caller != None:
            caller_str = " (for {})".format(caller)

        winning_moves = 0
        winning_move_cols = []
        for col in range(0, constants.num_cols):
            row = utils.find_first_empty_row(board, col)
            if row == None:
                continue
            if utils.check_for_winner(board, col, row, mark):
                winning_moves += 1
                winning_move_cols.append(col)
        log.info("count_winning_moves{}: player {} has {} winning moves in columns {}".format(caller_str, mark, winning_moves, winning_move_cols))
        return winning_moves


    def check_for_move_that_wins_in_two_moves(self, board):
        best_move = None
        for col in range(0, constants.num_cols):
            row = utils.find_first_empty_row(board, col)
            if row == None:
                continue
            # If we play here
            board[row][col] = self.mark
            opponent_win = self.check_for_opponent_winning_move(board, "check_for_move_that_wins_in_two_moves")
            # If the opponent can win, skip this move
            if opponent_win != None:
                board[row][col] = None
                continue
            # Otherwise count how many winning moves there are for me
            winning_moves = self.count_winning_moves(board, self.mark, "check_for_move_that_wins_in_two_moves")
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
            row = utils.find_first_empty_row(board, col)
            if row == None:
                continue
            # If we play here
            board[row][col] = self.mark
            # Can the opponent win?
            opponent_win = self.check_for_opponent_winning_move(board, "check_for_move_that_blocks_opponent_in_two_moves")
            # Reset board
            board[row][col] = None
            # If the opponent can win, skip this move
            if opponent_win != None:
                continue
            # If opponent plays here
            board[row][col] = self.other_player
            # can the opponent have two winning moves?
            winning_moves = self.count_winning_moves(board, self.other_player, "check_for_move_that_blocks_opponent_in_two_moves")
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
        opponent_can_win = self.check_for_opponent_winning_move(board, "other_could_win_after_this_move")
        # Reset the board
        board[row][col] = None
        return opponent_can_win


    def remove_full_columns(self, board, potential_moves):
        new_moves = []
        for col in potential_moves:
            row = utils.find_first_empty_row(board, col)
            if row == None:
                continue
            else:
                new_moves.append(col)
        log.info("remove_full_columns: player {} keeps moves {}".format(self.mark, new_moves))
        return new_moves


    def remove_moves_that_give_opponent_an_immediate_winning_move(self, board, potential_moves):
        new_moves = []
        for col in potential_moves:
            row = utils.find_first_empty_row(board, col)
            if row == None:
                # Should not happen, but keeping this just in case
                continue
            if self.other_could_win_after_this_move(board, col, row):
                continue
            else:
                new_moves.append(col)
        log.info("remove_moves_that_give_opponent_an_immediate_winning_move: player {} keeps moves: {}".format(self.mark, new_moves))
        return new_moves


    # Doesn't check for opponent winning in a single move, as that should be 
    # removed already
    def remove_moves_that_give_opponent_a_winning_move_in_two_moves(self, board, potential_moves):
        new_moves = []
        for col in potential_moves:
            row = utils.find_first_empty_row(board, col)
            if row == None:
                continue
            # If we play here
            board[row][col] = self.mark
            # If we are at the top of the board, it can't hurt
            if row == 0:
                # Reset board
                board[row][col] = None
                new_moves.append(col)
                continue
            # If opponent plays above us:
            board[row-1][col] = self.other_player
            # can the opponent have two winning moves?
            winning_moves = self.count_winning_moves(board, self.other_player, "remove_moves_that_give_opponent_a_winning_move_in_two_moves")
            if winning_moves > 1:
                # If so, skip this move
                # Reset board
                board[row][col] = None
                board[row-1][col] = None
                continue
            # If we've made it this far, the move is safe
            new_moves.append(col)
            # Reset board and continue to next col
            board[row][col] = None
            board[row-1][col] = None

        log.info("remove_moves_that_give_opponent_a_winning_move_in_two_moves: player {} keeps moves: {}".format(self.mark, new_moves))
        return new_moves


    def find_moves_that_give_at_least_x_in_a_row(self, potential_moves, num_consecutive):
        new_moves = []
        for col in potential_moves:
            result = self.my_board_analysis[col]
            if result == None:
                continue
            # num_consecutive includes the current move, results.consecutives doesn't
            if max(result.consecutives) >= num_consecutive - 1:
                new_moves.append(col)
        return new_moves

    def find_moves_that_give_at_least_two_in_a_row(self, potential_moves):
        new_moves = self.find_moves_that_give_at_least_x_in_a_row(potential_moves, 2)
        log.info("find_moves_that_give_at_least_two_in_a_row: player {} keeps moves: {}".format(self.mark, new_moves))
        return new_moves

    def find_moves_that_give_at_least_three_in_a_row(self, potential_moves):
        new_moves = self.find_moves_that_give_at_least_x_in_a_row(potential_moves, 3)
        log.info("find_moves_that_give_at_least_three_in_a_row: player {} keeps moves: {}".format(self.mark, new_moves))
        return new_moves

    def find_moves_that_block_opponent_from_getting_three_in_a_row(self, potential_moves):
        return potential_moves


    def move(self, board, previous_move):
        # First analyze the board for me
        self.my_board_analysis = utils.analyze_board(board, self.mark)

        # First check to see if I can win
        move = self.check_for_winning_move()
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
        potential_moves = range(0,constants.num_cols)

        # Not looping, just a way to break to bottom
        while True:
            # Remove any full columns first
            new_moves = self.remove_full_columns(board, potential_moves)
            if len(new_moves) != 0:
                potential_moves = new_moves
            else:
                log.error("move: Error: No valid moves, this should have been caught by the game engine")
                break

            # Remove all moves that give the oppenent an immediate winning move
            new_moves = self.remove_moves_that_give_opponent_an_immediate_winning_move(board, potential_moves)
            if len(new_moves) != 0:
                potential_moves = new_moves
            else:
                break
            
            # Then remove all moves that give the opponent a winning move in two moves
            new_moves = self.remove_moves_that_give_opponent_a_winning_move_in_two_moves(board, potential_moves)
            if len(new_moves) != 0:
                potential_moves = new_moves
            else:
                break

            # Exit this fake loop
            break

        # The next block of logic will use board analysis for other player
        self.other_board_analysis = utils.analyze_board(board, self.other_player)

        # Another fake loop, just to control code flow
        while True:
            # Then find moves that gives me two in a row
            new_moves = self.find_moves_that_give_at_least_two_in_a_row(potential_moves)
            if len(new_moves) != 0:
                potential_moves = new_moves

            # Then find moves that gives me three in a row
            new_moves = self.find_moves_that_give_at_least_three_in_a_row(potential_moves)
            if len(new_moves) != 0:
                potential_moves = new_moves

            # Then find moves that blocks opponent from getting three in a row
            new_moves = self.find_moves_that_block_opponent_from_getting_three_in_a_row(potential_moves)
            if len(new_moves) != 0:
                potential_moves = new_moves

            # Exit this fake loop
            break


        # Now pick any of the remaining moves
        move = random.choice(potential_moves)

        return move


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

