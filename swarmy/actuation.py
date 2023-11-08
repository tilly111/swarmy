# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   15/02/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
The module represents the motion capabilites of an agent.
"""

# =============================================================================
# Imports
# =============================================================================
import math
import pygame
import numpy as np
# =============================================================================
# Class
# =============================================================================
class Actuation():
    """
    The actuation object represents the physical movement and physical actions.
    
    Available capabilities:
        Move forward, move backward, 
        turn left, turn right, turn angle, 
    
    Args:
        g (agent.py): instance of the agent
        p ([int, int]): center position
        d (int): initial angle (direction)    
    """
    def __init__(self, g, p, d):
        """
        Initialize actuation object.
        """    
        # constants
        self.LINEAR_VELOCITY = 4                # choose even number
        self.ANGLE_VELOCITY = 6                 # choose even number

        # variables
        self.agent = g                  # parent python module
        self.position = p
        self.angle = (d + 90) % 360     # intial position is 90 degrees
        self.direction = [math.sin(math.radians(self.angle)), math.cos(math.radians(self.angle))]  # unit vector showing the direction
                              
    def stepForward(self):
        """
        One step forward.
        """
        # calculate the position from the direction and speed and update body position
        self.position[0] += self.direction[0]*self.LINEAR_VELOCITY
        self.position[1] += self.direction[1]*self.LINEAR_VELOCITY
        self.agent.body.rect.centerx = self.position[0]
        self.agent.body.rect.centery = self.position[1]
    
    
    def stepBackward(self):
        """
        One step backward.
        """
        # calculate the position from the direction and speed and update body position
        self.position[0] -= self.direction[0]*self.LINEAR_VELOCITY
        self.position[1] -= self.direction[1]*self.LINEAR_VELOCITY
        self.agent.body.rect.centerx = self.position[0]
        self.agent.body.rect.centery = self.position[1]


    def turnLeft(self):
        """
        turns left.
        """
        # new angle
        self.angle = (self.angle + self.ANGLE_VELOCITY) % 360

        # calculate the direction from the angle variable
        self.direction[0] = math.sin(math.radians(self.angle))
        self.direction[1] = math.cos(math.radians(self.angle))


    def turnRight(self):
        """
        Turns right.
        """
        # new angle
        self.angle = (self.angle - self.ANGLE_VELOCITY) % 360

        # calculate the direction from the angle variable
        self.direction[0] = math.sin(math.radians(self.angle))
        self.direction[1] = math.cos(math.radians(self.angle))


    def turnRightForward(self):
        self.turnRight()
        self.stepForward()


    def turnLeftForward(self):
        self.turnLeft()
        self.stepForward()


    def wait(self):
        self.agent.body.rect.centerx = self.position[0]
        self.agent.body.rect.centery = self.position[1]
        
#%% Helper functions
        
    def processUserInput(self, pressedKeys):
        """
        Process user keyboard input.
        
        Args:
            pressedKeys (Pygame Keyboard Codes)
        
        """
        if pressedKeys[pygame.K_UP]:           
            self.stepForward()
            
        if pressedKeys[pygame.K_DOWN]:
            self.stepBackward()
            
        if pressedKeys[pygame.K_LEFT]:
            # new angle
            self.angle = (self.angle + self.ANGLE_VELOCITY) % 360
                    
            # calculate the direction from the angle variable
            self.direction[0] = math.sin(math.radians(self.angle))
            self.direction[1] = math.cos(math.radians(self.angle))         
            
        if pressedKeys[pygame.K_RIGHT]:          
            # new angle
            self.angle = (self.angle - self.ANGLE_VELOCITY) % 360

            # calculate the direction from the angle variable
            self.direction[0] = math.sin(math.radians(self.angle))
            self.direction[1] = math.cos(math.radians(self.angle))
            