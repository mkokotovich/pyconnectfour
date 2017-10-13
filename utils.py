import constants
import log

def check_for_winner(board, move_col, move_row, move_mark):

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
            #log.info("Found consecutive mark at col: {} row: {}".format(col, move_row))
            cons_left += 1
        else:
            break

    # Check right (columns "move" to num_cols)
    for i in range(move_col+1, constants.num_cols):
        # Search from the move to the right
        col = i
        if board[move_row][col] == move_mark:
            #log.info("Found consecutive mark at col: {} row: {}".format(col, move_row))
            cons_right += 1
        else:
            break

    # Check up
    for i in range(0, move_row):
        # Search from the move to the right
        row = move_row - i - 1
        if board[row][move_col] == move_mark:
            #log.info("Found consecutive mark at col: {} row: {}".format(move_col, row))
            cons_up += 1
        else:
            break

    # Check down
    for i in range(move_row+1, constants.num_rows):
        # Search from the move to the right
        row = i
        if board[row][move_col] == move_mark:
            #log.info("Found consecutive mark at col: {} row: {}".format(move_col, row))
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
            #log.info("Found consecutive mark at col: {} row: {}".format(col, row))
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
            #log.info("Found consecutive mark at col: {} row: {}".format(col, row))
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
            #log.info("Found consecutive mark at col: {} row: {}".format(col, row))
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
            #log.info("Found consecutive mark at col: {} row: {}".format(col, row))
            cons_se += 1
        else:
            break

    # Including the move, we need to have three other consecutive pieces
    winner = False
    if cons_left + cons_right >= 3:
        log.info("Winner found going left ({0}) and right ({1})".format(cons_left, cons_right))
        winner = True
    if cons_up + cons_down >= 3:
        log.info("Winner found going up ({0}) and down ({1})".format(cons_up, cons_down))
        winner = True
    if cons_nw + cons_se >= 3:
        log.info("Winner found going nw ({0}) and se ({1})".format(cons_nw, cons_se))
        winner = True
    if cons_ne + cons_sw >= 3:
        log.info("Winner found going ne ({0}) and sw ({1})".format(cons_ne, cons_sw))
        winner = True
    log.debug("Checking for winner in col {0} and row {1} for player {2}: {3}".format(move_col, move_row, move_mark, winner))

    return winner


def create_empty_board():
    board = []
    for row in range(0,constants.num_rows):
        board.append([])
        for spot in range(0,constants.num_cols):
            board[row].append(None)
    return board

