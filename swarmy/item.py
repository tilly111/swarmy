# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   15/02/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
This module represents an item in the environment.
"""

# =============================================================================
# Imports
# =============================================================================
import pygame
import numpy as np

# =============================================================================
# Classes
# =============================================================================
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------        
class Obstacle():
    """
    The Obstacle item represents a barrier for an agent. 
    The agents can't walk through this kind of obstacle
    
    Args:
        e (environemnt): corresponding environment            
        x (int): x-Axis position
        y (int): y-Axis position
        w (int): obstacle width
        h (int): obstacle height
        c (int,int,int): obstacle color   
        b (int): border width
    
    """       
    def __init__(self, e, x, y, w, h, b):
        """
        Initialize a Source item.
        """   
        self.environment = e
        self.color = (0, 0, 0)      
        self.rect = pygame.Rect(0, 0, w, h)        # to track the surface position
        self.rect.centerx = x
        self.rect.centery = y
        self.border = b

        # add obstacle to environemt
        self.environment.staticRectList.append([self.color, self.rect, self.border])


class Item():

    def __init__(self, e, x, y, w, h, r):
        """
        Initialize a Source item.
        """
        self.environment = e
        self.color = (0, 100, 0)
        self.rect = pygame.Rect(0, 0, w, h)        # to track the surface position
        self.rect.centerx = x
        self.rect.centery = y
        self.radius = r
        self.picked_up = False
        self.holding_robot = None
        self.pushing_robots = []

        # add obstacle to environemt
        self.environment.dynamicItems.append(self)

    def render(self):
        """
        Render body orientation and position & Update token
        """
        if self.holding_robot:  # TODO check if this is equal to not none
            self.rect.centerx = self.holding_robot.body.rect.centerx
            self.rect.centery = self.holding_robot.body.rect.centery

        for r in self.pushing_robots:
            x_dir = (self.rect.centerx - r.actuation.position[0])
            y_dir = (self.rect.centery - r.actuation.position[1])
            x_dir_n = x_dir/np.sqrt(x_dir**2 + y_dir**2) * r.actuation.LINEAR_VELOCITY
            y_dir_n = y_dir/np.sqrt(x_dir**2 + y_dir**2) * r.actuation.LINEAR_VELOCITY
            self.rect.centerx += x_dir_n
            self.rect.centery += y_dir_n
        self.pushing_robots.clear()

        self.environment.dynamicItems.append(self)