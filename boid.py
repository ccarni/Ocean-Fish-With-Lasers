import pygame
import random
import sys
import graphics
import numpy as np
import math
from frect import Frect
import input_handler
from laser import Laser

class Boid(pygame.sprite.Sprite):
    def __init__(self, pos = [0.0, 0.0], color = (255, 0, 0), size = [10, 20], max_speed = 10):
        # Init sprite
        pygame.sprite.Sprite.__init__(self)
        
        # Transform
        self.pos = np.array([pos[0], pos[1]], dtype='float64')
        self.angle = random.uniform(0.0, 2.0 * math.pi)
        
        # Physics
        self.v = np.array([0, 0], dtype=np.dtype('float64'))
        self.acceleration = np.array([random.randint(-10, 10), random.randint(-10, 10)], dtype=np.dtype('float64')) / 1000
        self.max_speed = max_speed

        # Graphics
        self.color = color
        self.true_image = graphics.draw_fish(self.color, size)
        self.image = self.true_image


        # Boid Mechanics
        self.perception = 150
        self.separation_distance = self.perception / 3
        self.max_force = 1
        self.turn_force = 0




        # Also add actual self.rect
        self.frect = Frect(self.image.get_rect())
        self.frect.x = self.pos[0]
        self.frect.y = self.pos[1]
        self.set_real_rect()

        
        # Gameplay stuff (mostly exploiting fish for money)
        self.value = int(self.frect.height / 10)


        # Shooting laser order
        self.already_shot = False


        # If it spawns outside, make it not be outside
        #self.loop_screen(bounds)

    def shoot(self, flock, lasergroup):
        
        laser_color = (100, 255, 100)
        if not flock.player:
            laser_color = self.color

        laser_speed = 5 + self.max_speed * 2.5
        laser_position = self.frect.center_np()# + 
        #laser_position[1] -= self.frect.height / 2
        laser_dir = self.vector_from_angle(self.angle, laser_speed)
        laser_thick = 4
        laser_length = 20
        laser = Laser(flock, self, laser_position, laser_dir, laser_color, laser_thick, laser_length, laser_speed)
        lasergroup.add(laser)
        


    def draw_debug(self, screen, color = (50, 255, 50), boids = None):
        scale = 100
        mouse = np.array(input_handler.mouse_pos(), dtype=np.dtype('float64'))
        angle = -np.radians(self.angle)
        x = np.cos(angle) * scale
        y = np.sin(angle) * scale
        debug = np.array([x, y], dtype='float64')
        #debug = self.cohesion(boids)[1]
        #debug += self.frect.center_np()
        #pygame.draw.aaline(screen, color, self.frect.get_rect().center, self.frect.center() + debug)
        #pygame.draw.aaline(screen, (0, 255, 0), self.frect.get_rect().center, self.frect.get_rect().center + self.v * scale)
        pygame.draw.circle(screen, color, self.frect.center(), self.perception, 1)
        pygame.draw.circle(screen, color, self.frect.center(), self.separation_distance, 1)
        

    def debug_text(self, text, screen):
        font = pygame.font.Font(None, 100)
        text = font.render(text, False, (255, 255, 255))
        screen.blit(text, (0, 0))

    def update(self, speed, bounds):
        

        self.frect.x += self.v[0]
        self.frect.y += self.v[1]

        #self.loop_screen(bounds)

        self.v[0] += self.acceleration[0]
        self.v[1] += self.acceleration[1]
        
        if np.linalg.norm(self.v) > self.max_speed:
            self.v = self.v / np.linalg.norm(self.v) * self.max_speed

        # Set angle to direction
        self.angle = self.angle_from_vector(self.v) + self.turn_force
        

        #self.move_forward(speed)
        self.update_sprite()

        # DONT BOUNCE!! 
        bouncey = True
        if bouncey:
            self.bounce(bounds)

        # Reset turn force every time
        self.turn_force = 0


    

    def update_sprite(self):
        self.image = pygame.transform.rotate(self.true_image, self.angle - 90)
        cent = self.frect.center()
        self.frect = Frect(self.image.get_rect())
        self.frect.set_center(cent)
        self.set_real_rect()

    def set_real_rect(self,):
        self.rect = self.frect.get_rect()
    
    def loop_screen(self, bounds):
        self.frect.x = self.frect.x % bounds.width
        self.frect.y = self.frect.y % bounds.height

    def align(self, boids):
        steering = np.array([0, 0], dtype=np.dtype('float64'))
        total = 0
        avg_vec = np.array([0, 0], dtype=np.dtype('float64'))
        for boid in boids:
            if boid != self:
                if np.linalg.norm(boid.frect.center_np() - self.frect.center_np()) < self.perception:
                    avg_vec += boid.v
                    total += 1
        if total > 0:
            avg_vec /= total
            if np.linalg.norm(avg_vec) != 0:
                avg_vec = (avg_vec / np.linalg.norm(avg_vec)) * self.max_speed
            steering = avg_vec - self.v
            
        return steering, avg_vec

    def cohesion(self, boids):
        steering = np.array([0, 0], dtype=np.dtype('float64'))
        total = 0
        center_of_mass = np.array([0, 0], dtype=np.dtype('float64'))

        for boid in boids:
            if np.linalg.norm(boid.frect.center_np() - self.frect.center_np()) < self.perception:
                center_of_mass += boid.frect.center_np()
                total += 1
        center_of_mass /= total
        if total > 0:
            
            vec_to_com = center_of_mass - self.frect.center_np()  
            if np.linalg.norm(vec_to_com) > 0:
                vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * self.max_speed
            steering = vec_to_com - self.v
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering / np.linalg.norm(steering)) * self.max_force
        return steering, center_of_mass

    def go_mouse(self):
        mouse = np.array(input_handler.mouse_pos(), dtype=np.dtype('float64'))
        steering = np.array([0, 0], dtype=np.dtype('float64'))
        vec_to_com = mouse - self.frect.center_np()  
        if np.linalg.norm(mouse - self.frect.center_np()) < self.perception:
            if np.linalg.norm(vec_to_com) > 0:
                vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * self.max_speed
            steering = vec_to_com - self.v
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering / np.linalg.norm(steering)) * self.max_force
        return steering


    def separation(self, boids):
        steering = np.array([0, 0], dtype=np.dtype('float64'))
        total = 0
        avg_vector = np.array([0, 0], dtype=np.dtype('float64'))
        for boid in boids:
            distance = np.linalg.norm(boid.frect.center_np() - self.frect.center_np())
            if (self.frect.center_np()[0] != boid.frect.center_np()[0] and
                self.frect.center_np()[1] != boid.frect.center_np()[1]) and distance < self.separation_distance:
                diff = self.frect.center_np() - boid.frect.center_np()
                diff /= distance
                avg_vector += diff
                total += 1
        if total > 0:
            avg_vector /= total
            if np.linalg.norm(steering) > 0:
                avg_vector = (avg_vector / np.linalg.norm(steering)) * self.max_speed
                print(steering)
            steering = avg_vector - self.v
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering /np.linalg.norm(steering)) * self.max_force
        

        return steering

    def turn(self, force = 0):
        mouse = np.array(input_handler.mouse_pos(), dtype=np.dtype('float64'))
        angle = np.radians(self.angle) + force
        #print("Angle1 = " + str(self.angle))
        #print("Angle2 = " + str(self.angle + force))
        x = np.cos(angle)
        y = np.sin(angle)
        acc = np.array([x, y], dtype='float64')
        return acc

    def apply_behavior(self, boids, guiding = False, mousedir=[0, 0]):
        alignment = self.align(boids)[0]
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)
        self.acceleration += alignment * 0.1
        self.acceleration += cohesion[0] * 0.1
        self.acceleration += separation * 0.9 * 1.5
        if guiding:
            self.acceleration += mousedir

        if self.turn_force != 0:
            turn = self.turn(self.turn_force)
            self.acceleration += turn
        
        # Constrain velocity
        self.acceleration = (self.acceleration / np.linalg.norm(self.acceleration)) * self.max_speed
        
    def bounce(self, bounds):
        if self.frect.left < bounds.left:
            self.frect.left = bounds.left
            self.v[0] = abs(self.v[0])
            self.frect.x += self.v[0]
            self.invert_acceleration(x=True)
        if self.frect.top < bounds.top:
            self.frect.top = bounds.top
            self.v[1] = abs(self.v[1])
            self.frect.y += self.v[1]
            self.invert_acceleration(y=True)
        if self.frect.right > bounds.right:
            self.frect.right = bounds.right
            self.v[0] = -abs(self.v[0])
            self.frect.x += self.v[0]
            self.invert_acceleration(x=True)
        if self.frect.bottom > bounds.bottom:
            self.frect.bottom = bounds.bottom
            self.v[1] = -abs(self.v[1])
            self.frect.y += self.v[1]
            self.invert_acceleration(y=True)

    def invert_acceleration(self, x=False, y=False):
        if x:
            self.acceleration[0] *= -1
        if y:
            self.acceleration[1] *= -1


    def angle_from_vector(self, vector):
        angle = 0
        v = vector
        if v[0] != 0:
            v = vector / np.linalg.norm(vector)
            #angle = np.degrees(math.atan(v[1]/v[0]))
            angle = -np.degrees(np.arctan2(v[1], v[0]))
        return angle

    def vector_from_angle(self, angle, dist):
        angle = -np.radians(self.angle)
        x = np.cos(angle) * dist
        y = np.sin(angle) * dist
        vector = np.array([x, y], dtype='float64')
        return vector

