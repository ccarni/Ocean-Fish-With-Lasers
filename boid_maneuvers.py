import numpy as np
import math








def rule1(other_boid, center, n):
    newcenter = center
    if other_boid != other_boid:
        newcenter += other_boid.frect.center_np()

    newcenter = newcenter / (n - 1)

    return (newcenter - other_boid.frect.center_np()) / 100




def separation(nearest_neighbor, boid):
    # move 1: move away from nearest - separation
    # calculate angle between boid and nearest boid, then angle it in the opposite direction
    if nearest_neighbor is not None and boid.euclidean_distance(nearest_neighbor) < 35:
        if nearest_neighbor.frect.x - boid.frect.x == 0.0:
            angle = math.atan((nearest_neighbor.frect.y - boid.frect.y) / 0.0001)
        else:
            angle = math.atan((nearest_neighbor.frect.y - boid.frect.y) / (nearest_neighbor.frect.x - boid.frect.x))
        boid.angle -= angle

def alignment(neighbors, boid):
    # move 2: orient towards the neighbors - alignment
    # calculate average angle of neighbors and move in that direction
    average_neighbors_angle = 0.0
    if neighbors:
        for neighbor_boid in neighbors:
            average_neighbors_angle += neighbor_boid.angle
        average_neighbors_angle /= len(neighbors)
        boid.angle -= (average_neighbors_angle-boid.angle)/100.0
        boid.angle = average_neighbors_angle

def cohesion(neighbors, boid):
    # move 3: move together - cohesion
    if neighbors:
        avg_x = 0.0
        avg_y = 0.0
        for neighbor_boid in neighbors:
            avg_x += neighbor_boid.frect.x
            avg_y += neighbor_boid.frect.y
        avg_x /= len(neighbors)
        avg_y /= len(neighbors)
        if avg_x - boid.frect.x == 0.0:
            angle = math.atan((avg_y - boid.frect.y) / 0.00001)
        else:
            angle = math.atan((avg_y - boid.frect.y) / (avg_x - boid.frect.x))
        boid.angle -= angle / 20.0