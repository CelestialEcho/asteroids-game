import random
import math
from src.mgrs.object_manager import ObjectManager
from src.object_class.asteroid import Asteroid, ASTEROID_SPEED
from src.math import Vector2

SAFE_RADIUS = 200


class AsteroidSpawner:
	def __init__(
		self, 			object_manager: ObjectManager, screen_w: int,
		screen_h: int, 	max_asteroids: int = 6 ):
		
		self.object_manager = object_manager
		self.screen_w = screen_w
		self.screen_h = screen_h
		self.max_asteroids = max_asteroids
		self._spawn_timer = 0.0
		self._spawn_interval = 4.0

	def update(self, dt: float):
		self._spawn_timer += dt
		if self._spawn_timer >= self._spawn_interval:
			self._spawn_timer = 0.0
			self._maybe_spawn()

	def spawn_initial(self):
		for _ in range(self.max_asteroids):
			self._spawn_one()



#       TODO: fix 
	def _maybe_spawn(self):
		from src.object_class.base_object import BaseObject

		count = len(self.object_manager.get_by_id(BaseObject.ID_ASTEROID))
		if count < self.max_asteroids:
			self._spawn_one()


	def _spawn_one(self):
		cx, cy = self.screen_w / 2, self.screen_h / 2

		edge = random.randint(0, 3)

		if edge == 0: pos = Vector2(random.uniform(0, self.screen_w), -20)

		elif edge == 1: pos = Vector2(self.screen_w + 20, random.uniform(0, self.screen_h))

		elif edge == 2: pos = Vector2(random.uniform(0, self.screen_w), self.screen_h + 20)

		else: pos = Vector2(-20, random.uniform(0, self.screen_h))

		target = Vector2(cx + random.uniform(-150, 150), cy + random.uniform(-150, 150))
		direction = (target - pos).normalize()
		size = random.randint(3, 6)
		speed = ASTEROID_SPEED / size + random.uniform(-10, 10)
		velocity = direction * speed


		self.object_manager.register_object(Asteroid(pos, velocity, size))
