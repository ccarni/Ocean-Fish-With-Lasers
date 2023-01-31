import random
import pygame

def clip(number, lower, upper):
    number = max(lower, number)
    number = min(upper, number)
    return number

# This updates the color of a pixel by amount
def update_color(surf, point, amount):
    color = surf.get_at(point)
    color[0] = clip(color[0] + amount[0], 0, 255)
    color[1] = clip(color[1] + amount[1], 0, 255)
    color[2] = clip(color[2] + amount[2], 0, 255)
    surf.set_at(point, color)

# This helps smooth over random noise to (hopefully) improve quality of the images
def update_surrounding(surf, i, j, amount):
    update_color(surf, (i, j), amount)

    amount2 = [amount[i] // 1 for i in range(3)]
    right = ((i + 1) % surf.get_width(), j)
    left = ((i - 1 + surf.get_width()) % surf.get_width(), j)
    up = (i, (j - 1 + surf.get_height()) % surf.get_height())
    down = (i, (j + 1) % surf.get_height())
    update_color(surf, right, amount2)
    update_color(surf, left, amount2)
    update_color(surf, up, amount2)
    update_color(surf, down, amount2)

def screener(screen, back_color=(200, 191, 157)):
    surf = pygame.Surface((screen.get_width() / 25, screen.get_height() / 25))
    surf.fill(back_color)
    for i in range(surf.get_width()):
        for j in range(surf.get_height()):
            amount = [random.randint(0, 3) for i in range(3)]
            update_surrounding(surf, i, j, amount)
    surf = pygame.transform.scale(surf, (screen.get_width(), screen.get_height()))
    return surf