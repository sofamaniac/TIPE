"""Fichier du moteur graphique"""

from time import time

import pygame


class GraphObject:
	"""Object which handle images"""

	def __init__(self, image, pos, mode="center"):

		self.image = image  # peut subir des rotations
		self._image = image  # version de l'image qui ne sera jamais modifiée
		self.size = self.image.get_size()  # size (length, width) of the object
		self.pos = pos  # current position of the object
		self.mode = mode  # what point self.pos refers to, can be "center" or "corner"

		if mode == "center":
			self.pos[0] = self.pos[0] - (self.size[0] / 2)
			self.pos[1] = self.pos[1] - (self.size[1] / 2)

	def move(self, dx=0, dy=0):
		"""Move the object by dx, dy"""

		self.pos[0] += dx
		self.pos[1] += dy

	def rotate(self, angle):
		"""Rotate the image of the object by the angle given in degrees"""
		self.image = pygame.transform.rotate(self._image, angle)

	def show(self, fenetre):
		"""Display the object on fenetre"""

		fenetre.blit(self.image, self.pos)

	def set_pos(self, x=0, y=0):
		"""Set position to x, y"""

		self.pos[0] = x
		self.pos[1] = y

	def is_overlapping(self, entities):

		"""If a list is given return the index of the element colliding if needed else return None,
		if entity object given return True if colliding, else return False"""

		if isinstance(entities, list):
			for entity in entities:
				if self.compare_projection(entity):
					return entities.index(entity)
			return None

		else:
			return self.compare_projection(entities)

	def compare_projection(self, entity):
		"""Use projection on both x and y axis to know if rectangle are overlapping"""

		# size and x coordonate of the object
		x_a = self.pos[0]
		lxa = self.size[0]

		# same for the object to compare with
		x_b = entity.pos[0]
		lxb = entity.size[0]

		if (x_a < x_b < x_a + lxa) or (x_b < x_a < x_b + lxb):

			y_a = self.pos[1]
			y_b = entity.pos[1]
			lya = self.size[1]
			lyb = entity.size[1]

			if (y_a < y_b < y_a + lya) or (y_b < y_a < y_b + lyb):
				return True

		return False


class AnimatedObject(GraphObject):
	"""Object animated"""

	def __init__(self, frames, pos, surface=None, duration=1):

		self.frames = frames  # list of frames
		self.current_index = 0  # index of the current frame
		self.paused = False
		self.surface = surface  # surface on wich the object is blit

		if isinstance(frames, list):

			GraphObject.__init__(self, frames[0], pos)
			self.frame_duration = duration / len(frames)

		else:
			GraphObject.__init__(self, frames, pos)
			self.frame_duration = -1

		self.last_change = time()

	def pause(self):
		"""Pause or unpause the animation"""

		if self.paused:
			self.paused = False

		else:
			self.paused = True

	def update(self):
		"""Check if the current frame must change, this function must be call regularly"""

		if self.paused:
			return

		current_time = time()

		if (current_time - self.last_change) > self.frame_duration:
			self.last_change = current_time

			self.current_index += 1
			self.current_index %= len(self.frames)

	def show(self, fenetre=None):
		"""Allows to blit the frame needed on fenetre except is self.surface is defined"""
		if self.surface:
			fenetre = self.surface
		fenetre.blit(self.frames[self.current_index], self.pos)


class AnimatedGroup:
	"""Handler for a group of AnimatedObject (Useless)"""

	def __init__(self, animations):

		self.animations = animations

	def update(self):
		"""Update all the animations of the group"""

		for animation in self.animations:
			animation.update()

	def show(self, fenetre):
		"""Blit all the animations to the window specified"""

		for animation in self.animations:
			animation.show(fenetre)

	def add(self, animation):
		"""Add an animation to the group"""

		self.animations.append(animation)


class TextHandler(GraphObject):
	"""Class to easily transform and manipulate text into surface"""

	def __init__(self, text, size, police, position, pos_mode="center", color=(255, 255, 255), italic=False, bold=False,
				 underlined=False, antialias=True, background=None):
		"""Modes for position are :
				-center : the position given is the one of the center
				-top_left : the position given is the one of the top left corner"""

		self.pos_mode = pos_mode

		self.text_attributes = {"text": text,
								"size": size,
								"police": police,
								"color": color,
								"italic": italic,
								"bold": bold,
								"underlined": underlined,
								"antialias": antialias,
								"background": background}
		self.render()

		GraphObject.__init__(self, self.image, position)

		if pos_mode == "center":
			size = self.image.get_size()

			x = position[0] - size[0] / 2
			y = position[1] - size[1] / 2

			position = [x, y]
			self.pos = position

	# self.update_hitbox()  # Je sais pas à quoi ça sert :((((((

	def get_attribute(self, key):
		"""Return the value of the specified attribute"""

		return self.text_attributes[key]

	def set_attribute(self, key, value):
		"""Set the value of the key specfied to value and re-render the surface"""

		self.text_attributes[key] = value
		self.render()

	def set_pos(self, x=0, y=0):
		"""Set the position of the surface depending on the position mode of the object"""

		if self.pos_mode == "center":
			size = self.image.get_size()

			x = self.pos[0] - size[0] / 2
			y = self.pos[1] - size[1] / 2

		self.pos = [x, y]

	def render(self):
		"""Render text surface"""

		police = self.text_attributes["police"]
		size = self.text_attributes["size"]
		italic = self.text_attributes["italic"]
		bold = self.text_attributes["bold"]
		text = self.text_attributes["text"]
		antialias = self.text_attributes["antialias"]
		color = self.text_attributes["color"]
		background = self.text_attributes["background"]

		font = pygame.font.SysFont(police, size, italic, bold)

		self.image = font.render(text, antialias, color, background)
