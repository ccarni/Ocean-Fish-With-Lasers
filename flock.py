import pygame
import random
import sys
import graphics
import numpy as np
import math
from frect import Frect
from boid import Boid
import boid_maneuvers
import input_handler


class Flock():
    def __init__(self, startpos = [-500, 500], color = (255, 0, 0), count = 20, spacing = 200, size = [10, 20], bounds = pygame.Rect(0, 0, 1000, 1000), max_speed = 10, pewpew_speed = 50.0, player = False):
        # Starting position
        self.startpos = startpos

        if player:
            self.startpos = [bounds.width/2, bounds.height/2]
        
        # Zoomies
        self.max_speed = float(max_speed)

        # Fish military pog?
        self.armed = False
        self.pewpew_speed = pewpew_speed
        self.player = player


        # Capitalism
        self.total_value = 0
        self.overall_center = np.array([0, 0], dtype=np.dtype('float64'))

        # Make boids
        self.boids = pygame.sprite.Group()
        for i in range(count):
            newboid = Boid([self.startpos[0] + random.randint(-spacing, spacing), self.startpos[1] + random.randint(-spacing, spacing)]
            , color, size, max_speed=max_speed)
            newboid.flock = self
            self.total_value += newboid.value
            self.boids.add(newboid)

        # Boid Boundaries (Boindaries)
        self.bounds = bounds

        self.shooting = False
        self.guiding = False


        self.center = np.array([0, 0], dtype=np.dtype('float64'))

        # Direction from center to mouse
        self.mousedir = np.array([0, 0], dtype=np.dtype('float64'))


        # Shoot cooldown
        self.max_cooldown = self.pewpew_speed
        self.cooldown = self.max_cooldown

        # List of boids that already shot lasers
        self.reloading_boids = []
        

    def update_boids(self, runner, lasergroup):
        max_dist = 100

        if self.armed:
            self.shooting = True
        
        shoot = False # Do a shoot this update?
        if self.shooting:
            if self.cooldown > 0:
                self.cooldown -= runner.tick
            else:
                self.cooldown = self.max_cooldown
                shoot = True

        # Refresh list of reloading boids
        if len(self.reloading_boids) == len(self.boids):
            self.reloading_boids = []
        

        # Number of boids (n)
        n = len(self.boids)
        # Center of Flock
        self.center = np.array([0, 0], dtype=np.dtype('float64'))



        # Update boids
        for boid in self.boids:
            self.center += boid.frect.center_np()
            
            boid.apply_behavior(self.boids, self.guiding, mousedir=self.mousedir)
            if shoot:
                if not boid in self.reloading_boids:
                    boid.shoot(self, lasergroup)
                    self.reloading_boids.append(boid)
                    shoot = False
            boid.update(10, self.bounds)


        self.center /= n
        if len(self.boids) >= 2:
            self.overall_center = self.center
        

        if self.guiding:
            mouse = np.array(input_handler.mouse_pos(), dtype=np.dtype('float64'))
            self.mousedir = mouse - self.center
            if np.linalg.norm(self.mousedir) != 0:
                self.mousedir = self.mousedir / np.linalg.norm(self.mousedir)



    def draw(self, screen):
        # Draw boid lines
        for boid in self.boids:
            #boid.draw_debug(screen, boids=self.boids)
            #boid.debug_text(str(boid.angle), screen)
            for other_boid in self.boids:
                pass
                #self.draw_between_boids(screen, boid, other_boid)

    def draw_between_boids(self, screen, boid1, boid2, color = (255, 100, 100)):
        pygame.draw.aaline(screen, color, boid1.frect.get_rect().center, boid2.frect.get_rect().center)
        

    def rotate_all(self, delta_angle):
        for boid in self.boids:
            boid.rotate(delta_angle)






    def the_weird_code(self):
        max_dist = 100
        for boid in self.boids:
            neighbours = []
            for other_boid in self.boids:
                if boid.euclidean_distance(other_boid) < max_dist and (not boid.euclidean_distance(other_boid) == 0):
                    neighbours.append(other_boid)
            # Set closest boid to None
            nearest_neighbour = None
            if len(neighbours) > 0:
                shortest_distance = 10000 # Big number
                for neighbour_boid in neighbours:
                    dist = boid.euclidean_distance(neighbour_boid)
                    if dist < shortest_distance:
                        shortest_distance = dist
                        nearest_neighbour = neighbour_boid
            #boid_maneuvers.separation(nearest_neighbour, boid)
            boid_maneuvers.alignment(neighbours, boid)
            boid_maneuvers.cohesion(neighbours, boid)