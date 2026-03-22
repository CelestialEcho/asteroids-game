from src.mgrs.object_manager import ObjectManager
from src.object_class.base_object import BaseObject
from src.object_class.asteroid import Asteroid
from src.object_class.player import Player
from typing import cast


class CollisionManager:
	def __init__(self, object_manager: ObjectManager, player: Player):
		self.object_manager = object_manager
		self.player = player


	def run(self):
		asteroids = self.object_manager.get_by_id(BaseObject.ID_ASTEROID)
		bullets = self.object_manager.get_by_id(BaseObject.ID_BULLET)


		for asteroid in asteroids:
			if not asteroid.alive: continue

			for bullet in bullets:
				if not bullet.alive: continue
				
				if asteroid.hitbox.intersects(bullet.hitbox):
					bullet.alive = False
					asteroid.alive = False
					self.player.score += cast(Asteroid, asteroid).points
					for fragment in cast(Asteroid, asteroid).split():
						self.object_manager.register_object(fragment)
					break


			if asteroid.alive and not self.player.is_invincible():
				if asteroid.hitbox.intersects(self.player.hitbox):
					self.player.on_hit()
					asteroid.alive = False
