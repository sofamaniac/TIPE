"""Fichier principal du programme, pour l'instant c'est surtout un fichier de test"""

from time import sleep

import pygame
from pygame.locals import *

from pilote import *
from route import *

from ellipse import *
from math_alt import *


pygame.init()
fenetre = pygame.display.set_mode((700, 600))

continuer = True
voiture = Voiture(pos=[0, 10])
voiture.vitesse = 0

voiture2 = Voiture(pos=[60, 50])
voiture2.vitesse = 0

debut = Intersection([0, 10])
A = [40, 5]
fin = Intersection([60, 50])


length = get_distance_obj(debut, fin)

pente_x = (fin.pos[0] - debut.pos[0]) / get_distance_obj(debut, fin)
pente_y = (fin.pos[1] - debut.pos[1]) / get_distance_obj(debut, fin)

pente_x_2 = (debut.pos[0] - fin.pos[0]) / get_distance_obj(fin, debut)
pente_y_2 = (debut.pos[1] - fin.pos[1]) / get_distance_obj(fin, debut)

direction = lambda pos: [pente_x, pente_y]
direction_2 = lambda pos: [pente_x_2, pente_y_2]
direction_ellipse = find_ellipse(debut.pos, fin.pos, A)

kmh = 1 / 3.6  # 1 kmh en m.s-1

route = Route(debut, fin, direction_ellipse)
route.v_max = 50 * kmh

route2 = Route(fin, debut, direction_2)
route2.v_max = 50 * kmh

pilote = Pilote(voiture, fin, fenetre)
pilote.chemin = [route, route2]
pilote.current_road = pilote.chemin[0]

pilote2 = Pilote(voiture2, debut, fenetre)
pilote2.chemin = [route2, route]
pilote2.current_road = pilote2.chemin[0]
pilote2.delta_v_max = 1.2

route.prio = 2
debut.max_prio = 2
fin.max_prio = 2
intersections = [debut, fin]
pilotes = [pilote, pilote2]
pause = False

feu = Feux()
feu.intersection = fin
feu.sequences = [[0, [route]], [0, [route2]]]

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

	pilote.update(intersections, pilotes)
	pilote2.update(intersections, pilotes)

	pygame.display.update()
	feu.update()

	sleep(1 / framerate)

pygame.quit()
