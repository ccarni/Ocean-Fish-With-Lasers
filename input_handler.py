import pygame
import sys

class Input_Handler():
    def __init__(self):
        self.left_click = False
        self.right_click = False
        self.middle_click = False
        self.just_pressed = []
        self.left = False
        self.right = False

        
    def reset_input(self):
        # Reset just_pressed
        self.just_pressed = []

    def do_input(self):
        for event in pygame.event.get():
            self.do_event(event)

    def mouse_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        return mouse_pos

    def do_event(self, event):

        # Do the inputs
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.left_click = True
            if event.button == 2:
                self.middle_click = True
            if event.button == 3:
                self.right_click = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.left_click = False
            if event.button == 2:
                self.middle_click = False
            if event.button == 3:
                self.right_click = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.left = True
            if event.key == pygame.K_RIGHT:
                self.right = True
            if event.key == pygame.K_b:
                self.just_pressed.append(pygame.K_b)
            if event.key == pygame.K_r:
                self.just_pressed.append(pygame.K_r)
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.left = False
            if event.key == pygame.K_RIGHT:
                self.right = False
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def mouse_pos():
    mouse_pos = pygame.mouse.get_pos()
    return mouse_pos
