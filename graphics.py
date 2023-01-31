import pygame

def draw_fish(color="red"):
    surf = pygame.surface.Surface((10, 10))

    # Dark, saturated red (according to google.com)
    dark_saturated_red = (255, 0, 92)
    green = (100, 255, 100)
    if color == "red":
        surf.fill(dark_saturated_red)
    if color == "green":
        surf.fill(green)
    return surf


def draw_boid(color = (255, 0, 0), size = [10, 20]):
    surf = pygame.surface.Surface((size[0], size[1]))
    surf.fill((0, 0, 0))
    pygame.draw.rect(surf, color, surf.get_rect())
    surf.set_colorkey((0,0,0))
    pygame.draw.rect(surf, (255, 255, 255), surf.get_rect(), width=1)
    return surf

def draw_laser(color = (255, 0, 0), thick = 4, length = 20):
    surf = pygame.surface.Surface((thick, length))
    surf.fill((0, 0, 0))
    pygame.draw.rect(surf, color, surf.get_rect())
    surf.set_colorkey((0,0,0))
    return surf

def draw_fish(color = (255, 0, 0), size = [10, 20]):
    surf = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
    fish_width = int(2)
    surf.fill((0, 0, 0, 0))

    p1 = (0, surf.get_height())
    p2 = (surf.get_width(), surf.get_height()/3)
    p3 = (surf.get_width()/2, 0)
    p4 = (0, surf.get_height()/3)
    p5 = (surf.get_width(), surf.get_height())
    pygame.draw.polygon(surf, color, [p1, p2, p3, p4, p5])
    pygame.draw.polygon(surf, (255, 255, 255), [p1, p2, p3, p4, p5], width=1)

    p6 = (surf.get_width()/3, surf.get_height()/4)
    p7 = (7*surf.get_width()/12, surf.get_height()/4)
    pygame.draw.line(surf, color, p6, p7, width=2)

    surf.convert()
    return surf