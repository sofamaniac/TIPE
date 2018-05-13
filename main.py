"""Fichier principal du programme, pour l'instant c'est surtout un fichier de test"""

from time import sleep

import pygame
from pygame.locals import *

from voiture import *
from pilote import *

from ellipse import *
from math_alt import *


pygame.init()
fenetre = pygame.display.set_mode((700, 600))

continuer = True
voiture = Voiture(pos=[0, 100])
voiture.vitesse = 0

voiture2 = Voiture(pos=[600, 500])
voiture2.vitesse = 0

debut = Intersection([0, 100])
A = [400, 50]
fin = Intersection([600, 500])


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
pilote.chemin = [route, route2]
pilote.current_road = pilote.chemin[0]

pilote2 = Pilote(voiture2, debut, fenetre)
pilote2.chemin = [route2, route]
pilote2.current_road = pilote2.chemin[0]
pilote2.delta_v_max = 1.2

route.prio = 0
intersections = [debut, fin]
pilotes = [pilote, pilote2]
pause = False

while continuer:

	for event in pygame.event.get():
		if event.type == QUIT:
			continuer = False
		elif event.type == KEYDOWN:
			if event.key == K_SPACE:
				pause = True

	while pause:
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					pause = False

	fenetre.fill((0, 0, 0))

	route.show(fenetre)
	route2.show(fenetre)

	pilote.update(intersections, pilotes)
	pilote2.update(intersections, pilotes)

	print(get_distance_obj(pilote, pilote2))

	pygame.display.update()

	sleep(1/60)

pygame.quit()
