# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   15/02/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
This module represents an item in the environment.
"""

# =============================================================================
# Imports
# =============================================================================
import pygame

# =============================================================================
# Classes
# =============================================================================
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Source():
    """
    The Source item represents a food source. 
    The agents can pick up a token item (food) from the source.
    
    Args:
        e (environemnt): corresponding environment
        x (int): x-Axis position
        y (int): y-Axis position            
        w (int): display width
        h (int): display height
        b (int): border width
        t (int): number of tokens    
    """       
    def __init__(self, i, e, x, y, w, h, b, t):
        """
        Initialize a Source item.
        """        
        self.ID = i
        self.environment = e  
        self.color = (169, 0, 19)
        self.colorToken = (181,111,0)              # orange
        self.rect = pygame.Rect(0, 0, w, h)        # to track the surface position
        self.rect.centerx = x
        self.rect.centery = y
        self.border = b
        self.tokens = [] # tokens in source
        
        # fill tokens to list
        for n in range(t):
            self.tokens.append("T" + str(n+1))
        
        # needed for token visualization
        offsetX = self.rect.left + w/2
        offsetY = self.rect.top + h/2
        self.tokenPositionList = []
        self.tokenPositionList.append((offsetX - 20, offsetY - 5))
        self.tokenPositionList.append((offsetX - 10, offsetY - 5))
        self.tokenPositionList.append((offsetX + 00, offsetY - 5))
        self.tokenPositionList.append((offsetX + 10, offsetY - 5))
        self.tokenPositionList.append((offsetX + 20, offsetY - 5))
        self.tokenPositionList.append((offsetX - 20, offsetY + 5))
        self.tokenPositionList.append((offsetX - 10, offsetY + 5))
        self.tokenPositionList.append((offsetX + 00, offsetY + 5))
        self.tokenPositionList.append((offsetX + 10, offsetY + 5))
        self.tokenPositionList.append((offsetX + 20, offsetY + 5))

        # add sink to environemt
        self.environment.staticRectList.append([self.color, self.rect, self.border])
        
        # visualize tokens in simulation
        for tokenPosition in self.tokenPositionList:
            self.environment.staticCircList.append([self.colorToken, tokenPosition, 3])

    def getNumberOfTokens(self):        
        return len(self.tokens)

    def decrementTokens(self):
        """
        Get and remove one token from list by FIFO principle.
        Call function only if tokens are available in source.
    
        Returns:
            token (string): token information           
        """        
        # update source visualization
        self.environment.staticCircList.remove([self.colorToken, self.tokenPositionList[len(self.tokens)-1], 3])
        return self.tokens.pop(0)
    
    def printTokens(self):
        """
        Print all tokens in source.
        """
        print("\n------------------------------------")
        tks = ""
        tks = tks + "Tokens in source " + str(self.ID) + ": "     
        if(len(self.tokens) > 0):
            for t in self.tokens[:-1]:
               tks = tks + t + ", "
            tks = tks + self.tokens[-1] # add last element without comma
           
        print(tks)
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Sink():
    """
    The Sink item represents a nest
    
    Args:
        e (environemnt): corresponding environment
        x (int): x-Axis position
        y (int): y-Axis position            
        w (int): display width
        h (int): display height
        b (int): border width
    """  
    def __init__(self, i, e, x, y, w, h, b):
        """
        Initialize a Sink item.
        """
        self.ID = i
        self.environment = e                
        self.color = (23, 98, 144)
        self.colorToken = (181,111,0)        # yellow
        self.rect = pygame.Rect(0, 0, w, h)        # to track the surface position
        self.rect.centerx = x
        self.rect.centery = y
        self.border = b      
        self.tokens = [] # tokens in sink

        offsetX = self.rect.left + w/2
        offsetY = self.rect.top + h/2
        self.tokenPositionList = []
        self.tokenPositionList.append((offsetX - 20, offsetY - 5))
        self.tokenPositionList.append((offsetX - 10, offsetY - 5))
        self.tokenPositionList.append((offsetX + 00, offsetY - 5))
        self.tokenPositionList.append((offsetX + 10, offsetY - 5))
        self.tokenPositionList.append((offsetX + 20, offsetY - 5))
        self.tokenPositionList.append((offsetX - 20, offsetY + 5))
        self.tokenPositionList.append((offsetX - 10, offsetY + 5))
        self.tokenPositionList.append((offsetX + 00, offsetY + 5))
        self.tokenPositionList.append((offsetX + 10, offsetY + 5))
        self.tokenPositionList.append((offsetX + 20, offsetY + 5))

        # add sink to environemt
        self.environment.staticRectList.append([self.color, self.rect, self.border])

    def getNumberOfTokens(self):        
        return len(self.tokens)

    def incrementTokens(self, token):
        """
        Increment number of tokens and add new token to list.
    
        Args:
            token (string): piece of information
        """        
        if(not (token in self.tokens)): # if it is a new token in sink
            self.environment.staticCircList.append([self.colorToken, self.tokenPositionList[len(self.tokens)], 3])
            self.tokens.append(token)
        
    def printTokens(self):
        """
        Print all tokens in sink.
        """
        print("\n------------------------------------")
        
        tks = ""
        tks = tks + "Tokens in sink " + str(self.ID) + ": "     
        if(len(self.tokens) > 0):
            for t in self.tokens[:-1]:
               tks = tks + t + ", "
            tks = tks + self.tokens[-1] # add last element without comma
           
        print(tks)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------        
class Obstacle():
    """
    The Obstacle item represents a barrier for an agent. 
    The agents can't walk through this kind of obstacle
    
    Args:
        e (environemnt): corresponding environment            
        x (int): x-Axis position
        y (int): y-Axis position
        w (int): obstacle width
        h (int): obstacle height
        c (int,int,int): obstacle color   
        b (int): border width
    
    """       
    def __init__(self, e, x, y, w, h, b):
        """
        Initialize a Source item.
        """   
        self.environment = e
        self.color = (0, 0, 0)      
        self.rect = pygame.Rect(0, 0, w, h)        # to track the surface position
        self.rect.centerx = x
        self.rect.centery = y
        self.border = b

        # add obstacle to environemt
        self.environment.staticRectList.append([self.color, self.rect, self.border])

 