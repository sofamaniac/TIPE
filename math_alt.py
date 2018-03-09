"""Fichier contenant les fonction mathémétiques nécessaires au programme"""

from math import *


def get_distance(a, b):
	"""Retourne la distance entre deux obkets possédant un attribut pos"""
	return sqrt(pow(a.pos[0] - b.pos[0], 2) + pow(a.pos[1] - b.pos[1], 2))


def signe(a):
	"""Retourne le signe de a"""
	if a >= 0:
		return 1
	else:
		return -1


def get_rotation(coords_a, coords_b=(0, 0)):
	"""Retourne l'angle oritenté en degré du segment ab par rapport à l'horizontale"""

	dx = coords_b[0] - coords_a[0]
	dy = coords_b[1] - coords_a[1]

	l = sqrt(pow(coords_a[0] - coords_b[0], 2) + pow(coords_a[1] - coords_b[1], 2))  # longueur du segment

	c = dx / l  # cosinus de l'angle orienté
	s = dy / l  # sinus de l'angle orienté

	# Il faut inverser l'angle de rotation à cause du sens de l'axe des ordonnées
	angle = degrees(acos(c)) * signe(-s)  # permet d'avoir un angle orienté

	return angle