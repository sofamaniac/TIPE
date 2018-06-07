"""Fichier contenant le code nécessaire pour conduire les voitures"""

from voiture import *


class Pilote:
	def __init__(self, voiture, arrivee, fenetre):

		self.voiture = voiture
		self.pos = voiture.pos
		self.direction = voiture.direction
		self.arrivee = arrivee  # là où souhaite se rendre le pilote
		self.chemin = []  # contient les intersections que doit suivre la voiture pour arriver à destination
		self.current_road = None  # contient la route sur laquelle se trouve le véhicule
		self.range = 200  # champs de vision
		self.delta_v = 0  # les pilotes ralentissent pour prendre les virages, varie entre 0 et 1
		self.delta_v_max = 1  # les humains roulent à delat_v % de la vitesse max
		self.acceleration_max = 5  # représente l'accélération maximale en m.s-1
		self.deceleration_max = 10  # représente la décélération maximale en m.s-1
		self.distance_freinage = self.range  # distance avant laquelle le pilote ne commence à freiner
		self.fenetre = fenetre  # contient la fenetre sur laquelle est affichée la voiture
		self.intersection_proche = False

	def update(self, intersections, pilotes):
		"""Focntion mettant le pilote à jour et devant être appelée une fois par frame"""
		new_dir = 0
		old_dir = self.voiture.direction

		if self.intersection_proche and len(self.chemin):
			# permet la transition entre 2 routes
			suivante = self.chemin[1]
			new_dir = self.chemin[1].get_direction(suivante.debut.pos)

		else:
			new_dir = self.current_road.get_direction(self.pos)

		diff = get_distance_list(new_dir, old_dir)  # représente la quantité de changement de la direction

		if new_dir != self.direction:  # on ne met à jour l'image de la voiture que si nécessaire
			if self.intersection_proche:
				self.delta_v = self.delta_v_max - min(diff, 0.2)
				# on prend le min pour éviter d'avoir 0
				self.voiture.direction = self.current_road.get_direction(self.pos)
			else:
				self.voiture.direction = new_dir
				self.delta_v = self.delta_v_max - diff

		inter = self.see(intersections)
		pilote = self.see(pilotes)

		close_inter = [None, 0]
		close_pilote = [None, 0]

		if inter:
			close_inter = inter[0]

		if pilote:
			close_pilote = pilote[0]

		self.voiture.update()

		self.intersection_proche = False

		self.conduire(close_inter, close_pilote)
		self.voiture.show(self.fenetre)

	def see(self, world):
		"""Retourne une liste des pilotes et intersections se trouvant dans le champs de vision du pilote"""

		resultat = []
		range_2 = self.range ** 2

		for element in world:

			a_verifier = True

			if element == self or (isinstance(element, Pilote) and element.current_road == self.current_road.oppose):
				# on ne vérifie pas l'élément si c'est une voiture sur la route opposée
				a_verifier = False

			if a_verifier:

				distance = distance_squared_obj(self, element)  # la racine n'est calculée que si nécessaire

				if distance <= range_2:
					resultat.append([element, sqrt(distance)])

		resultat.sort(key=lambda x: x[1])  # les objets les plus proches seront les premiers dans la liste

		return resultat

	def conduire(self, inter, pilote):
		"""Fonction déterminant l'accélération de la voiture à chaque frame"""

		vitesse_cible = self.current_road.v_max * self.delta_v
		coeff = 1

		distance_freinage = max(10, 5/9 * self.voiture.vitesse * 5)   # wikipédia : Distance de sécurité en France
		if pilote[0] and pilote[1] < distance_freinage:

			# ====== On vérifie que la voiture se trouve devant la notre ===== #

			# on projette les coordonées du pilotes par rapport à la voiture et à sa direction

			angle = angle_between(self.voiture.direction)
			new_point = transform(pilote[0].pos, self.pos, angle)

			if new_point[1] >= 0:  # le pilote est visible

				if self.current_road == pilote[0].current_road:
					coeff = pilote[1] / distance_freinage

				elif len(self.chemin) > 1 and self.chemin[1] == pilote[0].current_road:
						if inter[1] <= distance_freinage and inter[0] == self.current_road.fin:
							coeff = pilote[1] / distance_freinage

			# ================================================================ #

			if inter[0] != self.current_road.debut and inter[0] == pilote[0].current_road.fin:
				# on laisse passer les voitures prioritaires
				if self.current_road.prio < pilote[0].current_road.prio:
					coeff = 0
					self.voiture.stop = True

		if inter[0] and inter[1] < distance_freinage and inter[0] == self.current_road.fin:
			self.intersection_proche = True
			if inter[0].max_prio > self.current_road.prio:
				# on ne ralentit que lorsque l'on est pas prioritaire
				coeff = inter[1] / distance_freinage
				coeff = mappage(coeff, [0, 1], [0.1, 1])

			# on s'arrete au feu rouge
			if self.current_road.prio < 0 and inter[1] < 0.5:
				coeff = 0
				self.voiture.stop = True

			if self.current_road.prio >= 0 and inter[1] < 1:  # todo: affiner le virage

				if len(self.chemin) > 1:
					self.chemin.append(self.chemin.pop(0))
					self.current_road = self.chemin[0]
					self.voiture.pos = self.current_road.debut.pos[:]
					self.pos = self.voiture.pos

				else:
					return  # todo: gérer supression de l'objet ou sa remise a zero

		if coeff < 0.1:
			coeff = 0
			self.voiture.stop = True

		if self.voiture.stop:
			self.voiture.vitesse = 0

		if self.voiture.stop and inter[0] == self.current_road.fin and inter[1] <= 1 and self.current_road.prio < 0:
			#  évite de dépasser l'intersection et de sortir de la route aux feux
			self.voiture.vitesse = 0
			# if pilote[1] > 4:
			# 	# évite de superposer les voitures aux intersections
			# 	self.pos = inter[0].pos[:]

		vitesse_cible *= coeff

		if self.voiture.vitesse != vitesse_cible:

			sens_acc = signe(vitesse_cible - self.voiture.vitesse)  # faut il accélérer ou freiner
			acceleration = abs(vitesse_cible - self.voiture.vitesse)

			if sens_acc > 0:  # il faut accélérer
				acceleration = min(self.acceleration_max, acceleration)  # la voiture est limité physiquement

			else:  # il faut freiner
				acceleration = -min(self.deceleration_max, acceleration)  # idem

			self.voiture.accelerer(acceleration)
