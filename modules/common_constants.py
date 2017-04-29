import os

# KEYBOARD KEYS
Q_KEY = 113
F_KEY = 102

# COLORS
RED = (255,0,0)
BLACK = (0, 0, 0)
GREEN=(0,100,0)
GRAY=(125, 125, 125)
WHITE=(255,255,255)
BLUE=(0,0,255)

def root_path():
    return os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), os.pardir
        )
    )