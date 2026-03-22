import pygame
import math
from src.object_class.base_object import BaseObject
from src.physics.circle_collider import CircleCollider
from src.math import Vector2
 
PLAYER_SPEED = 200
SHOOT_COOLDOWN = 0.25
INVINCIBILITY_TIME = 2.0
 
 
class Player(BaseObject):
    def __init__(self, pos: Vector2):
        texture = pygame.image.load("assets/spaceship.png").convert_alpha()
        hitbox = CircleCollider(Vector2(pos.x, pos.y), 10)
        super().__init__(pos=Vector2(pos.x, pos.y), velocity=Vector2(0, 0),
                         rotation=0.0,              hitbox=hitbox,
                         texture=texture,           object_id=BaseObject.ID_PLAYER)
        self.lives = 3
        self.score = 0
        self._shoot_timer = 0.0
        self._invincible = 0.0
        self._blink_timer = 0.0
 
# ---
    def can_shoot(self) -> bool:
        return self._shoot_timer <= 0
 
    def on_shoot(self):
        self._shoot_timer = SHOOT_COOLDOWN
 
 
    def on_hit(self):
        if self._invincible > 0:
            return False
        self.lives -= 1
        self._invincible = INVINCIBILITY_TIME
        self._blink_timer = 0.0
        return True
 
 
    def is_invincible(self) -> bool:
        return self._invincible > 0
 
 
#           TODO: fix movement
    def update(self, dt: float):
        if self.lives <= 0: return

        if self._shoot_timer > 0: self._shoot_timer -= dt

        if self._invincible > 0:
            self._invincible -= dt
            self._blink_timer += dt

        mx, my = pygame.mouse.get_pos()
        mouse = Vector2(mx, my)
        diff = mouse - self.pos
        keys = pygame.key.get_pressed()
        move = Vector2(0, 0)

        if diff.length() > 1:
            forward = diff.normalize()
            right = Vector2(forward.y, -forward.x)

            if keys[pygame.K_w]:
                move += forward

            # if keys[pygame.K_s]:
            #     move += -forward

            if keys[pygame.K_d]:
                move += right

            if keys[pygame.K_a]:
                move += -right

        if move.length() > 0:
            target_velocity = move.normalize() * PLAYER_SPEED
            self.velocity = self.velocity.lerp(target_velocity, min(1.0, 1.1 * dt))  # start
        else:
            self.velocity = self.velocity * max(0.0, 1.0 - 1.1 * dt)  # brake

        self.pos += self.velocity * dt
        self.rotation = math.degrees(math.atan2(diff.y, diff.x)) + 90
        self._wrap_position(800, 600)
        self.hitbox.update(self.pos)
 
 
    def draw(self, viewport: pygame.Surface):
        if self.lives <= 0:
            return
        if self._invincible > 0 and int(self._blink_timer * 8) % 2 == 0:
            return
        self._blit_rotated(viewport, self.rotation)
