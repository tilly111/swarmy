# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   15/02/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
This module is the base class for all sensors of an agent.
"""

# =============================================================================
# Imports
# =============================================================================
from abc import ABC, abstractmethod


# =============================================================================
# Class
# =============================================================================
class Perception(ABC):
    """
    The perception object is the base class for a sensor of an agent.
    Each sensor is a subclass that implements sensor().

    Args:
        agent (agent.py): instance of the agent
        environment (environment.py): instance of the environment
    """
    def __init__(self, agent, environment):
        """
        Initialize perception object.
        """
        self.agent = agent
        self.environment = environment

    @abstractmethod
    def sensor(self):
        print('Sensor not implemented')
