"""Fichier principal du programme"""

from time import sleep

import pygame
from pygame.locals import *

from voiture import *
from pilote import *


pygame.init()
fenetre = pygame.display.set_mode((700, 400))

continuer = True
rot = 90
voiture = Voiture(pos=[0, 0])
voiture.vitesse = 0

debut = Intersection([0, 0])
fin = Intersection([400, 300])

length = get_distance_obj(debut, fin)

pente_x = (fin.pos[0] - debut.pos[0]) / get_distance_obj(debut, fin)
pente_y = (fin.pos[1] - debut.pos[1]) / get_distance_obj(debut, fin)

direction = lambda pos: [pente_x, pente_y]

route = Route(debut, fin, direction)  # ligne droite
route.v_max = 100

pilote = Pilote(voiture, fin, fenetre)
pilote.current_road = route

world = [debut, fin]

while continuer:

	for event in pygame.event.get():
		if event.type == QUIT:
			continuer = False

	fenetre.fill((0, 0, 0))
	route.show(fenetre)
	pilote.update()
	pilote.accelerer(world)
	pygame.display.update()

	sleep(1/60)

pygame.quit()