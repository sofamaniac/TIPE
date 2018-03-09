"""Fichier contenant le code relatif aux voitures"""

from math_alt import *
from moteur_graphique import moteur_graph as graph


class Voiture(graph.GraphObject):

	def __init__(self, pos=[0, 0]):

		self.vitesse = 0
		self.acceleration = 0

		# vecteur direction que suit la voiture initialement la voiture est à l'horizontale
		self._direction = [1, 0]  # assimilable à un vecteur de changement de base

		self.angle = 0  # angle de la voiture par rapport à l'axe des abscisses

		# ======CREATION DE L'IMAGE DE LA VOITURE====== #

		length = 30
		height = 15

		image = graph.pygame.Surface((length, height), graph.pygame.locals.SRCALPHA)

		image_1 = graph.pygame.Surface((int(3/4 * length), height))
		image_2 = graph.pygame.Surface((length - (3/4 * length), height))

		image_1.fill((155, 155, 155))
		image_2.fill((200, 200, 200))
		image.blit(image_1, (0, 0))
		image.blit(image_2, (15, 0))

		graph.GraphObject.__init__(self, image, pos)

	def update(self):
		"""Fonction mettant à jour la position et la vitesse de la voiture"""
		self.vitesse += self.acceleration

		v_x = self.vitesse * self._direction[0]
		v_y = self.vitesse * self._direction[1]

		self.pos[0] += v_x
		self.pos[1] += v_y

	def accelerer(self, da):
		self.acceleration += da

	def get_dir(self):
		return self._direction

	def set_dir(self, new_dir):
		"""Lors du changement de direction il faut mettre à jour l'image de la voiture"""
		self._direction = new_dir
		self.angle = get_rotation(new_dir)
		self.rotate(self.angle)

	direction = property(get_dir, set_dir)