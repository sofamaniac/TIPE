"""Fichier contenant le code relatif aux voitures"""

from pygame.locals import SRCALPHA

from math_alt import *
from moteur_graphique import moteur_graph as graph


class Voiture(graph.GraphObject):

	def __init__(self, pos=(0, 0)):

		# les voitures sont condidérées comme des objets ponctuels

		if pos is None:
			pos = [0, 0]
		self.vitesse = 0
		self.acceleration = 0

		# vecteur direction que suit la voiture initialement la voiture est à l'horizontale
		self._direction = [1, 0]  # assimilable à un vecteur de changement de base

		self.angle = 0  # angle de la voiture par rapport à l'axe des abscisses

		# ======CREATION DE L'IMAGE DE LA VOITURE====== #

		length = 40  # utitlisé pour prendre en compte la longueur de la voiture dans le calcul de distance
		height = 20

		image = graph.pygame.Surface((length, height), SRCALPHA)

		image_1 = graph.pygame.Surface((int(1 / 4 * length), height), SRCALPHA)
		image_2 = graph.pygame.Surface((int(3 / 4 * length), height), SRCALPHA)

		image_1.fill((200, 200, 200))
		image_2.fill((100, 100, 100))
		image.fill((255, 255, 255))
		image.blit(image_1, (0, 0))
		image.blit(image_2, (int(1 / 4 * length), 0))

		graph.GraphObject.__init__(self, image, pos, "corner")

	def update(self):
		"""Fonction mettant à jour la position et la vitesse de la voiture"""
		self.vitesse += self.acceleration * 1 / 60  # la vitesse est passée px.s-1 sauf que l'on est en px.frame-1

		if self.vitesse < 0.01:
			self.vitesse = 0

		v_x = self.vitesse * self._direction[0]
		v_y = self.vitesse * self._direction[1]

		self.move(v_x * 1 / 60, v_y * 1 / 60)

		self.acceleration = 0  # l'accélération est remise à zéro à chaque fois

	def accelerer(self, da):
		self.acceleration += da

	def get_dir(self):
		return self._direction

	def set_dir(self, new_dir):
		"""Lors du changement de direction il faut mettre à jour l'image de la voiture"""
		self._direction = new_dir
		self.angle = angle_between(new_dir)
		self.rotate(self.angle - 90)

	def show(self, fenetre=None):

		fenetre.blit(self.image, [self.pos[0] * M, self.pos[1] * M])

	direction = property(get_dir, set_dir)
