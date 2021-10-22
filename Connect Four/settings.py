# Recommended settings: ROWS = 8, COLS = 16, AI_DIFFICULTY = 2 or ROWS = 6, COLS = 7, AI_DIFFICULTY = 4

# Number of columns can only be a positive number below 17
# Number of rows can only be a positive number below 9
ROWS = 8
COLS = 16
# Default window sizes:
WIDTH = 858 + max(0, (COLS - 16) * 50)
HEIGHT = 480 + max(0, (ROWS - 8) * 50)

# Custom window sizes:
WIDTH = WIDTH
HEIGHT = HEIGHT

# Used colors
FG = '#424247'
BG = '#FFFFFD'
RED = '#D64C42'
BLUE = '#18778C'

# High difficulty raises AI's processing time
# Difficulty has to be at least 1
AI_DIFFICULTY = 1

# Secret button activates top secret stuff
SECRET_BUTTON = True

win_sound = 'win_2.wav'
piece_1_sound = 'plastic_impact_1.mp3'
piece_2_sound = 'plastic_impact_2.mp3'
erase_sound = 'erase.mp3'
click_sound = 'click_1.mp3'

# Volume can only be between 0 and 1
VOLUME = 0.3
