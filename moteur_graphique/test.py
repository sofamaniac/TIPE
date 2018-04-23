"""Fichier test"""

from time import sleep

from pygame.locals import *

from entity import *
from sub_surface import *


def create_animations(path, cols, rows, pos):
	right_image = pygame.image.load(path).convert_alpha()

	right_sprites = subdivisions(right_image, cols, rows)

	return AnimatedObject(right_sprites, pos)


class Player:
	def __init__(self, screen):

		self.pos = [0, 240]

		self.right = False
		self.left = False
		self.crouch = False

		self.current_statut = "idle"
		self.orientation = "r"

		run_animations = create_animations("sprites/player/john_run.png", 10, 1, self.pos)
		jump_animations = create_animations("sprites/player/john_jump.png", 9, 1, self.pos)
		idle_animations = create_animations("sprites/player/john_idle.png", 5, 1, self.pos)
		crouch_animations = create_animations("sprites/player/john_crouch.png", 2, 1, self.pos)

		self.animations = {"run": run_animations,
						   "jump": jump_animations,
						   "crouch": crouch_animations,
						   "idle": idle_animations}

		self.animations["crouch"].frames = self.animations["crouch"].frames[1:]  # on vire une frame en trop

		for key in self.animations.keys():
			self.animations[key].surface = screen

	def move(self, dx, dy):

		self.pos = [self.pos[0] + dx, self.pos[1] + dy]
		for animation in self.animations.items():
			animation[1].move(dx, dy)

	def update(self):

		self.current_statut = "idle"
		if self.right:
			self.current_statut = "run"
			self.orientation = "r"
			if not self.crouch:
				self.move(2, 0)
		if self.left:
			self.current_statut = "run"
			self.orientation = "l"
			if not self.crouch:
				self.move(-2, 0)
		if self.crouch:
			self.current_statut = "crouch"

		for statuts in self.animations.keys():

			if self.current_statut == statuts:
				self.animations[statuts].update()

			else:
				self.animations[statuts].current_index = 0

	def show(self, screen):

		animation = self.animations[self.current_statut]
		frame = animation.frames[animation.current_index].copy()
		if self.orientation == "l":
			frame = pygame.transform.flip(frame, True, False)
		screen.blit(frame, self.pos)


pygame.init()

screen = pygame.display.set_mode((680, 480))

image = pygame.Surface((50, 50))
image_2 = pygame.Surface((50, 50))

image.fill((255, 0, 0))
image_2.fill((0, 255, 0))

text = TextHandler("test", 24, "Courrier", [100, 100])

obj_test = AnimatedObject([image, image_2], [0, 0])

explosion_image = pygame.image.load("sprites/explosion/explosion 3.png").convert_alpha()
explosion_sprites = subdivisions(explosion_image, 8, 8)

explosion = AnimatedObject(explosion_sprites, [0, 0], duration=1, surface=screen)

player = Player(screen)

while True:

	for event in pygame.event.get():

		if event.type == QUIT:
			exit(0)

		if event.type == KEYDOWN:

			if event.key == K_RIGHT:
				player.right = True

			if event.key == K_LEFT:
				player.left = True

			if event.key == K_UP:
				obj_test.move(0, -5)

			if event.key == K_DOWN:
				player.crouch = True

		elif event.type == KEYUP:

			if event.key == K_RIGHT:
				player.right = False

			if event.key == K_LEFT:
				player.left = False

			if event.key == K_UP:
				obj_test.move(0, 5)

			if event.key == K_DOWN:
				player.crouch = False

	screen.fill((120, 120, 120))
	obj_test.update()
	explosion.update()
	player.update()

	if obj_test.is_overlapping(text):
		obj_test.current_index = 1

	obj_test.show(screen)

	text.show(screen)

	explosion.show(screen)

	player.show(screen)

	pygame.display.flip()

	sleep(1 / 60)
