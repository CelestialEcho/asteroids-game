from src.mgrs.object_manager import ObjectManager
from src.mgrs.collision_manager import CollisionManager
from src.mgrs.asteroid_spawner import AsteroidSpawner
from src.object_class.player import Player
from src.object_class.bullet import Bullet
from src.math import Vector2

import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()
FPS = 60

BLACK = (23, 23, 23)
WHITE = (255, 255, 255)
RED = (220, 60, 60)
GRAY = (140, 140, 140)
DARK_GRAY = (50, 50, 50)

font_big = pygame.font.SysFont(None, 72)
font_med = pygame.font.SysFont(None, 40)
font_small = pygame.font.SysFont(None, 30)


def new_game():
	om = ObjectManager(viewport=screen)
	pl = Player(pos=Vector2(WIDTH // 2, HEIGHT // 2))
	cm = CollisionManager(object_manager=om, player=pl)
	sp = AsteroidSpawner(
		object_manager=om, screen_w=WIDTH, screen_h=HEIGHT, max_asteroids=8
	)
	om.register_object(pl)
	sp.spawn_initial()
	return om, pl, cm, sp


object_manager, player, collision_manager, asteroid_spawner = new_game()


def draw_hud():
	score_surf = font_med.render(f"Score: {player.score}", True, WHITE)
	screen.blit(score_surf, (16, 12))

	for i in range(player.lives):
		pygame.draw.circle(screen, WHITE, (16 + i * 28, 60), 8, 2)


def draw_game_over():
	overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
	overlay.fill((0, 0, 0, 160))
	screen.blit(overlay, (0, 0))

	go_surf = font_big.render("GAME OVER", True, RED)
	sc_surf = font_med.render(f"Score: {player.score}", True, WHITE)
	re_surf = font_med.render("Press R to restart", True, GRAY)

	screen.blit(go_surf, go_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))) # TODO: fix 
	screen.blit(sc_surf, sc_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))) # TODO: fix 
	screen.blit(re_surf, re_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))) # TODO: fix 


running = True
game_over = False


while running:
	dt = clock.tick(FPS) / 1000.0
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r and game_over:
				object_manager, player, collision_manager, asteroid_spawner = (new_game())
				game_over = False


		if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
			if event.button == 1 and player.can_shoot():
				mx, my = pygame.mouse.get_pos()
				direction = (Vector2(mx, my) - player.pos).normalize()
				object_manager.register_object(Bullet(player.pos, direction))
				player.on_shoot()


	if not game_over:
		object_manager.update(dt)
		collision_manager.run()
		asteroid_spawner.update(dt)
		
		if player.lives <= 0:
			game_over = True

	screen.fill(BLACK)
	object_manager.draw()
	draw_hud()


	if game_over:
		draw_game_over()

	pygame.display.flip()

pygame.quit()
sys.exit()
