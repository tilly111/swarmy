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
# Class
# =============================================================================
class Processing():
    """
    In the processing object all computation procedures of an agent are represented.

    Args:
        agent (agent.py): instance of the agent
    """
    def __init__(self, agent):
        """
        Initialize processing object.
        """
        self.agent = agent

    def perform(self, pressed_keys):
        """
        Update agent processing for one timestep
        """
        self.agent.actuation.process_user_input(pressed_keys)
        self.agent.actuation.torus()
        self.agent.actuation.controller()
