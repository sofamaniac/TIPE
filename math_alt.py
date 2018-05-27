"""Fichier contenant les fonction mathémétiques ainsi que les constantes nécessaires au programme"""

from math import *
import numpy as np

M = 10  # mètre de référence en pixel, valeur complètement aléatoire
framerate = 60  # nombre d'actualisation par seconde


def get_distance_obj(a, b):
	"""Retourne la distance entre deux objets possédant un attribut pos"""
	return sqrt(pow(a.pos[0] - b.pos[0], 2) + pow(a.pos[1] - b.pos[1], 2))


def distance_squared_obj(a, b):
	return pow(a.pos[0] - b.pos[0], 2) + pow(a.pos[1] - b.pos[1], 2)


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
	"""Retourne l'angle oritenté en radians du segment ab par rapport à l'horizontale, un segment de longueur nulle a
	un angle orienté de 0 radians"""

	dx = coords_b[0] - coords_a[0]
	dy = coords_b[1] - coords_a[1]

	l = get_distance_list(coords_a, coords_b)  # longueur du segment

	if l != 0:

		c = dx / l  # cosinus de l'angle orienté
		s = dy / l  # sinus de l'angle orienté

		# Il faut inverser l'angle de rotation à cause du sens de l'axe des ordonnées
		angle = acos(c) * signe(s)  # permet d'avoir un angle orienté

	else:
		angle = 0

	return angle


def angle_between(p1, p2=(0, 0), dtype="rad"):
	"""Retourne l'angle en degrés du segment formé des deux points"""
	ang1 = np.arctan2(*p1[::-1])
	ang2 = np.arctan2(*p2[::-1])

	res = ang1 - ang2

	if dtype == "rad":
		return res

	else:
		return np.rad2deg((ang1 - ang2) % (2 * np.pi))


def mappage(x, start_inter, end_inter):
	"""Map linéairement un nombre appartenant start_inter à end_inter"""

	a = start_inter[0]
	b = start_inter[1]

	c = end_inter[0]
	d = end_inter[1]

	res = (x - a) / (b - a) * (d - c) + c

	return res


def transform(pt, tr=(0, 0), rot=0):
	"""Fonction qui prend en argument un point, une translation et une rotation en radian et retourne les coordonnées
	après changement de base"""
	tr_x = pt[0] - tr[0]
	tr_y = pt[1] - tr[1]

	res_x = round(tr_x * cos(rot) + tr_y * sin(rot))
	res_y = round(tr_y * cos(rot) - tr_x * sin(rot))

	return [res_x, res_y]


def normalize(vect):
	"""Fonction retournant un vecteur unitaire colinéaire à vect"""

	norme = get_distance_list([0, 0], vect)

	res = [vect[0] / norme, vect[1] / norme]

	return res


def round(x, prec=10):
	"""Fonction retournant une valeur de x arrondi à l'inférieur avec une précision de 'prec' décimales"""
	p = pow(10, prec)
	x_int = int(x * p)
	return x_int / p
