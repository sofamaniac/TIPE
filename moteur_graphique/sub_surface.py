"""Fichier contenant les fonctions nécessaires à la subdivision des surfaces pygame"""

import pygame


def subdivide(parent, rect):
	"""return a subsurface"""
	return parent.subsurface(rect)


def subdivisions(parent, cols, rows):
	"""return a list of subsurface"""

	subsurfaces = []

	xoff = parent.get_width() / cols
	yoff = parent.get_height() / rows

	x = 0
	y = 0

	for j in range(rows):
		for i in range(cols):
			rect = pygame.Rect(x, y, xoff, yoff)
			subsurfaces.append(subdivide(parent, rect))
			x += xoff
		y += yoff
		x = 0

	return subsurfaces
