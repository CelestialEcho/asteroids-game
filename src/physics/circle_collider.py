from src.math import Vector2


class CircleCollider:
	def __init__(self, pos: Vector2, radius: float):
		self.pos = pos
		self.radius = radius

	def intersects(self, other: "CircleCollider") -> bool:
		return self.pos.distance_to(other.pos) <= (self.radius + other.radius)


	def update(self, new_pos: Vector2):
		self.pos = new_pos
