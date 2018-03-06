"""Fichier contenant un objet entity"""

from moteur_graph import *


class Entity(AnimatedObject):

    def __init__(self, pos, images, pos_mode, visible=True):

        self.visible = visible

        AnimatedObject.__init__(self, images, pos)

        self.pos_mode = pos_mode

        self.hitbox = []
        self.update_hitbox()

    def move(self, dx=0, dy=0):

        self.pos[0] += dx
        self.pos[1] += dy

        self.update_hitbox()

    def update_hitbox(self):
        """Update the coordinates of the hitbox based on the size of the current image"""

        pos = self.pos
        size = self.image.get_size()

        self.hitbox = [pos[0], pos[1], size[0], size[1]]

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
        """Use projection on both axis to know if rectangle are overlapping"""
        x_a = self.pos[0]
        x_b = entity.pos[0]
        lxa = self.pos[2]
        lxb = entity.pos[2]

        if (x_a < x_b < x_a + lxa) or (x_b < x_a < x_b + lxb):

            y_a = self.pos[1]
            y_b = entity.pos[1]
            lya = self.pos[3]
            lyb = entity.pos[3]

            if (y_a < y_b < y_a + lya) or (y_b < y_a < y_b + lyb):
                return True

        return False
