import constants
import log


class MoveResult(object):
    def __init__(self):
        self.winner = False
        self.consecutives = []


def find_first_empty_row(board, col):
    for row in range(constants.num_rows - 1, -1, -1):
        if board[row][col] == None:
            return row
    return None


# Using this repeatedly by itself is slower than generating board_anaysis and checking that
# However, for look-aheads that change the board first, we need to still use this
# Also, this assumes the move has already been made
def check_for_winner(board, move_col, move_row, move_mark):
    winner = False
    result = analyze_move(board, move_col, move_row, move_mark)
    if result != None:
        winner = result.winner
    log.debug("Checking for winner in col {0} and row {1} for player {2}: {3}".format(move_col, move_row, move_mark, winner))
    return winner


def analyze_board(board, mark):
    board_analysis = []
    for col in range(0, constants.num_cols):
        move_results = analyze_potential_move(board, col, mark)
        board_analysis.append(move_results)
    return board_analysis


# Returns the result of making a move at move_col
def analyze_potential_move(board, move_col, move_mark):
    row = find_first_empty_row(board, move_col)
    if row == None:
        return None

    return analyze_move(board, move_col, row, move_mark)


# Returns the results of the move at this coordinate
def analyze_move(board, move_col, move_row, move_mark):
    result = MoveResult()

    # Consecutive pieces of the same mark as the move
    cons_left = 0
    cons_right = 0
    cons_up = 0
    cons_down = 0
    cons_nw = 0
    cons_ne = 0
    cons_sw = 0
    cons_se = 0

    # Check left (columns "move-1" to "0")
    for i in range(0, move_col):
        # Search from the move to the left
        col = move_col - i - 1
        if board[move_row][col] == move_mark:
            #log.debug("Found consecutive mark at col: {} row: {}".format(col, move_row))
            cons_left += 1
        else:
            break

    # Check right (columns "move" to num_cols)
    for i in range(move_col+1, constants.num_cols):
        # Search from the move to the right
        col = i
        if board[move_row][col] == move_mark:
            #log.debug("Found consecutive mark at col: {} row: {}".format(col, move_row))
            cons_right += 1
        else:
            break

    # Check up
    for i in range(0, move_row):
        # Search from the move to the right
        row = move_row - i - 1
        if board[row][move_col] == move_mark:
            #log.debug("Found consecutive mark at col: {} row: {}".format(move_col, row))
            cons_up += 1
        else:
            break

    # Check down
    for i in range(move_row+1, constants.num_rows):
        # Search from the move to the right
        row = i
        if board[row][move_col] == move_mark:
            #log.debug("Found consecutive mark at col: {} row: {}".format(move_col, row))
            cons_down += 1
        else:
            break

    # Check NW
    row = move_row
    for i in range(0, move_col):
        col = move_col - i - 1
        row = row - 1
        if row < 0:
            break
        if board[row][col] == move_mark:
            #log.debug("Found consecutive mark at col: {} row: {}".format(col, row))
            cons_nw += 1
        else:
            break

    # Check NE
    row = move_row
    for i in range(move_col+1, constants.num_cols):
        col = i
        row = row - 1
        if row < 0:
            break
        if board[row][col] == move_mark:
            #log.debug("Found consecutive mark at col: {} row: {}".format(col, row))
            cons_ne += 1
        else:
            break

    # Check SW
    row = move_row
    for i in range(0, move_col):
        col = move_col - i - 1
        row = row + 1
        if row >= constants.num_rows:
            break
        if board[row][col] == move_mark:
            #log.debug("Found consecutive mark at col: {} row: {}".format(col, row))
            cons_sw += 1
        else:
            break

    # Check SE
    row = move_row
    for i in range(move_col+1, constants.num_cols):
        col = i
        row = row + 1
        if row >= constants.num_rows:
            break
        if board[row][col] == move_mark:
            #log.debug("Found consecutive mark at col: {} row: {}".format(col, row))
            cons_se += 1
        else:
            break

    # Including the move, we need to have three other consecutive pieces to be a winner
    result.consecutives.append(cons_left + cons_right)
    if cons_left + cons_right >= 3:
        log.info("Winner found at col {0} and row {1} for player {2} going left ({3}) and right ({4})".format(move_col, move_row, move_mark, cons_left, cons_right))
        result.winner = True

    result.consecutives.append(cons_up + cons_down)
    if cons_up + cons_down >= 3:
        log.info("Winner found at col {0} and row {1} for player {2} going up ({3}) and down ({4})".format(move_col, move_row, move_mark, cons_up, cons_down))
        result.winner = True

    result.consecutives.append(cons_nw + cons_se)
    if cons_nw + cons_se >= 3:
        log.info("Winner found at col {0} and row {1} for player {2} going nw ({3}) and se ({4})".format(move_col, move_row, move_mark, cons_nw, cons_se))
        result.winner = True

    result.consecutives.append(cons_ne + cons_sw)
    if cons_ne + cons_sw >= 3:
        log.info("Winner found at col {0} and row {1} for player {2} going ne ({3}) and sw ({4})".format(move_col, move_row, move_mark, cons_ne, cons_sw))
        result.winner = True

    return result


def create_empty_board():
    board = []
    for row in range(0,constants.num_rows):
        board.append([])
        for spot in range(0,constants.num_cols):
            board[row].append(None)
    return board

