import pygame
import math
import numpy as np
import pygame
import random

class Explosion(pygame.sprite.Sprite):
    def __init__(self, color, radius, world, pos=(0, 0), v=(0,0)):

        self.lifetime = radius
        self.maxlife = self.lifetime
        self.max_radius = radius

        self.color = color
 
        self.pos = pos

        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.image = pygame.surface.Surface((2*radius, 2*radius))
        self.image.set_alpha(28)
        self.image.fill((0, 0, 0))
        pygame.draw.ellipse(self.image, color, self.image.get_rect())
        pygame.draw.ellipse(self.image, (255, 255, 255), self.image.get_rect(), 2)
        self.image.set_colorkey((0,0,0))

        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.v = np.array(v)
        self.mass = math.pi*radius*radius

        self.world = world

        self.debug_vector = [0, 0]


    def update_image(self):
        
        self.image = pygame.surface.Surface((2*self.radius, 2*self.radius))
        self.image.set_alpha(100)
        self.image.fill((0, 0, 0))
        pygame.draw.ellipse(self.image, self.color, self.image.get_rect())
        
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def explosion_update(self):
        self.lifetime -= 1
        perc = self.lifetime / self.maxlife + 0.1
        self.radius = self.max_radius * perc
        self.mass = math.pi*self.radius*self.radius
        self.update_image()
        if self.lifetime < 0:
            self.kill()
            del self
