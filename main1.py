from if3_game.engine import init, Game, Layer, Sprite
from asteroid1 import RESOLUTION, Spaceship, Asteroid
from random import choice, randint

init(RESOLUTION, "Asteroid")

# -------- Background --------
background = Sprite("assets/galaxy.png", (0,0), anchor=(0,0))
background.scale_x = RESOLUTION[0] / background.width
background.scale_y = RESOLUTION[1] / background.height

# -------- Spaceship --------
spaceship = Spaceship((400,300))

# -------- Layer --------
main_layer = Layer()
main_layer.add(background)
main_layer.add(spaceship)

# ✅ Add hearts to layer
for heart in spaceship.hearts:
    main_layer.add(heart)

# -------- Asteroids --------
for _ in range(3):
    x = randint(64,736)
    y = randint(64,536)

    while 186 < x < 614 and 136 < y < 464:
        x = randint(64,736)
        y = randint(64,536)

    speed = (
        randint(30,70) * choice([1,-1]),
        randint(30,70) * choice([1,-1])
    )

    rotation_speed = randint(-50,50)

    asteroid = Asteroid((x,y), speed, rotation_speed)
    main_layer.add(asteroid)

# -------- Run Game --------
game = Game()
game.add(main_layer)
#game.debug = True # for green circle sprite
game.run()
