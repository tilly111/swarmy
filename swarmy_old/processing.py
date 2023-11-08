# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   15/02/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
This module includes all computation procedures of an agent.
"""

# =============================================================================
# Imports
# =============================================================================
import itertools
from .innate import Innate
from .learning_not_needed import Learning

# =============================================================================
# Class
# =============================================================================
class Processing():
    """
    In the processing object all computation procedures of an agent are represented.
    
    Args:
        a (agent.py): instance of the agent
        t (int):    ToF turn distance
    """    
    def __init__(self, a):
        """
        Initialize processing object.
        """    
        self.agent = a
        
        # current agent state
        self.state = {
            "processing state":  0,  # Current processing state --> 
            "carries token":     0,  # Does the agent carry a token? --> boolean {0:no 1:yes}
            "source detected":   0,  # Has the agent detected a source? --> boolean {0:no 1:yes}
            "sink detected":     0,  # Has the agent detected a sink? --> boolean {0:no 1:yes}    
            "token detected":    0   # Has the agent detected a token in a sink? --> boolean {0:no 1:yes}    
        }

        # possible values for each substate
        self.stateValues = [[0,1], [0,1], [0,1], [0,1]]        
        
         # list of tuples that represent all combinations for the state
        self.stateCombinations = list(itertools.product(*self.stateValues)) # cartesian product

        # self monitoring
        self.monitoring = {
            "rewards":          0,       # Current rewards
            "cumulatedRewards": 0,       # Cumulated rewards      
            "collisions":       0        # How many collisions had the agent?
        }
        
        self.actionCodes = {
            "move forward":    0,  # Does the agent carry a token?
            "collect token":   1,  # Has the agent detected a source?
            "discard token":   2,  # Has the agent detected a sink?    
            "wait":            3   # Has the agent detected a token in a sink?                
        }
                
               
        # instantiate processing units
        self.innate = Innate(self)
        self.learning = Learning(self)
        

    def perform(self, pressedKeys):
        """
        Update agent processing for one timestep
        """     
        
        # control the agent with ID=1 via keyboard
        #if(self.agent.ID == 1):
        self.agent.actuation.processUserInput(pressedKeys)         
        
        # --- self monitoring ---
        self.selfMonitoring()
        
        # --- innate behaviour ---
        self.innate.communicate()        
        self.innate.explore()
        self.innate.forage()
        
        # --- learning procedure ---
        #self.learning.rl_qLearning()
        
        
    def selfMonitoring(self):
        # self-monitoring status
        if(self.agent.nesting.communication.tokens): # if agent has tokens 
            self.agent.processing.state["carries token"] = 1
        else:
            self.agent.processing.state["carries token"] = 0
        
        