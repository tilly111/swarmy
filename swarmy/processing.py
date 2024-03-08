# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   15/02/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
This module includes all computation procedures of an agent, e.g. its behavior in perform()
"""

# =============================================================================
# Imports
# =============================================================================

# =============================================================================
# Class
# =============================================================================
class Processing():
    """
    In the processing object all computation procedures of an agent are represented.
    
    Args:
        a (agent.py): instance of the agent
    """    
    def __init__(self, a):
        """
        Initialize processing object.
        """    
        self.agent = a

    def perform(self, pressedKeys):
        """
        Update agent processing for one timestep
        """     
        #self.agent.actuation.stepForward()
        #self.agent.actuation.fear()
        #self.agent.actuation.aggression()
        self.agent.actuation.processUserInput(pressedKeys)
        self.agent.actuation.torus()
        self.agent.actuation.controller()


    
        
        
        
    
        
        