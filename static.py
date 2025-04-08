
#Screen
WIDTH, HEIGHT = 1600, 1000 
current_window_w, current_window_h = WIDTH, HEIGHT
SCREEN_CHANGE_RATIO_W, SCREEN_CHANGE_RATIO_H = 1, 1

#Object Names
PLACEABLE_OBJECT_NAMES = ("BH", "Jupiter 2.0", "Sun 2.0")

#Colors
WHITE =(255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (255, 0, 0)
DARK_GRAY = (80, 78, 81)
ORANGE = (255, 165, 0)
TAN = (188, 152, 126)
BABY_BLUE = (137, 207, 240)
DARK_BLUE = (32, 42, 68)
BLACK = (0, 0, 0)

#Buttons
BUTTON_WIDTH_RATIO, BUTTON_HEIGHT_RATIO = 1/15, 1/30
BUTTON_WIDTH, BUTTON_HEIGHT = (WIDTH * BUTTON_WIDTH_RATIO), (WIDTH * BUTTON_HEIGHT_RATIO)

#Timestep
frames = 0
TIMESTEP = (
        3600 * 24
    )  # the difference in time betweent frames. Since we want each frame to represent one day, we will use the amount of seconds in a day
TIMESTEP_MULTIPLIER = 1

#Booleans Misc.
pause = False
place_active = False

