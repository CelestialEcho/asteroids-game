import pygame
from src.math import Vector2
from src.physics.circle_collider import CircleCollider


class BaseObject:
	ID_ASTEROID = 0
	ID_BULLET = 1
	ID_PLAYER = 2

	def __init__(
		self, 				pos: Vector2, 			velocity: Vector2,
		rotation: float, 	hitbox: CircleCollider, texture: pygame.Surface, object_id: int = -1):

		self.pos = pos
		self.velocity = velocity
		self.rotation = rotation
		self.hitbox = hitbox
		self.texture = texture
		self.object_id = object_id
		self.alive = True

    # virtual method
	def update(self, dt: float):
		pass
    

    # virtual method
	def draw(self, viewport: pygame.Surface):
		pass


	def _wrap_position(self, screen_w: int, screen_h: int):

		if self.pos.x < 0: self.pos.x = screen_w

		if self.pos.x > screen_w: self.pos.x = 0

		if self.pos.y < 0: self.pos.y = screen_h

		if self.pos.y > screen_h: self.pos.y = 0


# TODO: complete
	def _blit_rotated(self, viewport: pygame.Surface, angle_deg: float = 0.0):
		rotated = pygame.transform.rotate(self.texture, -angle_deg)

		rect = rotated.get_rect(center=(int(self.pos.x), int(self.pos.y)))
		
		viewport.blit(rotated, rect)
