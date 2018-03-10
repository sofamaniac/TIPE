"""Fichier contenant les fonction mathémétiques nécessaires au programme"""

from math import *


def get_distance_obj(a, b):
	"""Retourne la distance entre deux objets possédant un attribut pos"""
	return sqrt(pow(a.pos[0] - b.pos[0], 2) + pow(a.pos[1] - b.pos[1], 2))


def get_distance_list(a, b):
	"""Retourne la distance entre deux points"""
	return sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))


def signe(a):
	"""Retourne le signe de a"""
	if a >= 0:
		return 1
	else:
		return -1


def get_rotation(coords_a, coords_b=(0, 0)):
	"""Retourne l'angle oritenté en degré du segment ab par rapport à l'horizontale, un segment de longueur nulle à
	un angle orienté de 0 degrés"""

	dx = coords_b[0] - coords_a[0]
	dy = coords_b[1] - coords_a[1]

	l = get_distance_list(coords_a, coords_b)  # longueur du segment

	if l != 0:

		c = dx / l  # cosinus de l'angle orienté
		s = dy / l  # sinus de l'angle orienté

		# Il faut inverser l'angle de rotation à cause du sens de l'axe des ordonnées
		angle = degrees(acos(c)) * signe(-s)  # permet d'avoir un angle orienté

	else:
		angle = 0

	return angle


def mappage(x, start_inter, end_inter):
	"""Map linéairement un nombre appartenant start_inter à end_inter"""

	a = start_inter[0]
	b = start_inter[1]

	c = end_inter[0]
	d = end_inter[1]

	res = (x - a) / (b - a) * (d - c) + c

	return res