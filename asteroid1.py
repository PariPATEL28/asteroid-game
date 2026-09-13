from random import choice, randint
from if3_game.engine import Sprite
from pyglet.window import key as keyboard
from math import sin, cos, radians, sqrt

RESOLUTION = 1350,700

# -------- Base Object --------
class SpaceObject(Sprite):
    def __init__(self, image, position, anchor, speed=(0,0), rotation_speed=0):
        super().__init__(image, position, anchor=anchor, collision_shape="circle")
        self.speed = speed
        self.rotation_speed = rotation_speed

    def update(self, dt):
        super().update(dt)

        # Movement
        self.position = (
            self.position[0] + self.speed[0] * dt,
            self.position[1] + self.speed[1] * dt
        )

        self.rotation += self.rotation_speed * dt

        x, y = self.position

        # Screen wrap
        if x < -self.width/2:
            x = RESOLUTION[0] + self.width/2
        elif x > RESOLUTION[0] + self.width/2:
            x = -self.width/2

        if y < -self.height/2:
            y = RESOLUTION[1] + self.height/2
        elif y > RESOLUTION[1] + self.height/2:
            y = -self.height/2

        self.position = (x, y)

# -------- Asteroid --------
class Asteroid(SpaceObject):
    def __init__(self, position, speed, rotation_speed, level=3):
        self.level = level

        image = "assets/asteroid128.png"
        anchor = (64,64)

        if self.level == 2:
            image = "assets/asteroid64.png"
            anchor = (32,32)
        elif self.level == 1:
            image = "assets/asteroid32.png"
            anchor = (16,16)

        super().__init__(image, position, anchor, speed, rotation_speed)

    def on_collision(self, other):
        if isinstance(other, Bullet):
            other.destroy()
            self.destroy()
        elif isinstance(other, Spaceship):
            self.destroy()

    def destroy(self):
        super().destroy()

        if self.level > 1:
            for _ in range(3):
                speed = (
                    randint(30,70) * choice([1,-1]),
                    randint(30,70) * choice([1,-1])
                )
                rotation_speed = randint(-20,20)
                asteroid = Asteroid(self.position, speed, rotation_speed, self.level-1)
                self.layer.add(asteroid)

# -------- Spaceship --------
class Spaceship(SpaceObject):
    def __init__(self, position):
        super().__init__("assets/ship.png", position, (32,64))

        self.engine_on = False
        self.acceleration = 250

        self.invincibility = False
        self.chrono = 0

        self.life = 3

        # ❤️ Hearts
        self.hearts = []
        for i in range(self.life):
            heart = Heart((20 + i*40, RESOLUTION[1] - 40))
            self.hearts.append(heart)

    def on_key_press(self, key, _):
        if key == keyboard.RIGHT:
            self.rotation_speed = 180
        elif key == keyboard.LEFT:
            self.rotation_speed = -180

        if key == keyboard.UP:
            self.engine_on = True

        if key == keyboard.SPACE:
            self.create_bullet()

    def on_key_release(self, key, _):
        if key in (keyboard.LEFT, keyboard.RIGHT):
            self.rotation_speed = 0

        if key == keyboard.UP:
            self.engine_on = False

    def update(self, dt):
        if self.engine_on:
            angle = radians(-self.rotation + 90)
            self.speed = (
                self.speed[0] + cos(angle) * self.acceleration * dt,
                self.speed[1] + sin(angle) * self.acceleration * dt
            )

        # Invincibility timer
        if self.invincibility:
            self.chrono += dt
            if self.chrono >= 1:
                self.invincibility = False
                self.opacity = 255
                self.chrono = 0

        super().update(dt)

    def create_bullet(self):
        angle = radians(-self.rotation + 90)

        offset = self.height / 2
        pos = (
            self.position[0] + cos(angle) * offset,
            self.position[1] + sin(angle) * offset
        )

        speed_value = 300 + sqrt(self.speed[0]**2 + self.speed[1]**2)
        speed = (
            cos(angle) * speed_value,
            sin(angle) * speed_value
        )

        bullet = Bullet(pos, speed, 2)
        self.layer.add(bullet)

    def on_collision(self, other):
        if isinstance(other, Asteroid):

            if not self.invincibility:
                self.life -= 1
                print("Lives left:", self.life)

                # ❤️ remove one heart
                if self.hearts:
                    heart = self.hearts.pop()
                    heart.destroy()

                # 💀 Game Over
                if self.life <= 0:
                    print("Game Over")

                    game_over = GameOver()
                    self.layer.add(game_over)

                    self.destroy()
                    return

                # 🛡️ invincibility
                self.invincibility = True
                self.opacity = 125
                self.chrono = 0

# -------- Bullet --------
class Bullet(SpaceObject):
    def __init__(self, position, speed, life_time):
        super().__init__("assets/bullet.png", position, (8,8), speed)
        self.life_time = life_time
        self.chrono = 0

    def update(self, dt):
        super().update(dt)
        self.chrono += dt

        if self.chrono >= self.life_time:
            self.destroy()

# -------- Heart --------
class Heart(Sprite):
    def __init__(self, position):
        super().__init__("assets/heart.png", position, anchor=(16,16))

# -------- Game Over --------
class GameOver(Sprite):
    def __init__(self):
        super().__init__("assets/gameover.png", (0,0), anchor=(0,0))
        self.scale = 0.7
        # Now set position to center
        self.position = (RESOLUTION[0]//2 - self.width*self.scale//2 -50,
                         RESOLUTION[1]//2 - self.height*self.scale//2 - 50)

