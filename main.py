import pygame
import random
import sys
from runner import Runner


class Main():
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Make Mouse Invisible
        pygame.mouse.set_visible(False)

        runner = Runner(self)


        while True:
            runner.update()
            runner.draw()


main = Main()