import pygame
from src.object_class.base_object import BaseObject
from src.physics.circle_collider import CircleCollider
from src.math import Vector2

ASTEROID_SPEED = 120
ASTEROID_POINTS = 50
MIN_SIZE = 2


class Asteroid(BaseObject):
	def __init__(
		self, pos: Vector2, velocity: Vector2, size: int, hits: int = 0):
		self._base_texture = pygame.image.load("assets/asteroid.png").convert_alpha()
		self.size = size
		self.hits = hits
		self._angle = 0.0
		self._spin = 30.0 / max(size, 1)

		pixel_radius = 4 * size
		scaled = pygame.transform.scale(self._base_texture, (pixel_radius * 2, pixel_radius * 2))
		

		hitbox = CircleCollider(Vector2(pos.x, pos.y), pixel_radius * 0.8)

		super().__init__(pos=Vector2(pos.x, pos.y), velocity=velocity, rotation=0.0,
						 hitbox=hitbox, 			texture=scaled,    object_id=BaseObject.ID_ASTEROID)
		
		self.points = ASTEROID_POINTS * size


	def update(self, dt: float):
		self.pos += self.velocity * dt
		self._angle += self._spin * dt
		self._wrap_position(800, 600)
		self.hitbox.update(self.pos)


	def draw(self, viewport: pygame.Surface):
		self._blit_rotated(viewport, self._angle)


	def split(self) -> list["Asteroid"]:
		if self.size <= MIN_SIZE:
			return []
		new_size = self.size - 1
		left_vel = self.velocity.rotate(30).normalize() * (
			ASTEROID_SPEED / new_size
		)
		right_vel = self.velocity.rotate(-30).normalize() * (
			ASTEROID_SPEED / new_size
		)
		return [
			Asteroid(
				Vector2(self.pos.x, self.pos.y),  # pyright: ignore[reportAttributeAccessIssue]
				left_vel,
				new_size,
				self.hits + 1,
			),
			Asteroid(
				Vector2(self.pos.x, self.pos.y),   # pyright: ignore[reportAttributeAccessIssue]
				right_vel,
				new_size,
				self.hits + 1,
			), 
		]
