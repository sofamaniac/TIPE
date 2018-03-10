"""Fichier contenant le code nécessaire pour conduire les voitures"""

from math_alt import *

from route import *


class Pilote:
	def __init__(self, voiture, arrivee, fenetre):

		self.voiture = voiture
		self.pos = voiture.pos  # c'est une référence donc pas besoin de la modifier
		self.direction = voiture.direction  # direction que doit suivre le pilote et c'est aussi une référence
		self.arrivee = arrivee  # là où souhaite se rendre le pilote
		self.chemin = []  # contient les intersections que doit suivre la voiture pour arriver à destination
		self.current_road = None  # contient la route sur laquelle se trouve le véhicule
		self.range = 15  # champs de vision
		self.delta_v = 0  # les pilotes ralentissent pour prendre les virages, varie entre 0 et 1
		self.acceleration_max = 100  # représente l'accélération maximale en m.s-1 (valeur moyenne sur Internet)
		self.deceleration_max = 200
		self.fenetre = fenetre  # contient la fenetre sur laquelle est affichée la voiture

	def update(self):

		new_dir = self.current_road.get_direction(self.pos)
		old_dir = self.voiture.direction

		diff = get_distance_list(new_dir, old_dir)  # représente la quantité de changement de la direction
		self.delta_v = 1 - 0.9999 * diff  # on multiplie par 0.9 pour éviter d'avoir 0

		if new_dir != self.direction:  # on ne met à jour l'image de la voiture que si nécessaire
			self.voiture.direction = new_dir  # on est donc obliger de modifier voiture.direction plutot que
		# self.direction

		self.voiture.update()
		self.voiture.show(self.fenetre)

	def see(self, world):
		"""Retourne une liste des voitures et intersections se trouvant dans le champs de vision du pilote"""
		resultat = []

		for element in world:
			distance = get_distance_obj(self, element)
			if distance <= self.range:
				resultat.append([element, distance])
		resultat.sort(key=lambda x: x[1])  # les objets les plus proches seront les premiers dans la liste
		return resultat

	def accelerer(self, world):

		obstacles = self.see(world)
		vitesse_cible = self.current_road.v_max * self.delta_v

		if isinstance(obstacles, list) and len(obstacles):

			close = obstacles[0]  # on ne garde que l'obstacle le plus proche

			if isinstance(close[0], Intersection):
				x = close[1] / self.range
				x = mappage(x, [0, 1], [0.2, 1])
				vitesse_cible = self.current_road.v_max * x

		if self.voiture.vitesse != vitesse_cible:
			sens_acc = signe(vitesse_cible - self.voiture.vitesse)  # faut il accélérer ou freiner
			acceleration = abs(vitesse_cible - self.voiture.vitesse)
			if sens_acc > 0:  # il faut accélérer
				acceleration = min(self.acceleration_max, acceleration)
			else:  # il faut freiner
				acceleration = -min(self.deceleration_max, acceleration)
			self.voiture.accelerer(acceleration)
