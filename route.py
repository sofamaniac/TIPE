"""Fichier contenant le code relatif aux routes"""

from time import time
from pygame.locals import SRCALPHA

from math_alt import *
from moteur_graphique import moteur_graph as graph


class Route(graph.GraphObject):  # équivaut a une vertice d'un graphe

	def __init__(self, debut, fin, get_dir):

		self.debut = debut  # debut et fin sont des intersections
		self.fin = fin
		self.v_max = 0  # contient la vitesse maximale autorisée sur cette route
		self.longueur = get_distance_obj(debut, fin)  # contient la longueur de la route
		self.get_dir = get_dir  # permet d'avoir des routes qui ne soient pas des lignes droites
		self.prio = 0  # niveau de priorité de la route
		self.prio_max = 0  # niveau de priorité maximale à attribuer à la route (sert pour les feux tricolores)
		self.oppose = None  # route conjugée a celle-ci

		angle = get_rotation(self.debut.pos, self.fin.pos)
		image = graph.pygame.Surface((self.longueur, 50), graph.pygame.locals.SRCALPHA)
		image.fill((155, 155, 155))
		pos = [min(self.debut.pos[0], self.fin.pos[0]), min(self.debut.pos[1], self.fin.pos[1])]  # coin supérieur
		# gauche de l'image

		graph.GraphObject.__init__(self, image, pos, mode="corner")
		self.rotate(angle)

	def get_direction(self, pos):  # permet d'avoir des routes parfaitement courbes
		return self.get_dir(pos)


class Intersection:  # équivaut à un noeud d'un graphe
	def __init__(self, pos):
		self.pos = pos
		self.voisins = []  # contient une liste des nodes auxquelles est connectée l'intersection
		self.connection = {}  # couples {intersection: route} pour connaitres les connections entre inersections
		self.max_prio = 0  # correspond à la priorité maximale de toutes les routes connectées à l'intersection


class Feux:

	def __init__(self):

		self.intersection = None
		self.sequences = [[], []]  # [ [ max_prio_sequence, [routes] ], ...]
		self.coeff = [10, 10]  # le temps en secondes de vert pour chaque sequence est coeff[0] * max_prio + coeff[1]
		self.last_activation = 0  # heure du dernier changement d'état
		self.index_sequence = 0  # contient l'indice de la séquence courante

	def update(self):

		t = time()

		if t - self.last_activation > self.coeff[0] * self.sequences[self.index_sequence][0] + self.coeff[1]:

			self.last_activation = t
			print(self.index_sequence)
			# le feu passe au rouge sur les routes concernées
			for route in self.sequences[self.index_sequence][1]:
				route.prio = -1

			self.index_sequence += 1
			self.index_sequence %= len(self.sequences)

			# le feu passe au vert sur les routes concernées
			for route in self.sequences[self.index_sequence][1]:
				route.prio = route.prio_max
