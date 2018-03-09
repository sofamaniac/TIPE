"""Fichier contenant le code nécessaire pour conduire les voitures"""

from math_alt import *


class Pilote:

	def __init__(self, voiture, arrivee):

		self.voiture = voiture
		self.pos = voiture.pos  # c'est une référence donc pas besoin de la modifier
		self.direction = voiture.direction  # direction que doit suivre le pilote et c'est aussi une référence
		self.arrivee = arrivee  # là où souhaite se rendre le pilote
		self.chemin = []  # chemin que doit suivre la voiture pour arriver à destination contient les intersections
		self.current_road = None  # contient la route sur laquelle se trouve le véhicule
		self.range = 100  # champs de vision

	def update(self):

		new_dir = self.current_road.get_direction(self.pos)

		if new_dir != self.direction:  # on ne met à jour l'image de la voiture que si nécessaire
			self.voiture.direction = new_dir

	def see(self, world):
		"""Retourne une liste des voitures et intersections se trouvant dans le champs de vision du pilote"""
		resultat = []

		for element in world:
			if get_distance(self, element) <= self.range:
				resultat.append(element)
