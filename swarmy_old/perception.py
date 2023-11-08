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
import pygame

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
        Collision sensor:       Detects collisions with objects or other agents.
        Source sensor:          Detects sources where tokens can be collected.
        Sink sensor:            Detects sinks where tokens can be discarded.
        Time-of-Flight sensor:  Measures the distance in front the agent to the next object in the environment. The sensor is available as a 1D or 2D sensor.
    
    """
    def __init__(self, a):
        """
        Initialize perception object.
        """    

        # constants
        self.TOF_MAX = 1000                # choose even number

        # variables        
        self.agent = a
        self.otherAgentRects = []
        self.obstacleRects = []    
       
        # important to initially calculate collisions when instatiating the agents
        self.helperOAO()
        
    def collisionSensor(self):
        """
        Collision sensor returns true when a collision with the bounding rectangle is detected
        
        Returns:
            collisionObserved (boolean): True = collision, False = no collision 
        """
        agentRect = self.agent.body.rect
        testbedWidth = self.agent.environment.width
        testbedHeight = self.agent.environment.height
        
        collisionObserved = False
        
        # check collision with the testbed wall
        if(agentRect.left <= 0 or agentRect.right >= testbedWidth or agentRect.top <= 0 or agentRect.bottom >= testbedHeight):
            collisionObserved = True
        
        # check collision with an obstacle
        elif(self.agent.body.rect.collidelistall(self.obstacleRects)):
            collisionObserved = True
        
        # check collision due to other agents
        elif(self.agent.body.rect.collidelistall(self.otherAgentRects)):
            collisionObserved = True
            
        return collisionObserved
 

    def sourceSensor(self):
        """
        Sensor can detect a source from which a token can be taken
        
        Returns:
            tokenDetected (boolean): True = token detected, False = no token 
            affectedSource (source)
        """
        tokenDetected = False
        affectedSource = None
        
        self.agent.processing.state["source detected"] = 0
        self.agent.processing.state["token detected"] = 0      
        
        # iterate through all possible sources
        for source in self.agent.sources:
            # check if the source has tokens left and if the agent is in contact with the source
            if(self.agent.body.rect.colliderect(source)):
                self.agent.processing.state["source detected"] = 1            
                if(source.getNumberOfTokens() > 0):
                    self.agent.processing.state["token detected"] = 1  
                    tokenDetected = True
                    affectedSource = source
                                                    
        return tokenDetected, affectedSource
        
    
    def sinkSensor(self):
        """
        Sensor can detect a sink in which a token can be placed
        
        Returns:
            sinkDetected (boolean): True = sink detected, False = no sink 
            affectedSink (source)
        """
        sinkDetected = False
        affectedSink = None
        
        # iterate through all possible sources
        for sink in self.agent.sinks:
            if(self.agent.body.rect.colliderect(sink)):
                self.agent.processing.state["sink detected"] = 1  
                sinkDetected = True
                affectedSink = sink
            else:
                self.agent.processing.state["sink detected"] = 0  
                
        return sinkDetected, affectedSink
         

    def tofLaserSensor1D(self):
        """
        Measure the distance in one dimension.
    
        Args:
            rendering (boolean): visualize sensor if true
    
        Returns:
            distance (int): distance in mm     
        """
        
        # helper list to identify shortest distance to objects
        currDistance = self.TOF_MAX  # start with max distance
        collisionPoint = pygame.Vector2()
        
        # ---------------------
        # start point of ToF-Sensor
        v = pygame.Vector2()
        v.x = self.agent.actuation.position[0] + self.agent.actuation.direction[0]*self.agent.body.HEIGHT/2
        v.y = self.agent.actuation.position[1] + self.agent.actuation.direction[1]*self.agent.body.HEIGHT/2
        
        # end point of ToF-Sensor
        v2 = pygame.Vector2()
        v2.x = self.agent.actuation.position[0] + self.agent.actuation.direction[0]*(self.TOF_MAX+self.agent.body.HEIGHT/2)
        v2.y = self.agent.actuation.position[1] + self.agent.actuation.direction[1]*(self.TOF_MAX+self.agent.body.HEIGHT/2)
        
        
        # calculate the distance to obstacles and add results to list
        for o in self.agent.obstacles:
            x = o.rect.clipline(v.x, v.y, v2.x, v2.y)
            if(x): # if a collision detected
                d = v.distance_to(x[0])
                if(d < currDistance):
                    currDistance = d
                    collisionPoint = x[0]
        
        # calculate the distance to other agents and add results to list
        for agent in self.agent.agents:
            x = agent.body.rect.clipline(v.x, v.y, v2.x, v2.y)
            if(self.agent.ID != agent.ID and x): # if a collision detected
                d = v.distance_to(x[0])
                if(d < currDistance):
                    currDistance = d
                    collisionPoint = x[0]                
                
        for w in self.agent.environment.wall:
            x = w.clipline(v.x, v.y, v2.x, v2.y)
            if(x): # if a collision detected
                d = v.distance_to(x[0])
                if(d < currDistance):
                    currDistance = d
                    collisionPoint = x[0]              
         
                
        # visualize ToF-Laser for testing
        rendering = False
        if (rendering == True):
            if(currDistance < self.TOF_MAX):
                self.agent.environment.dynamicLineList.append(["RED", v, collisionPoint])
            else:
                self.agent.environment.dynamicLineList.append(["BLUE", v, v2])
       
            
        currDistance = round(currDistance)    
        #print(currDistance) 
        
        return currDistance


    def tofLaserSensor2D(self):
        """
        Measure the distance in one dimension.
    
        Args:
            rendering (boolean): visualize sensor if true
    
        Returns:
            distance (int): distance in mm
        """
        
        # helper list to identify shortest distance to objects
        currDistance = self.TOF_MAX  # start with max distance
        currDistance2 = self.TOF_MAX  # start with max distance
        collisionPoint = pygame.Vector2()
        collisionPoint2 = pygame.Vector2()

        # start point of ToF-Sensor
        # vector perpedicular to direction


        v = pygame.Vector2()
        v.x = self.agent.actuation.position[0] + self.agent.actuation.direction[0]*self.agent.body.HEIGHT/2 + -self.agent.actuation.direction[1]*5
        v.y = self.agent.actuation.position[1] + self.agent.actuation.direction[1]*self.agent.body.HEIGHT/2 + self.agent.actuation.direction[0]*5
        
        v2 = pygame.Vector2()
        v2.x = self.agent.actuation.position[0] + self.agent.actuation.direction[0]*(self.TOF_MAX+self.agent.body.HEIGHT/2) + -self.agent.actuation.direction[1]*5
        v2.y = self.agent.actuation.position[1] + self.agent.actuation.direction[1]*(self.TOF_MAX+self.agent.body.HEIGHT/2) + self.agent.actuation.direction[0]*5

        w = pygame.Vector2()
        w.x = self.agent.actuation.position[0] + self.agent.actuation.direction[0]*self.agent.body.HEIGHT/2 + self.agent.actuation.direction[1]*5
        w.y = self.agent.actuation.position[1] + self.agent.actuation.direction[1]*self.agent.body.HEIGHT/2 + -self.agent.actuation.direction[0]*5
        
        w2 = pygame.Vector2()
        w2.x = self.agent.actuation.position[0] + self.agent.actuation.direction[0]*(self.TOF_MAX+self.agent.body.HEIGHT/2) + self.agent.actuation.direction[1]*5
        w2.y = self.agent.actuation.position[1] + self.agent.actuation.direction[1]*(self.TOF_MAX+self.agent.body.HEIGHT/2) + -self.agent.actuation.direction[0]*5
        
        
        
        # calculate the distance to obstacles and add results to list
        for o in self.agent.obstacles:
            x = o.rect.clipline(v.x, v.y, v2.x, v2.y)
            x2 = o.rect.clipline(w.x, w.y, w2.x, w2.y)
            
            if(x): # if a collision detected
                d = v.distance_to(x[0])
                if(d < currDistance):
                    currDistance = d
                    collisionPoint = x[0]
            
            if(x2): # if a collision2 detected
                d2 = w.distance_to(x2[0])
                if(d2 < currDistance2):
                    currDistance2 = d2
                    collisionPoint2 = x2[0]
                    
        # calculate the distance to other agents and add results to list
        for agent in self.agent.agents:
            x = agent.body.rect.clipline(v.x, v.y, v2.x, v2.y)
            x2 = agent.body.rect.clipline(w.x, w.y, w2.x, w2.y)
            if(self.agent.ID != agent.ID):
                if(x): # if a collision detected
                    d = v.distance_to(x[0])
                    if(d < currDistance):
                        currDistance = d
                        collisionPoint = x[0]                
                if(x2): # if a collision detected
                    d2 = w.distance_to(x2[0])
                    if(d2 < currDistance2):
                        currDistance2 = d2
                        collisionPoint2 = x2[0] 
                        
        for wall in self.agent.environment.wall:
            x = wall.clipline(v.x, v.y, v2.x, v2.y)
            x2 = wall.clipline(w.x, w.y, w2.x, w2.y)
            if(x): # if a collision detected
                d = v.distance_to(x[0])
                if(d < currDistance):
                    currDistance = d
                    collisionPoint = x[0]              

            if(x2): # if a collision detected
                d2 = w.distance_to(x2[0])
                if(d2 < currDistance2):
                    currDistance2 = d2
                    collisionPoint2 = x2[0] 
                    
        # visualize ToF-Laser for testing
        rendering = False        
        if (rendering == True):
            if(currDistance < self.TOF_MAX):
                self.agent.environment.dynamicLineList.append(["RED", v, collisionPoint])
            else:
                self.agent.environment.dynamicLineList.append(["BLUE", v, v2])
                
            if(currDistance2 < self.TOF_MAX):
                self.agent.environment.dynamicLineList.append(["RED", w, collisionPoint2])
            else:
                self.agent.environment.dynamicLineList.append(["BLUE", w, w2])    
            
        currDistance = round(currDistance)    
        currDistance2 = round(currDistance2)    
                
        #print("L1: " + str(currDistance) + " L2: " + str(currDistance2)) 
            
        return round(currDistance), currDistance2
    
    
#%% Helper functions
    
    def helperOAO(self): 
        """
        Helper function to avoid redundant calculation of other agents and obstacles-
        Store once other agents and obstacles.
        Needed e.g. for sensors and communication.
        """              
        
        # reset pre calculated other agents and obstacles to avoid multiple representations
        self.otherAgentRects = []
        self.obstacleRects = []  
        
        # other agents
        for agent in self.agent.agents:
            if(self.agent.ID != agent.ID):
                self.otherAgentRects.append(agent.body.rect)
                
        # obstacles agents                
        for obstacle in self.agent.obstacles:
            self.obstacleRects.append(obstacle.rect)
        