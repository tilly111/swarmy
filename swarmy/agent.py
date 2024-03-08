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
from .perception import Perception
#from my_sensors import MySensor
#from .actuation import Actuation
from .body import Body
from .processing import Processing
#from .actuation import Actuation
#from my_controller import MyController

# =============================================================================
# Class
# =============================================================================
class Agent():
    """
    Autonomous agent that can perceive its enviroment and interact with it.
    
    Args
        p ([int, int]): initial position
        d (int): initial direction (angle)
        e (environment.py): instance of environement class
 
    
    Attributes:
        body        (body.py):         represents the agent body
        processing  (processing.py):   represents the processing capabilites
        perception  (perception.py):   represents the sensing capabilities
        actuation   (actuation.py):    represents the actuator capabilites
    """
    def __init__(self,e,controller, sensor, config):
        """
        Initialize agent object.
        """
        # environment and other objects. This variables are only needed for simulation calculations and are not needed from the agents point of view
        self.environment = e

        # instantiate agent parts
        self.body = Body(self)
        self.perception = []
        for i in range(len(sensor)):
            self.perception.append(sensor[i](self, e, config))   #   MySensor(self, e)
        ##self.perception = sensor(self, e, config)   #   MySensor(self, e)
        self.actuation = controller(self, config)   #MyController(self, p, d)
        self.processing = Processing(self)

    def get_position(self):
        """
        Get the x-y position and direction unit vector of the agent.
        Returns:
        """
        x, y, gamma = self.actuation.position[0], self.actuation.position[1], self.actuation.angle
        return x,y, gamma

    def set_position(self, x: float, y: float, gamma:float):
        """
        Set the x-y position and direction unit vector of the agent.
        """
        self.actuation.position[0] = x
        self.actuation.position[1] = y
        self.actuation.angle = gamma







