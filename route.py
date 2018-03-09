"""Fichier contenant le code relatif aux routes"""

from pygame.locals import SRCALPHA

from math_alt import *
from moteur_graphique import moteur_graph as graph


class Route(graph.GraphObject):  # équivaut a une vertice d'un graphe

	def __init__(self, debut, fin, get_dir):

		self.debut = debut  # debut et fin sont des intersections
		self.fin = fin
		self.v_max = 0  # contient la vitesse maximale autorisée sur cette route
		self.longueur = get_distance(debut, fin)  # contient la longueur de la route
		self.get_dir = get_dir  # permet d'avoir des routes qui ne soient pas des lignes droites

		angle = get_rotation(self.debut.pos, self.fin.pos)
		image = graph.pygame.Surface((self.longueur, 50), graph.pygame.locals.SRCALPHA)
		image.fill((155, 155, 155))
		pos = [min(self.debut.pos[0], self.fin.pos[0]), min(self.debut.pos[1], self.fin.pos[1])]  # coin supérieur
		# gauche de l'image

		graph.GraphObject.__init__(self, image, pos)
		self.rotate(angle)

	def get_direction(self, pos):  # permet d'avoir des routes parfaitement courbes
		return self.get_dir(pos)


class Intersection:  # équivaut à un noeud d'un graphe
	def __init__(self, pos):
		self.pos = pos
		self.voisins = []  # contient une liste des nodes auxquelles est connectée l'intersection
		self.connection = {}  # couples {intersection: route} pour connaitres les connections entre inersections