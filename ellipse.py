"""Fichier test pour les routes courbes"""

from math_alt import *


def find_ellipse(A, P, M):
	"""Retourne une fonction permettant de connaitre le vecteur tangent unitaire à l'ellipse passant par les points
	A, P et M sachant que [AP] correspond au grand axe de l'ellipse"""

	# Coordonnées du centre
	x0 = (A[0] + P[0]) / 2
	y0 = (A[1] + P[1]) / 2

	# "Rayon" de l'ellipse
	r = get_distance_list([x0, y0], A)

	# Angle du grand axe par rapport à l'axe des abscisses
	phi = get_rotation(P, A)

	# Rotation et translation du point M
	# on utilise la matrice de rotation
	# [ cos(phi) -sin(phi)]
	# [ sin(phi)  cos(phi)]
	M2 = transform(M, [x0, y0], phi)

	# Angle du point M par rapport au grand axe
	theta = acos(M2[0] / r)

	# Définition des constantes pour la fonction
	a = M2[0] / cos(theta)
	b = M2[1] / sin(theta)

	cos_phi = cos(phi)
	sin_phi = sin(phi)

	# ellipse = lambda t: [x0 + a * cos(t) * cos(phi) - b * sin(t) * sin(phi),
	# 					   y0 + a * cos(t) * sin(phi) + b * sin(t) * cos(phi)]

	# ellipse_dt represente la dérivée en fonction de l'angle theta
	ellipse_dt = lambda t: [- a * sin(t) * cos_phi - b * cos(t) * sin_phi,
							- a * sin(t) * sin_phi + b * cos(t) * cos_phi]

	# ellipse_dxy represent la dérivée en fonction de la position sur l'ellipse
	ellipse_dxy = lambda pos: normalize(ellipse_dt(acos(transform(pos, [x0, y0], phi)[0] / r)))
	return ellipse_dxy
