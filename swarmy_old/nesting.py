# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   30/05/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
This module is responsible for the micro-macro-link.
"""

# =============================================================================
# Imports
# =============================================================================
from .communication import Communication
from .spacetime import Spacetime
from .ethics import Ethics

# =============================================================================
# Class
# =============================================================================
class Nesting():
    """
    The nesting object is responsible for the micro-macro-link.
    
    Args:
        a (agent.py): instance of the agent    
    """
    def __init__(self, a):
        """
        Initialize nesting object.
        """    
        self.agent = a
        
        # instantiate interaction units
        self.communication = Communication(self)  
        self.spacetime = Spacetime(self)
        self.ethics = Ethics(self)