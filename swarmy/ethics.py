# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   07/04/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
The Module defines the ethical values for an agent.
"""

# =============================================================================
# Class
# =============================================================================
class Ethics():
    """
    The object is responsible for the ethical values of an agent.
    To establish the link between micro and macro and to be able to perform as one unit 
    the agents in the swarm need to have a common basis of values.
    All agents commit to be part of the swarm and to act as one unit.   
    
    Args:
        i (Interaction): interaction unit        
    """
    def __init__(self, i):
        """
        Initialize ethics module.
        """          
        # variables
        self.nesting = i
        self.groupID = 0 		# defines which swarm the agents belong to