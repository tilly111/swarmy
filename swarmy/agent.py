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
from .actuation import Actuation
from .body import Body
from .processing import Processing
from .nesting import Nesting
from .energy import Energy

# =============================================================================
# Class
# =============================================================================
class Agent():
    """
    Autonomous agent that can perceive its enviroment and interact with it.
    
    Args:
        i (int): agent ID
        p ([int, int]): initial position
        d (int): initial direction (angle)
        e (environment.py): instance of environement class
        a (agent.py): list with agents
        c (itme.py):  list with sources
        s (item.py):  list with sinks
        o (item.py):  list with obstacles    
        x (int):      specific experimental parameters
    
    Attributes:
        body        (body.py):         represents the agent body
        energy      (energy.py):       represents the energy consumption
        processing  (processing.py):   represents the processing capabilites
        perception  (perception.py):   represents the sensing capabilities
        actuation   (actuation.py):    represents the actuator capabilites
        nesting     (nesting.py):      represents the micro-macro-link
    """

    def __init__(self, i, p, d, e, a, c, s, o, x):
        """
        Initialize agent object.
        """
        # experiment variables
        self.xParams = x

        # attributes
        self.ID = i

        # environment and other objects. This variables are only needed for simulation calculations and are not needed from the agents point of view
        self.environment = e
        self.agents = a
        self.sources = c
        self.sinks = s
        self.obstacles = o
            
        # instantiate agent parts
        self.body = Body(self, p)
        self.perception = Perception(self)
        self.actuation = Actuation(self, p, d)
        self.nesting = Nesting(self)
        self.processing = Processing(self)
        self.energy = Energy(self)





