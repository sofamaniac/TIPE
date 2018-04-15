"""Fichier principal du programme"""

from time import sleep

import pygame
from pygame.locals import *

from voiture import *
from pilote import *

from math import cos, sin, sqrt, acos


pygame.init()
fenetre = pygame.display.set_mode((700, 400))

continuer = True
voiture = Voiture(pos=[0, 100])
voiture.vitesse = 0

debut = Intersection([0, 100])
fin = Intersection([600, 100])

fin_2 = Intersection([500, 400])

length = get_distance_obj(debut, fin)

pente_x = (fin.pos[0] - debut.pos[0]) / get_distance_obj(debut, fin)
pente_y = (fin.pos[1] - debut.pos[1]) / get_distance_obj(debut, fin)

pente_x_2 = (fin_2.pos[0] - fin.pos[0]) / get_distance_obj(fin, fin_2)
pente_y_2 = (fin_2.pos[1] - fin.pos[1]) / get_distance_obj(fin, fin_2)

direction = lambda pos: [pente_x, pente_y]
direction_2 = lambda pos: [pente_x_2, pente_y_2]

route = Route(debut, fin, direction)  # ligne droite
route.v_max = 100

route2 = Route(fin, fin_2, direction_2)
route2.v_max = 100

pilote = Pilote(voiture, fin, fenetre)
pilote.current_road = route
pilote.chemin = [route, route2]

world = [debut, fin]

while continuer:

	for event in pygame.event.get():
		if event.type == QUIT:
			continuer = False

	fenetre.fill((0, 0, 0))
	route.show(fenetre)
	route2.show(fenetre)
	pilote.update()
	pilote.accelerer(world)
	pygame.display.update()

	sleep(1/60)

pygame.quit()