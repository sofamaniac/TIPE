"""Fichier principal du programme"""

from time import sleep
from math import cos, sin
import pygame
from pygame.locals import *
from voiture import *


pygame.init()
fenetre = pygame.display.set_mode((700, 400))

continuer = True
rot = 90
voiture = Voiture(pos=[300, 200])
voiture.vitesse = 0

while continuer:

	for event in pygame.event.get():
		if event.type == QUIT:
			continuer = False

	fenetre.fill((0, 0, 0))
	voiture.update()
	voiture.show(fenetre)
	pygame.display.update()

	sleep(1/60)
	rot += 0.05
	voiture.set_dir([cos(rot), sin(rot)])

pygame.quit()