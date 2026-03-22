import pygame
from src.object_class.base_object import BaseObject
from src.physics.circle_collider import CircleCollider
from src.math import Vector2

BULLET_SPEED = 500
BULLET_LIFETIME = 2.0


class Bullet(BaseObject):
	def __init__(self, pos: Vector2, direction: Vector2):
		texture = pygame.image.load("assets/bullet.png").convert_alpha()
		hitbox = CircleCollider(Vector2(pos.x, pos.y), 4)
		super().__init__(pos=Vector2(pos.x, pos.y), velocity=direction * BULLET_SPEED, 	rotation=0.0,
						 hitbox=hitbox, 			texture=texture, 					object_id=BaseObject.ID_BULLET)
		
		self._lifetime = BULLET_LIFETIME

	def update(self, dt: float):
		self._lifetime -= dt

		if self._lifetime <= 0:
			self.alive = False
			return

		self.pos += self.velocity * dt
		self.hitbox.update(self.pos)


	def draw(self, viewport: pygame.Surface):
		self._blit_rotated(viewport)
