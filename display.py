import curses
import constants
import threading
import Queue
import log


class DisplayManager(object):
    def __init__(self, display):
        self.update_queue = Queue.Queue()
        self.update_queue.put(None)
        self.display = display
        self.display_thread = None

    def start(self, board):
        self.display_thread = DisplayThread(self.update_queue, self.display, board)
        self.display_thread.start()

    def update(self, message=None):
        if message != None:
            log.info("Message from display: {}".format(message))
        self.update_queue.put(message)

    def exit(self):
        self.update_queue.put("die")
        self.display_thread.join()


class DisplayThread(threading.Thread):
    def __init__(self, update_queue, display, board):
        threading.Thread.__init__(self)
        self.update_queue = update_queue
        self.display = display
        self.display.setup(self.update_queue, board)

    def run(self):
        self.display.display()


class C4Display(object):

    def __init__(self):
        pass

    def setup(self, update_queue, board):
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


    def setup(self, update_queue, board):
        self.child.setup(update_queue, board)


    def exit(self):
        self.child.exit()


    def display(self):
        curses.wrapper(self.child.display)


class TextOnlyDisplayCurses(C4Display):

    def __init__(self):
        self.update_queue = None
        self.stdscr = None

    def setup(self, update_queue, board):
        self.update_queue = update_queue
        self.board = board

    def exit(self):
        pass

    def display(self, stdscr):
        self.stdscr = stdscr
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.bkgd(' ', curses.color_pair(1))

        self.stdscr.timeout(0)
        self.stdscr.clear()

        self.update_screen(None)

        ch = 0 
        while ch != 'q':
            # Check for new board to update
            try:
                message = self.update_queue.get(block=False)
                if message == "die":
                    return
                self.update_screen(message)
            except:
                # No updates for board
                pass

            # Check for user input
            try:
                ch = self.stdscr.getkey()
            except:
                curses.napms(10)


    def update_screen(self, message):
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

	self.stdscr.refresh()

