import pygame
import random
import sys
import graphics
import numpy as np
import math
from frect import Frect
import input_handler

class Laser(pygame.sprite.Sprite):
    def __init__(self, flock, boid, pos = [0.0, 0.0], dir = [0.0, 0.0], color = (255, 0, 0), thick = 4, length = 20, max_speed = 10):
        # Init sprite
        pygame.sprite.Sprite.__init__(self)
        
        # Transform
        self.pos = np.array(pos, dtype='float64')
        self.dir = dir
        self.angle = random.uniform(0.0, 2.0 * math.pi)
        
        # Graphics
        self.color = color
        self.true_image = graphics.draw_laser(self.color, thick, length)
        self.image = self.true_image

        # Flock
        self.flock = flock
        self.boid = boid

        # Frect Rect
        self.frect = Frect(self.image.get_rect())
        self.frect.x = self.pos[0]
        self.frect.y = self.pos[1]
        self.set_real_rect()
        
        # Set pos
        self.frect.set_center(self.boid.frect.center() + self.vector_from_angle(self.boid.angle, self.boid.frect.width / 2 + self.frect.width / 2))


        # Laser stuff
        self.lifetime = 1000
        self.max_speed = max_speed

    def update_sprite(self):
        self.image = pygame.transform.rotate(self.true_image, self.angle - 90)
        cent = self.frect.center()
        self.frect = Frect(self.image.get_rect())
        self.frect.set_center(cent)
        self.set_real_rect()

    def update(self, runner):

        self.clamp_speed()

        # Update Position
        self.frect.x += self.dir[0]
        self.frect.y += self.dir[1]
        
        # Set angle to direction
        self.angle = self.angle_from_vector(self.dir)

        # Update sprite
        self.set_real_rect()
        self.update_sprite()

        self.clamp_speed()

        # Lifetime
        self.lifetime -= runner.tick

        # Die.
        if self.lifetime < 0:
            self.kill()
            del self

    def clamp_speed(self):
        if np.linalg.norm(self.dir) != 0:
            self.dir = (self.dir / np.linalg.norm(self.dir)) * self.max_speed

        
    def set_real_rect(self,):
        self.rect = self.frect.get_rect()




    def angle_from_vector(self, vector):
        angle = 0
        v = vector
        if v[0] != 0:
            v = vector / np.linalg.norm(vector)
            #angle = np.degrees(math.atan(v[1]/v[0]))
            angle = -np.degrees(np.arctan2(v[1], v[0]))
        return angle

    def vector_from_angle(self, angle, dist):
        angle = -np.radians(angle)
        x = np.cos(angle) * dist
        y = np.sin(angle) * dist
        vector = np.array([x, y], dtype='float64')
        return vector