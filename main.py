from display import *
from game_engine import *
import random
import constants
import time
import traceback


display = DisplayManager(TextOnlyDisplay())
engine = GameEngine(display)

try:
    engine.play_game()

except Exception as e:
    display.exit()
    print str(e)
    traceback.print_exc()
