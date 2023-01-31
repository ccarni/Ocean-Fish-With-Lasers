import pygame
import random
import sys
import drawings
import bonus_text


class World():
    def __init__(self, runner):
        
        # Initialize screen
        self.screen = pygame.display.set_mode()
        self.background_color = (100, 100, 255)

        # Runner
        self.runner = runner


        # Jaren balckgronds
        self.balckgronds_color = (47, 69, 138)
        self.scr = drawings.screener(self.screen, self.balckgronds_color)


        # Bonus point texts
        self.bonus_texts = []
        self.last_text = "None"


    def draw(self):
        self.screen.blit(self.scr, (0, 0))

        # Render flocks
        for flock in self.runner.flocks:
            flock.draw(self.screen)
            flock.boids.draw(self.screen)
            

        self.screen.blit(self.runner.fish, self.runner.fish_pos)
        self.runner.lasers.draw(self.screen)
        self.runner.explosions.draw(self.screen)
        for explosion in self.runner.explosions:
            pygame.draw.ellipse(self.screen, (255, 255, 255), explosion.rect, 3)

        # Draw texts:
        for text in self.bonus_texts:
            text.draw(self.screen, self.runner)
            # Yeet
            if text.lifetime < 0:
                if text.is_big == False:
                    self.last_text = "None"
                self.bonus_texts.remove(text)
                del text
        #if self.last_text == "None":
            #pygame.draw.ellipse(self.screen, (255, 255, 255), pygame.Rect(100, 100, 100, 100), 3)

        self.draw_score()
        if self.runner.lost_game:
            self.do_big_text("You've been fished.", 0.3, 120)
            self.do_big_text("Your final score was: " + str(self.runner.score), 0.5, 100)
        pygame.display.update()

    def do_big_text(self, text, height_mult = 0.3, font_size = 120):
        font = pygame.font.SysFont(None, 120)
        text = font.render(text, True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (self.screen.get_width() / 2, self.screen.get_height() * height_mult)
        self.screen.blit(text, textRect)


    def draw_score(self):
        screen_width = self.screen.get_width()

        font = pygame.font.SysFont("monospace", 40)

        text = font.render("Score is: " + str(self.runner.score), True, (0, 255, 0), (0, 0, 255))
        textRect = text.get_rect()
        textRect.center = (screen_width - textRect.width / 2 - 10, 30)
        self.screen.blit(text, textRect)

    def add_bonus(self, amount, position, upspeed = 3, lifetime = 100, scale = 40, is_big = False, color=(255, 255, 255)):
        text = bonus_text.Bonus_Text("+" + str(amount), position, upspeed, lifetime, color=color, scale = scale, is_big=is_big)
        self.bonus_texts.append(text)
        return text