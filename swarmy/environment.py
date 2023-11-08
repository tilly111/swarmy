# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   15/02/2021 -- 13/04/2022
# version:      0.9
# status:       prototype
# =============================================================================
"""
This module represents the physical environment.
"""

# =============================================================================
# Imports
# =============================================================================
import pygame

# =============================================================================
# Class
# =============================================================================
class Environment():
    """
    The environment object represents the simulation world of an agent.
    It is the testbed where the experiments are conducted. 
    The object expects that pygame is already initialized.
    
    Args:
        rendering (bolean): set simulation rendering on or off
    """    
    def __init__(self, rendering):
        """
        Initialize environment object.
        """     
        super(Environment, self).__init__()
        
        # Variables and constants - set screws
        self.FPS = 60  # Frames per second. A typical value is 60 frames per second
        self.BACKGROUND_COLOR = (255, 255, 255)    
        self.width = pygame.display.Info().current_w    # testbed width  // self.width = 500
        self.height = pygame.display.Info().current_h   # testbed height // self.height = 300
        
        # init basic rendering surface
        if(rendering == 1):
            if(self.width == pygame.display.Info().current_w and self.height == pygame.display.Info().current_h):   # fullscreen size
                self.displaySurface = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
            else:                                                                                                   # size smaller than fullscreen
                self.displaySurface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        elif(rendering == -1):
            self.displaySurface = pygame.display.set_mode((self.width, self.height), pygame.HIDDEN)                 # no screen
        elif(rendering == 0):
            self.displaySurface = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)                # black screen where capture images is possible

        
        # add wall
        self.wall = []
        wallWidth = 3
        self.wall.append(pygame.Rect(0, 0, self.width, wallWidth))
        self.wall.append(pygame.Rect(0, 0, wallWidth, self.height))
        self.wall.append(pygame.Rect(0, self.height-wallWidth, self.width, wallWidth))
        self.wall.append(pygame.Rect(self.width-wallWidth, 0, wallWidth, self.height))
        
        # list with objects to be plotted
        self.staticRectList = []
        self.staticCircList = []
        
        self.dynamicCircList = [] # filled circle
        self.dynamicRectList = []
        self.dynamicPolyList = []
        self.dynamicLineList = []

        self.clock = pygame.time.Clock()  # create an object to help track time


#%% Rendering and Helper functions

    def render(self):
        """
        This method is used to update the whole environment.
        """     
        self.displaySurface.fill(self.BACKGROUND_COLOR) 
                
        # draw static rects (items = sources, sinks, obstacles)
        for x in self.staticRectList:
            pygame.draw.rect(self.displaySurface, x[0], x[1], x[2])   

        # draw static circles (source and sink tokens)
        for x in self.staticCircList:
            pygame.draw.circle(self.displaySurface, x[0], x[1], x[2])

        # draw walls (environment border)     
        for x in self.wall:
            pygame.draw.rect(self.displaySurface, "BLACK", x)   
                      
        # draw dynamic polygons (agents)
        for x in self.dynamicPolyList:
            pygame.draw.polygon(self.displaySurface, (255,255,255), x[1]) # fill the polygon
            pygame.draw.polygon(self.displaySurface, x[0], x[1], 3)
            #pygame.draw.aalines(self.displaySurface, x[0], True, x[1])   
            
        # draw dynamic circles (agent tokens)
        for x in self.dynamicCircList:
            pygame.draw.circle(self.displaySurface, x[0], x[1], x[2], x[3])

        # draw rectangles
        for x in self.dynamicRectList:
            pygame.draw.rect(self.displaySurface, x[0], x[1], x[2])   

        for x in self.dynamicLineList:
            pygame.draw.line(self.displaySurface, x[0], x[1], x[2])

        # reset dynamic buffers
        self.resetDynamicBuffers()                  

        # update content on display and enforce given frames per second
        pygame.display.flip()                       
        self.forceFramerate()       

       
    def resetDynamicBuffers(self):
        self.dynamicCircList = []
        self.dynamicRectList = []
        self.dynamicPolyList = []
        self.dynamicLineList = []
            
    def getDisplay(self):
        """
        Get current display (window).
        """     
        return self.displaySurface

    def forceFramerate(self):
        """
        This method is used once per frame to enforce a fixed number of frames per second.
        It will delay the simulation to get the desired fps.
        """
        self.clock.tick(self.FPS)  # every second at most fps frames should pass.
        #self.clock.tick_busy_loop(fps)  # more accurate to ensure fps than tick but need more CPU computation power

    def printFPS(self):
        """
        Compute frames per second by averaging the last ten Clock.tick()
        """
        print("\n------------------------------------")    
        print("Frames per second: " + str(self.clock.get_fps()))
        
        
        
        
        