# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   15/02/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
This module includes all perception possibilites of an agent.
"""

# =============================================================================
# Imports
# =============================================================================
from abc import abstractmethod

import pygame
import math
# =============================================================================
# Class
# =============================================================================
class Perception():
    """
    The perception object represents the all sensing capabilites of an agent.
    All sensors will be defined here. 
        
    Args:
        a (agent.py): instance of the agent    
    
    Available sensors:
        Your light sensor
    
    """
    def __init__(self, a, e):
        
        """
        Initialize perception object.
        """    

        # variables        
        self.agent = a
        self.env = e


    @abstractmethod
    def Sensor(self):
        print('Sensor not implemented')




 

       
