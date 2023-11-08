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
import numpy as np

from .perception import Perception
from .actuation import Actuation
from .body import Body
from .processing import Processing


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
    def __init__(self, p, d, e, id, controller, track):
        """
        Initialize agent object.
        """
        # environment and other objects. This variables are only needed for simulation calculations and are not needed from the agents point of view
        self.agent_id = id
        self.track = track
        self.visited = np.zeros((100, 100))

        self.environment = e

        # instantiate agent parts
        self.body = Body(self, p, controller)
        self.perception = Perception(self, e)
        self.actuation = Actuation(self, p, d)
        self.processing = Processing(self, controller)







