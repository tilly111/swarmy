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
from abc import abstractmethod
import numpy as np
import yaml
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
    def __init__(self, g):
        """
        Initialize actuation object.
        """    
        # constants

        # variables
        self.agent = g                  # parent python module
        self.position = [0,0]
        self.angle  = 0
        self.direction = [0,0]          # unit vector showing the direction

        with open('config.yaml', 'r') as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)
            
    @abstractmethod
    def torus(self):
        print('Torus not implemented')

    @abstractmethod
    def controller(self):
        print('Controller not implemented')

    def stepForward(self, velocity):
        """
        One step forward.
        """

        # calculate the position from the direction and speed and update body position
        robot_position_x, robot_position_y, robot_heading = self.agent.get_position()

        direction_x = math.sin(math.radians(robot_heading))
        direction_y = math.cos(math.radians(robot_heading))

        new_position_x = float(robot_position_x + direction_x * velocity)
        new_position_y = float(robot_position_y + direction_y * velocity)

        self.agent.set_position(new_position_x, new_position_y, robot_heading)

    def stepBackward(self,velocity):
        """
        One step backward.
        """
        robot_position_x, robot_position_y, robot_heading = self.agent.get_position()

        direction_x = math.sin(math.radians(robot_heading))
        direction_y = math.cos(math.radians(robot_heading))
        new_position_x = robot_position_x - direction_x * velocity
        new_position_y = robot_position_y - direction_y * velocity

        self.agent.set_position(new_position_x, new_position_y, robot_heading)

    def turn_right(self, angle_velocity):

        robot_position_x, robot_position_y, robot_heading = self.agent.get_position()
        new_angle = (robot_heading - angle_velocity) % 360
        self.agent.set_position(robot_position_x, robot_position_y, new_angle)

    def turn_left(self,angle_velocity):
        # new angle
        robot_position_x, robot_position_y, robot_heading = self.agent.get_position()
        new_angle = (robot_heading + angle_velocity) % 360
        self.agent.set_position(robot_position_x, robot_position_y, new_angle)

#%% Helper functions
        
    def processUserInput(self, pressedKeys):
        """
        Process user keyboard input.
        
        Args:
            pressedKeys (Pygame Keyboard Codes)
        
        """
        if pressedKeys[pygame.K_UP]:           
            self.stepForward(self.config['default_velocity'])
            
        if pressedKeys[pygame.K_DOWN]:
            self.stepBackward(self.config['default_velocity'])
            
        if pressedKeys[pygame.K_LEFT]:
            # new angle
            self.turn_left(self.config['default_angle_velocity'])
            
        if pressedKeys[pygame.K_RIGHT]:          
            self.turn_right(self.config['default_angle_velocity'])
            