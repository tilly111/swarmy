# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   15/02/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
This module represents an agent in the environment.
"""

# =============================================================================
# Imports
# =============================================================================
from abc import ABC, abstractmethod

from .body import Body
from .processing import Processing


# =============================================================================
# Class
# =============================================================================
class Agent(ABC):
    """
    Autonomous agent that can perceive its environment and interact with it.

    Args:
        environment (environment.py): instance of the environment class
        controller (class): controller class, a subclass of Actuation
        sensors (list): sensor classes, subclasses of Perception
        config (dict): simulation configuration from config.yaml

    Attributes:
        body        (body.py):         represents the agent body
        processing  (processing.py):   represents the processing capabilities
        perception  (perception.py):   represents the sensing capabilities
        actuation   (actuation.py):    represents the actuator capabilities
    """
    def __init__(self, environment, controller, sensors, config):
        """
        Initialize agent object.
        """
        # environment and other objects. These variables are only needed for simulation calculations and are not needed from the agent's point of view
        self.environment = environment
        self.unique_id = None
        # instantiate agent parts
        self.body = Body(self)
        self.perception = []
        for sensor in sensors:
            self.perception.append(sensor(self, environment, config))
        self.actuation = controller(self, config)
        self.processing = Processing(self)
        self.config = config

    @abstractmethod
    def initial_position(self):
        """
        Define the initial position of the agent.
        """
        print('initial position not implemented')

    @abstractmethod
    def save_information(self, last_robot):
        """
        Save information of the agent, e.g. trajectory or the environmental plot.
        last_robot is True for the last agent, e.g. to save a shared image once.
        """
        print('save information not implemented')

    def get_position(self):
        """
        Get the x-y position and heading (in degrees) of the agent.
        """
        x, y, heading = self.actuation.position[0], self.actuation.position[1], self.actuation.heading
        return x, y, heading

    def set_position(self, x: float, y: float, heading: float):
        """
        Set the x-y position and heading (in degrees) of the agent.
        """
        self.actuation.position[0] = x
        self.actuation.position[1] = y
        self.actuation.heading = heading

    def get_perception(self):
        """
        Get the ID of the agent followed by the value of each sensor.
        """
        sensor_values = [self.unique_id]
        for sensor in self.perception:
            sensor_values.append(sensor.sensor())
        return sensor_values
