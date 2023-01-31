import pygame
import numpy as np

class Frect():
    def __init__(self, rect=pygame.Rect(0,0,0,0)):
        self.x = float(rect.x)
        self.y = float(rect.y)
        self.width = float(rect.width)
        self.height = float(rect.height)

    def __getattr__(self, name):
        if name == 'top':
            return self.y
        if name == 'bottom':
            return self.y + self.height
        if name == 'left':
            return self.x
        if name == 'right':
            return self.x + self.width
        if name == 'center':
            return [self.x + self.width/2, self.y + self.height/2]

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def set_center(self, centx, centy):
        self.x = centx - self.width/2
        self.y = centy - self.height/2
        
    def set_center(self, cent):
        self.x = cent[0] - self.width/2
        self.y = cent[1] - self.height/2

    def center(self):
        return [self.x + self.width/2, self.y + self.height/2]

    def center_np(self):
        return np.array([self.x + self.width/2, self.y + self.height/2], dtype='float64')

    def centerx(self):
        return self.x + self.width/2

    def centery(self):
        return self.y + self.height/2