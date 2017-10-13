import curses
import constants
import threading
import Queue
import log


class DisplayManager(object):
    def __init__(self, display):
        self.update_queue = Queue.Queue()
        self.update_queue.put(None)
        self.input_queue = Queue.Queue()
        self.display = display
        self.display_thread = None

    def start(self, board):
        self.display_thread = DisplayThread(self.update_queue, self.input_queue, self.display, board)
        self.display_thread.start()

    def update(self, message=None):
        if not self.display_thread.isAlive():
            raise constants.UserQuit("User quit the game")
        if message != None:
            log.info("Message from display: {0}".format(message))
        self.update_queue.put(message)

    def get_move(self, message):
        if not self.display_thread.isAlive():
            raise constants.UserQuit("User quit the game")
        log.info("Asking user for input")
        self.update_queue.put("input")
        self.update_queue.put(message)
        move = self.input_queue.get(block=True)
        log.info("Received {0} from user".format(move))
        if move == None:
            raise constants.UserQuit("User quit game")
        return move
        

    def exit(self):
        self.update_queue.put("die")
        self.display_thread.join()


class DisplayThread(threading.Thread):
    def __init__(self, update_queue, input_queue, display, board):
        threading.Thread.__init__(self)
        self.update_queue = update_queue
        self.input_queue = input_queue
        self.display = display
        self.display.setup(self.update_queue, self.input_queue, board)

    def run(self):
        self.display.display()


class C4Display(object):

    def __init__(self):
        pass

    def setup(self, update_queue, input_queue, board):
        pass

    def exit(self):
        pass

    # board is a two dimensional array board[x] is a row (numbered 0-5), and board[x][y] is a spot on the row,
    # with 0 being the furthest left spot.
    # Columns:  0 1 2 3 4 5 6
    #         0 x x x x x x x
    #      R  1 x x x x x x x
    #      o  2 x x x x x x x
    #      w  3 x x x x x x x
    #      s  4 x x x x x x x
    #         5 x x x x x x x
    def display(self, board):
        pass


class TextOnlyDisplay(C4Display):

    def __init__(self):
        self.child = TextOnlyDisplayCurses()


    def setup(self, update_queue, input_queue, board):
        self.child.setup(update_queue, input_queue, board)


    def exit(self):
        self.child.exit()


    def display(self):
        curses.wrapper(self.child.display)


class TextOnlyDisplayCurses(C4Display):

    def __init__(self):
        self.update_queue = None
        self.input_queue = None
        self.stdscr = None

    def setup(self, update_queue, input_queue, board):
        self.update_queue = update_queue
        self.input_queue = input_queue
        self.board = board

    def exit(self):
        pass

    def display(self, stdscr):
        self.stdscr = stdscr
        curses.use_default_colors()
        curses.init_pair(1, -1, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.bkgd(' ', curses.color_pair(1))

        self.stdscr.timeout(0)
        self.stdscr.clear()

        self.update_screen(None)

        ch = 0 
        while ch != 'q':
            get_input = False

            # Check for new board to update
            try:
                message = self.update_queue.get(block=False)
                if message == "die":
                    return
                if message == "input":
                    message = self.update_queue.get(block=True)
                    get_input = True
                self.update_screen(message, get_input=get_input)
            except:
                # No updates for board
                pass

            # Check for user input
            while True:
                try:
                    ch = self.stdscr.getkey()
                    if get_input:
                        self.input_queue.put(ch)
                    break
                except:
                    curses.napms(10)
                    if not get_input:
                        break

        # Just in case game thread is waiting for input
        self.input_queue.put(None)


    def update_screen(self, message, get_input=False):
        self.stdscr.clear()
        rownum = 1
        colnum = 1
        self.stdscr.addstr(rownum, colnum, "Welcome to Connect Four")
        rownum += 1
        self.stdscr.addstr(rownum, colnum, "Press 'q' to quit")
        rownum += 1
        if message:
            self.stdscr.addstr(rownum, colnum, message)
            rownum += 1
        self.stdscr.addstr(rownum, colnum, "")
        rownum += 1

        for row in self.board:
            rowstr = ""
            for spot in row:
                if spot != None:
                    rowstr += spot
                else:
                    rowstr += "-"
                rowstr += "  "
            self.stdscr.addstr(rownum, colnum, rowstr)
            rownum += 1

        self.stdscr.addstr(rownum, colnum, "")
        rownum += 1
        self.stdscr.addstr(rownum, colnum, "0  1  2  3  4  5  6")
        rownum += 1
        if get_input:
            self.stdscr.addstr(rownum, colnum, "Please enter the column number you'd like to play in:")
            rownum += 1

	self.stdscr.refresh()

