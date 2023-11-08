# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   15/02/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
The Module is responsible for swarm coordination in space and time.
"""

# =============================================================================
# Class
# =============================================================================
class Spacetime():
    """
    The object is responsible for the coordination of an agent in a swarm in space and time.   
        
    Args:
        i (Interaction): interaction unit
    """
    def __init__(self, i):
        """
        Initialize spacetime module.
        """          
        # variables
        self.nesting = i