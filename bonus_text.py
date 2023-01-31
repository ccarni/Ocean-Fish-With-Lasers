import pygame

class Bonus_Text():
    def __init__(self, text, startpos = [200, 200], upspeed = 3, lifetime = 100, color = (255, 255, 255), scale = 40, is_big=False):
        self.text = text
        self.pos = startpos
        self.upspeed = upspeed
        self.color = color
        self.scale = scale
        
        self.height = 0.0

        self.is_big = is_big

        self.lifetime = lifetime * 20
        self.maxlife = self.lifetime

    def draw(self, screen, runner):
        self.lifetime -= runner.tick

        font = pygame.font.SysFont("monospace", self.scale)

        self.height -= runner.tick * self.upspeed / 20

        if self.is_big:
            self.color = (255, 0, 0)

        text = font.render(self.text, True, self.color)
        textRect = text.get_rect()
        textRect.center = (self.pos[0] - textRect.width / 2, self.pos[1] + self.height)
        screen.blit(text, textRect)

