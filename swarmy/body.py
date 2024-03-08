# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   15/02/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
This module represents the body of an agent.
"""

# =============================================================================
# Imports and Variables
# =============================================================================
import pygame
import math
import numpy as np

# Helper variable
polyRotatedLookUp = [] # the table reduces computation steps to improves rendering speed

# =============================================================================
# Class
# =============================================================================
class Body():
    """
    The body is the visual representation of an agent in the simulation.    
    The object defines the dimensions and the position of an agent in the environment.
    
    Args:
        a (agent.py): instance of the agent
        p ([int, int]): initial center position
    """
    def __init__(self, a):
        """
        Initialize body object.
        """    
        super(Body, self).__init__()
        
        # constants
        self.WIDTH = 24                 # agent body width
        self.HEIGHT = 10                # agent body height
        self.COLOR = (0,90,90)          # turquoise
        self.BOUNDING = round(np.hypot(self.WIDTH, self.HEIGHT))+20
        
        # variables
        self.agent = a
        
        # initial position with agent center in coordinate system origin
        wheelDist = 8        # helper variable to calculate the agent body
        motorDist = 3        # helper variable to calculate the agent body
        ratioBodyWheel = 6   # helper variable to calculate the agent body  
        v1 = pygame.Vector2(-self.WIDTH/ratioBodyWheel/2-self.WIDTH/2-wheelDist, -self.HEIGHT*2/2)  
        v2 = pygame.Vector2(self.WIDTH/ratioBodyWheel/2-self.WIDTH/2-wheelDist, -self.HEIGHT*2/2)
        v3 = pygame.Vector2(self.WIDTH/ratioBodyWheel/2-self.WIDTH/2-wheelDist, -self.HEIGHT/2+motorDist)
        v4 = pygame.Vector2(-self.WIDTH/2, -self.HEIGHT/2+motorDist)  
        v5 = pygame.Vector2(-self.WIDTH/2, -self.HEIGHT/2)        
        v6 = pygame.Vector2(self.WIDTH/2, -self.HEIGHT/2)
        v7 = pygame.Vector2(self.WIDTH/2, -self.HEIGHT/2+motorDist)
        v8 = pygame.Vector2(-self.WIDTH/ratioBodyWheel/2+self.WIDTH/2+wheelDist, -self.HEIGHT/2+motorDist) 
        v9 = pygame.Vector2(-self.WIDTH/ratioBodyWheel/2+self.WIDTH/2+wheelDist, -self.HEIGHT*2/2)
        v10 = pygame.Vector2(self.WIDTH/ratioBodyWheel/2+self.WIDTH/2+wheelDist, -self.HEIGHT*2/2)
        v11 = pygame.Vector2(self.WIDTH/ratioBodyWheel/2+self.WIDTH/2+wheelDist, self.HEIGHT*2/2)
        v12 = pygame.Vector2(-self.WIDTH/ratioBodyWheel/2+self.WIDTH/2+wheelDist, self.HEIGHT*2/2)  
        v13 = pygame.Vector2(-self.WIDTH/ratioBodyWheel/2+self.WIDTH/2+wheelDist, self.HEIGHT/2-motorDist)
        v14 = pygame.Vector2(self.WIDTH/2, self.HEIGHT/2-motorDist)
        v15 = pygame.Vector2(self.WIDTH/2, self.HEIGHT/2)
        v16 = pygame.Vector2(-self.WIDTH/2, self.HEIGHT/2)        
        v17 = pygame.Vector2(-self.WIDTH/2, self.HEIGHT/2-motorDist)
        v18 = pygame.Vector2(self.WIDTH/ratioBodyWheel/2-self.WIDTH/2-wheelDist, self.HEIGHT/2-motorDist)
        v19 = pygame.Vector2(self.WIDTH/ratioBodyWheel/2-self.WIDTH/2-wheelDist, self.HEIGHT*2/2)
        v20 = pygame.Vector2(-self.WIDTH/ratioBodyWheel/2-self.WIDTH/2-wheelDist, self.HEIGHT*2/2)
        
        self.polyRef = [v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16,v17,v18,v19,v20]  # coordinates for reference polygon
        self.polyCur = []             # coordinates for current polygon
  
        # init bounding rect
        self.rect = pygame.Rect(0, 0, self.BOUNDING, self.BOUNDING)
        self.rect.centerx = 0#p[0]
        self.rect.centery = 0#p[1]
           
        
#%% Rendering and Helper functions
    
    def render(self):
        """
        Render body orientation and position & Update token
        """ 
        global polyRotatedLookUp
        self.polyCur = []
        # use precalculated rotations and add position vector
        for p in polyRotatedLookUp[self.agent.actuation.angle-1]:
            self.polyCur.append(p + self.agent.actuation.position)
        self.agent.environment.dynamicPolyList.append([self.COLOR, self.polyCur, 3])

        # --- Old Approach without lookup table ---
        # rotate polygon according to current angle and add position vector
        # ang = math.radians(self.agent.actuation.angle)
        # turnMat = [[np.cos(ang),-np.sin(ang)],[np.sin(ang),np.cos(ang)]]
        # for p in self.polyRef:
        #     self.polyCur.append(np.matmul(p,turnMat) + self.agent.actuation.position)
        # self.agent.environment.dynamicPolyList.append([self.COLOR, self.polyCur, 3])

        # Debug mode: show bounding rect
        # self.agent.environment.dynamicRectList.append([self.COLOR, self.rect, 3]) 
        
        # update token visualization
        ##if(self.agent.nesting.communication.tokens): # if agent carries a token
        ##    self.agent.environment.dynamicCircList.append([self.TOKEN_COLOR, self.agent.actuation.position, 3, 10])      


    def helperLUT(self):
        """
        Calculates a lookup table for the rotation of an agent to improve rendering performance.
        The lookup table is not relevant for logic performance (when simulating without drawing on a display).
        The results are stored in a global variable, so that the calculation has only to be performed once.
        """         
        global polyRotatedLookUp
        for x in range(360):
            ang = math.radians(x+1)
            turnMat = [[np.cos(ang),-np.sin(ang)],[np.sin(ang),np.cos(ang)]]
            
            self.polyCur = []
            for p in self.polyRef:
                self.polyCur.append(np.matmul(p,turnMat) + ([int(0), int(0)]))
            polyRotatedLookUp.append(self.polyCur)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            