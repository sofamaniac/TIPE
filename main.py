"""Fichier principal du programme, pour l'instant c'est surtout un fichier de test"""

from time import sleep

import pygame
from pygame.locals import *

from voiture import *
from pilote import *

from ellipse import *


pygame.init()
fenetre = pygame.display.set_mode((700, 400))

continuer = True
voiture = Voiture(pos=[0, 100])
voiture.vitesse = 0

debut = Intersection([0, 100])
A = [400, 50]
fin = Intersection([600, 500])

fin_2 = Intersection([500, 400])

length = get_distance_obj(debut, fin)

pente_x = (fin.pos[0] - debut.pos[0]) / get_distance_obj(debut, fin)
pente_y = (fin.pos[1] - debut.pos[1]) / get_distance_obj(debut, fin)

pente_x_2 = (debut.pos[0] - fin.pos[0]) / get_distance_obj(fin, debut)
pente_y_2 = (debut.pos[1] - fin.pos[1]) / get_distance_obj(fin, debut)

direction = lambda pos: [pente_x, pente_y]
direction_2 = lambda pos: [pente_x_2, pente_y_2]
direction_ellipse = find_ellipse(debut.pos, fin.pos, A)

route = Route(debut, fin, direction_ellipse)
route.v_max = 100

route2 = Route(fin, debut, direction_2)
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
