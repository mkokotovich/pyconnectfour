from display import *
from game_engine import *
import random
import constants
import time


display = DisplayManager(TextOnlyDisplay())
engine = GameEngine(display)

try:
    engine.play_game()

except:
    display.exit()
