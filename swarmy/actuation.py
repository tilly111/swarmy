# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   15/02/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
The module represents the motion capabilities of an agent.
"""

# =============================================================================
# Imports
# =============================================================================
import math
import pygame
from abc import ABC, abstractmethod


# =============================================================================
# Class
# =============================================================================
class Actuation(ABC):
    """
    The actuation object represents the physical movement and physical actions.

    Available capabilities:
        move forward, move backward,
        turn left, turn right

    Args:
        agent (agent.py): instance of the agent
        config (dict): simulation configuration from config.yaml
    """
    def __init__(self, agent, config):
        """
        Initialize actuation object.
        """
        self.agent = agent              # parent python module
        self.position = [0, 0]
        self.heading = 0
        self.config = config

    @abstractmethod
    def torus(self):
        print('Torus not implemented')

    @abstractmethod
    def controller(self):
        print('Controller not implemented')

    def step_forward(self, velocity):
        """
        One step forward.
        """
        # calculate the position from the direction and speed and update body position
        x, y, heading = self.agent.get_position()

        direction_x = math.sin(math.radians(heading))
        direction_y = math.cos(math.radians(heading))

        new_x = float(x + direction_x * velocity)
        new_y = float(y + direction_y * velocity)

        self.agent.set_position(new_x, new_y, heading)

    def step_backward(self, velocity):
        """
        One step backward.
        """
        x, y, heading = self.agent.get_position()

        direction_x = math.sin(math.radians(heading))
        direction_y = math.cos(math.radians(heading))

        new_x = x - direction_x * velocity
        new_y = y - direction_y * velocity

        self.agent.set_position(new_x, new_y, heading)

    def turn_right(self, angular_velocity):
        x, y, heading = self.agent.get_position()
        new_heading = (heading - angular_velocity) % 360
        self.agent.set_position(x, y, new_heading)

    def turn_left(self, angular_velocity):
        x, y, heading = self.agent.get_position()
        new_heading = (heading + angular_velocity) % 360
        self.agent.set_position(x, y, new_heading)

    # =============================================================================
    # Helper functions
    # =============================================================================
    def process_user_input(self, pressed_keys):
        """
        Process user keyboard input.

        Args:
            pressed_keys (Pygame Keyboard Codes)
        """
        if pressed_keys[pygame.K_UP]:
            self.step_forward(self.config['default_velocity'])

        if pressed_keys[pygame.K_DOWN]:
            self.step_backward(self.config['default_velocity'])

        if pressed_keys[pygame.K_LEFT]:
            self.turn_left(self.config['default_angular_velocity'])

        if pressed_keys[pygame.K_RIGHT]:
            self.turn_right(self.config['default_angular_velocity'])
