"""Fichier contenant le code relatif aux pilotes humains"""
from copy import copy

def dijkstra(debut, fin, world):
	"""Implémentation de l'algorithme de djikstra avec world la liste des intersections"""

	unvisited = copy(world)
	current = debut