# game settings/options

HEIGHT = 600
WIDTH = 480
FPS = 60
WALKING_PERIOD = 200
STANDING_PERIOD = 350
TITLE = "Jumpy!"
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"

#player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.1
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 40
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = 20

#Game properties
BOOST_POWER = 60
PWP_SPAWN_PCT = 7

#starting platforms

PLATFORM_LIST = [(0, HEIGHT - 60),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]

#COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0 , 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
