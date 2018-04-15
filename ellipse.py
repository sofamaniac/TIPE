"""Fichier test pour les routes courbes"""

from math_alt import *
import matplotlib.pyplot as plt
from numpy import linspace

A = [700, 0]
P = [-100, 100]

M = [150, -200]

# Coordonnées du centre
x0 = (A[0] + P[0]) / 2
y0 = (A[1] + P[1]) / 2

# "Rayon" de l'ellipse
r = get_distance_list([x0, y0], A)

# Angle du grand axe par rapport à l'axe des abscisses
phi = get_rotation(P, A)

# Translation du point M
x1 = M[0] - x0
y1 = M[1] - y0

# Rotation du point M
# on utilise la matrice de rotation
# [ cos(phi)  sin(phi)]
# [ -sin(phi) cos(phi)]
M2 = transform(M, [x0, y0], phi)

# Angle du point M par rapport au grand axe
theta = acos(M2[0] / r)

a = M2[0] / cos(theta)
b = M2[1] / sin(theta)

ellipse = lambda t: [x0 + a * cos(t) * cos(phi) - b * sin(t) * sin(phi),
					 y0 + a * cos(t) * sin(phi) + b * sin(t) * cos(phi)]

ellipse_xy = lambda pos: ellipse(acos(transform(pos, [x0, y0], phi)[0] / r))

bla = ellipse(theta - phi)

x = []
y = []

for t in linspace(0, pi, 2000):
	temp = ellipse(t)
	x.append(temp[0])
	y.append(temp[1])

plt.plot(x, y)
plt.plot([A[0], P[0], M[0]], [A[1], P[1], M[1]])
print(ellipse_xy(A))
plt.axis('equal')
plt.show()
