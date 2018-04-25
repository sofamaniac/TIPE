"""Fichier contenant le code nécessaire pour conduire les voitures"""

from route import *


class Pilote:
	def __init__(self, voiture, arrivee, fenetre):

		self.voiture = voiture
		self.pos = voiture.pos  # c'est une référence donc pas besoin de la modifier
		self.direction = voiture.direction  # direction que doit suivre le pilote et c'est aussi une référence
		self.arrivee = arrivee  # là où souhaite se rendre le pilote
		self.chemin = []  # contient les intersections que doit suivre la voiture pour arriver à destination
		self.current_road = None  # contient la route sur laquelle se trouve le véhicule
		self.range = 200  # champs de vision
		self.delta_v = 0  # les pilotes ralentissent pour prendre les virages, varie entre 0 et 1
		self.delta_v_max = 1  # les humains roulent delat_v % de la vitesse max
		self.acceleration_max = 100  # représente l'accélération maximale en px.s-1
		self.deceleration_max = 200  # représente la décélération maximale en px.s-1
		self.distance_freinage = self.range  # distance avant laquelle le pilote ne commence à freiner
		self.fenetre = fenetre  # contient la fenetre sur laquelle est affichée la voiture

	def update(self):
		"""Focntion mettant le pilote à jour et devant être appelée une fois par frame"""
		new_dir = self.current_road.get_direction(self.pos)
		old_dir = self.voiture.direction

		diff = get_distance_list(new_dir, old_dir)  # représente la quantité de changement de la direction
		self.delta_v = max(self.delta_v_max - diff, 0.1)  # on prend le max pour éviter d'avoir 0

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

	def conduire(self, closest):
		"""Fonction déterminant l'accélération de la voiture à chaque frame"""
		vitesse_cible = self.current_road.v_max * self.delta_v
		# todo: modifier pour que le pilote s'arrête complètement lorsque closest est une voiture

		if closest[1] < self.distance_freinage * self.voiture.vitesse / 100 \
				and closest[0].max_prio > self.current_road.prio:
			# on ne freine que si l'obstacle est proche
			# todo: choisir la distance de freinage en fonction de la vitesse de la voiture
			x = closest[1] / self.range
			x = mappage(x, [0, 1], [0.1, 1])  # determine la force du freinage
			vitesse_cible = self.current_road.v_max * x

		if isinstance(closest[0], Intersection) and closest[1] < 16 and closest[0] == self.current_road.fin \
				and len(self.chemin) > 1:
			# on change de route quand closest[1] < à 1/2 largeur de voiture
			# todo: à affiner
			self.chemin.pop(0)
			self.current_road = self.chemin[0]

		if self.voiture.vitesse != vitesse_cible:
			sens_acc = signe(vitesse_cible - self.voiture.vitesse)  # faut il accélérer ou freiner
			acceleration = abs(vitesse_cible - self.voiture.vitesse)
			if sens_acc > 0:  # il faut accélérer
				acceleration = min(self.acceleration_max, acceleration)
				self.voiture._image.fill((0, 255, 0))
			else:  # il faut freiner
				acceleration = -min(self.deceleration_max, acceleration)
				self.voiture._image.fill((255, 0, 0))
			self.voiture.accelerer(acceleration)
