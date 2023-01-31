import pygame
import random
import sys
import world
import input_handler
import graphics
from flock import Flock
from explosion import Explosion

class Runner():
    def __init__(self, main):

        # Init world
        self.world = world.World(runner=self) 


        # Init flocks of boids
        self.flocks = []
        self.lasers = pygame.sprite.Group()
        

        # Explosions
        self.explosions = pygame.sprite.Group()
        #self.flocks.append(Flock(bounds=self.world.screen.get_rect()))

        
        self.player_flock = self.add_random_flock(5, player=True)
        self.add_random_flock(5, 2)

        # Clock Tick
        self.tick = 0
        self.FPS = 60
        self.clock = pygame.time.Clock()

        # The input boi
        self.input_boi = input_handler.Input_Handler()

        # The debug fish [debug]
        self.fish = graphics.draw_fish()
        self.fish_pos = [100, 100]

        # Flock spawner
        self.time_since_flock = 0
        self.time_till_flock = random.randint(200, 400)


        # Score
        self.score = 0

        # For text movement
        self.last_hit_flock = None


        # Chance to arm fish
        self.fish_arming_chance = 0.5


        
        # Main and restarting
        self.lost_game = False
        self.main = main


    def update(self):
        self.tick = self.clock.tick(self.FPS)

        # Jarne flobck spawneber
        self.update_flock_spawner()

        # Do input
        self.input_boi.do_input()

        # Update boom booms
        for explosion in self.explosions:
            explosion.explosion_update()

        # Restart
        if pygame.K_r in self.input_boi.just_pressed:
            self.__init__(self.main)


        # Fish cursor
        self.fish_pos = self.input_boi.mouse_pos()

        # Debug Fish Click [debug]
        if self.input_boi.left_click:
            self.fish = graphics.draw_fish("green")
            
                
            
            if False: #DEBUG FOR ZOOMEIES
                for flock in self.flocks:
                    for boid in flock.boids:
                        go_mouse = boid.go_mouse()
                        boid.acceleration += go_mouse / 1
        else:
            self.fish = graphics.draw_fish("red")




            #self.add_random_flock(5, random.randint(20, 30)/20)

        if len(self.player_flock.boids) < 1:
            self.lost_game = True

        # Rotate boids [debug]            
        self.player_flock.guiding = self.input_boi.right_click
        self.player_flock.shooting = self.input_boi.left_click
        if self.input_boi.left:
            for flock in self.flocks:
                for boid in flock.boids:
                    boid.turn_force = 10
        if self.input_boi.right:
            for flock in self.flocks:
                for boid in flock.boids:
                    boid.turn_force = -10

        for flock in self.flocks:
            if self.input_boi.left_click:
                if flock != self.player_flock:
                    if float(random.randint(0, 10000)) / 100 <= self.fish_arming_chance:
                        flock.armed = True
            flock.update_boids(self, self.lasers)

            # Collision with lasers/balls
            laserboid_collision = pygame.sprite.groupcollide(flock.boids, self.lasers, False, False)

            list_to_die = []
            for col_boid in laserboid_collision.keys():
                for col_laser in laserboid_collision[col_boid]:
                    playerhit = col_boid.flock == self.player_flock
                    if col_laser.flock == self.player_flock or col_boid.flock == self.player_flock:
                        if col_laser.flock != col_boid.flock:
                            if not playerhit:
                                self.score += col_boid.value
                            else:
                                self.world.add_bonus("Bruh", col_boid.frect.center(), 3, 100, 60, color=(235, 107, 52))
                            self.add_explosion(col_boid.color, col_boid.frect.center(), col_boid.frect.width)
                            self.last_hit_flock = col_boid.flock
                            col_laser.kill()
                            del col_laser
                            list_to_die.append(col_boid)
                            if not playerhit:
                                try:
                                    if len(flock.boids) <= 1:
                                        self.world.add_bonus(flock.total_value, flock.overall_center, 3, 100, 100, is_big=True)
                                        self.score += flock.total_value
                                        print("it dead")
                                        del flock
                                except:
                                    print("whoopsie")
                            if playerhit:
                                if len(flock.boids) <= 1:
                                    col_boid.frect.y = 10000
            for boid in list_to_die:
                if self.world.last_text == "None":
                    self.world.last_text = self.world.add_bonus(boid.value, boid.frect.center(), 3, 100, 40)
                else:
                    if boid.flock != self.last_hit_flock:
                        self.world.last_text.pos = boid.frect.center()
                    self.world.last_text.text.removeprefix("+")
                    self.world.last_text.text = "+" + str(int(self.world.last_text.text) + boid.value)
                boid.kill()
                del boid

        for laser in self.lasers:
            laser.update(self)


        


    def draw(self):
        self.world.draw()

    # Maybe make new class with functions like this <-------------
    def add_random_flock(self, count = 10, sizemult = 1.5, player = False):
        r = random.randint(50, 255)
        g = random.randint(50, 255)
        b = random.randint(50, 255)
        count = count
        spacing = random.randint(10, random.randint(10, 1000))
        size = [0, 0]
        size[0] = random.randint(10, 20) * sizemult
        size[1] = size[0] + random.randint(5, 10) * sizemult
        speed = random.randint(3, 6)

        pewpew_speed=float(random.randint(0,random.randint(0,500)))

        if player == True:
            spacing = 100
            count = count
            speed = 4
            pewpew_speed=float(random.randint(30,60))

        

        rand_speed = random.randint(-1, 1)
        flock = Flock(bounds=self.world.screen.get_rect(), color=(r, g, b), count=count, 
                spacing=spacing, size=size, max_speed=speed, pewpew_speed=pewpew_speed, player=player)
        self.flocks.append(flock)

        return flock

    def update_flock_spawner(self):
        self.time_since_flock += 1
        if self.time_since_flock >= self.time_till_flock:
            self.add_random_flock(random.randint(5,random.randint(10,15)))
            self.time_since_flock = 0
            self.time_till_flock = random.randint(200, 400)


    def add_explosion(self, color, position, size):
        b = Explosion(color, size / 2 + random.randint(0,5), self, position)
        self.explosions.add(b)