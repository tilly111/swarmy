# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   25/04/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
This module implements the innate behavior of an agent.
"""

# =============================================================================
# Class
# =============================================================================
class Innate():
    """
    The innate object represents the inherent skills that the agent already has from the start.
    
    Args:
        p (Processing): processing unit
    """    
    def __init__(self, p):
        """
        Initialize innate object.
        """    
        self.processing = p
        self.agent = self.processing.agent
        self.comm = self.agent.nesting.communication

    def wait(self):
        """
        Do not perform any action, do nothing, just wait.
        """   
        self.agent.processing.monitoring["rewards"] += -1         # punishment for just waiting          
    
    def explore(self):
        """
        Move on or turn if collision detected.
        """           
        # either turn or move 
        if(not self.agent.actuation.turn()):

            self.agent.actuation.stepForward() 
                  
            # if a step forward leads to a collision --> step back and start turning
            if(self.agent.perception.collisionSensor()):
                self.processing.monitoring["collisions"] += 1 
                self.agent.actuation.stepBackward()
                self.agent.actuation.turnRandom()         
        
    def forage(self):
        """
        Collect token from a source and discard the collected token in a sink
        """   
        numberOfTokens = len(self.agent.nesting.communication.tokens)
        
        if(numberOfTokens == 0):                                                    # agent is able to collect a new token
            tokenDetected,  affectedSource = self.agent.perception.sourceSensor()   # check if the agent is in the source to collect a token 
            if(tokenDetected): 
                self.agent.actuation.collectToken(affectedSource)
        else:                                                                       # agent is able to discard a token
            sinkDetected,  affectedSink = self.agent.perception.sinkSensor()        # check if the agent is in the sink to discard a token
            if(sinkDetected):
                self.agent.actuation.discardToken(affectedSink)

    def communicate(self):
        """
        Process incoming messages and broadcast token if available.
        """           
        self.comm.processIncomingMessages()
        if(len(self.comm.tokens) > 0 and self.comm.remainingBroadcastingSteps == 0):   # if agent has token and no ongoing communication
            self.comm.publishToken()        
        self.comm.broadcast()           # broadcasting update
        
