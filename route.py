"""Fichier contenant le code relatif aux routes"""

from math import sqrt
from pilote import get_distance


class Route:  # équivaut a une vertice d'un graphe

	def __init__(self, debut, fin, get_dir):

		self.debut = debut  # debut et fin sont des intersections
		self.fin = fin
		self.v_max = 0  # contient la vitesse maximale autorisée sur cette route
		self.longueur = get_distance(debut, fin)  # contient la longueur de la route
		self.get_dir = get_dir

	def get_direction(self, pos):  # permet d'avoir des routes parfaitement courbes
		return self.get_dir(pos)


class Intersection:  # équivaut à un noeud d'un graphe
	def __init__(self):

		self.pos = []
		self.voisins = []