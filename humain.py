"""Fichier contenant le code relatif aux pilotes humains"""

from copy import copy
from math import inf as infinity
from pilote import get_distance


def dijkstra(debut, fin, world):
	"""Implémentation de l'algorithme de djikstra avec world la liste des intersections"""

	unvisited = {}
	prev = {debut: None}  # contient une liste chainée des chemins les plus courts pour toutes les nodes visitées

	index = 0

	for inter in world:
		if inter == debut:
			unvisited.update(inter=[0, -1])
		else:
			unvisited.update(inter=[infinity, index])
		index += 1

	while len(unvisited) > 0:

		current = min(unvisited, key=unvisited.get)
		key = unvisited.keys()

		if current == fin:
			break

		for voisin in current.voisins:
			if voisin in key:
				# on ne peut faire l'algorithme que si le voisin n'a pas été visitée
				dist_alt = unvisited[current][0] + get_distance(current, voisin)
				if dist_alt < unvisited[voisin][0]:
					unvisited[voisin][0] = dist_alt
					prev.update(voisin=current)
		del unvisited[current]  # une fois la node visitée on ne la viste plus

	# ====== RECONSTRUCTION DU CHEMIN VERS LA CIBLE ====== #

	path = []
	node = fin
	while prev[node]:
		path.append(node)
		node = prev[node]

	return path  # le chemin est à l'envers
