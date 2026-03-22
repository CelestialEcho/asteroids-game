import pygame
from src.object_class.base_object import BaseObject


class ObjectManager:
	def __init__(self, viewport: pygame.Surface):
		self.viewport = viewport
		self._objects: list[BaseObject] = []
		self._pending_add: list[BaseObject] = []


	def register_object(self, obj: BaseObject):
		self._pending_add.append(obj)


	def _flush_pending(self):
		self._objects.extend(self._pending_add)
		self._pending_add.clear()



	def update(self, dt: float):
		self._flush_pending()
		for obj in self._objects:
			obj.update(dt)
		self._objects = [o for o in self._objects if o.alive]

	def draw(self):
		for obj in self._objects:
			obj.draw(self.viewport)


# 		TODO
	def get_all(self) -> list[BaseObject]:
		return self._objects

	def get_by_id(self, object_id: int) -> list[BaseObject]:
		return [o for o in self._objects if o.object_id == object_id]
# ---