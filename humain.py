"""Fichier contenant le code relatif aux pilotes humains"""

from math import inf as infinity
from random import gauss
from time import time

from pilote import *


def minimum(dico):
	"""Fonction permettant d'obtenir la node avec la plus petite distance"""

	res = []  # on créer une liste de la forme [[distance, index, node], ...]

	for element in dico.items():
		temp = element[1]
		temp.append(element[0])
		res.append(temp)

	res.sort(key=lambda x: x[0])  # on trie cette liste en se basant sur la première valeur de chaque sous liste
	return res[0][2]


def dijkstra(debut, fin, world):
	"""Implémentation de l'algorithme de djikstra avec world la liste des intersections"""

	unvisited = {}  # contient des élément de la forme {node: distance}
	prev = {debut: None}  # contient une liste chainée des chemins les plus courts pour toutes les nodes visitées

	index = 0

	# ====== CREATION DE UNVISITED ====== #

	for inter in world:
		if inter == debut:
			unvisited.update(inter=[0, -1])
		else:
			unvisited.update(inter=[infinity, index])
		index += 1

	# ====== ALGORITHME DE DJIKSTRA ====== #

	while len(unvisited) > 0:

		current = minimum(unvisited)
		key = unvisited.keys()

		if current == fin:
			break

		for voisin in current.voisins:
			if voisin in key:
				# on ne peut faire l'algorithme que si le voisin n'a pas été visitée
				dist_alt = unvisited[current][0] + get_distance_obj(current, voisin)
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


class Humain(Pilote):

	def __init__(self, voiture, debut, arrivee, world, fenetre):

		self.temps_react = 0.1  # temps de réaction de l'humain
		self.detected = {}  # {objet: heure [détection, distance]}

		Pilote.__init__(self, voiture, arrivee, fenetre)

		self.chemin = dijkstra(debut, arrivee, world)  # les humains suivent toujours le chemin le plus court
		self.delta_v_max = gauss(1, 0.3)  # les humains roulent delat_v % de la vitesse max
		self.distance_freinage = self.range * 1 / 2  # les humains freinent très tardivement

	def conduire(self, world):

		seen = self.see(world)  # liste des objets dans le champ de vision de l'humain ansi que leur distance

		keys = self.detected.keys()

		t = time()

		for index in range(len(seen)):
			obstacle = seen[index]
			if obstacle[0] in keys:
				# on met à jour la distance de l'objet dans le dictionnaire
				self.detected[obstacle[0]][1] = seen[0]
			else:
				# on ajoute l'obstacle dans le dictionnaire
				self.detected.update({obstacle[0]: t})

		seen_keys = [obstacle[0] for obstacle in seen]
		for key in keys:
			if key not in seen_keys:
				del self.detected[key]

		closest = None

		while len(seen) and not closest:
			if isinstance(seen[0][0], Intersection):
				closest = seen[0]
			else:
				other_road = seen[0][0].current_road
				if other_road.fin != self.current_road.debut and other_road.debut != self.current_road.fin:
					# on ne considère pas les voitures sur la même route mais dans l'autre sens
					closest = seen[0]
				else:
					seen.pop(0)

		if closest and t > self.detected[closest] + self.temps_react:
			Pilote.conduire(self, closest)
