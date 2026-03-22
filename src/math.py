import math


class Vector2:
	def __init__(self, x: float = 0.0, y: float = 0.0):
		self.x = float(x)
		self.y = float(y)


	def length(self) -> float:
		return math.sqrt(self.x**2 + self.y**2)


	def normalize(self) -> "Vector2":
		l = self.length()
		if l == 0:
			return Vector2(0, 0)
		return Vector2(self.x / l, self.y / l)


	def distance_to(self, other: "Vector2") -> float:
		return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)
	
#	TODO: implement
	def rotate(self, degrees: float) -> "Vector2":
		rad = math.radians(degrees)
		cos_a = math.cos(rad)
		sin_a = math.sin(rad)
		return Vector2(self.x * cos_a - self.y * sin_a, self.x * sin_a + self.y * cos_a)

	def angle_degrees(self) -> float:
		return math.degrees(math.atan2(self.y, self.x))


	def __add__(self, other: "Vector2") -> "Vector2":
		return Vector2(self.x + other.x, self.y + other.y)


	def __sub__(self, other: "Vector2") -> "Vector2":
		return Vector2(self.x - other.x, self.y - other.y)

	def __mul__(self, scalar: float) -> "Vector2":
		return Vector2(self.x * scalar, self.y * scalar)


	def __neg__(self) -> "Vector2":
		return Vector2(-self.x, -self.y)

	def __repr__(self) -> str:
		return f"Vector2({self.x:.2f}, {self.y:.2f})"

	def lerp(self, other: "Vector2", t: float) -> "Vector2":
		return Vector2(self.x + (other.x - self.x) * t, self.y + (other.y - self.y) * t)
