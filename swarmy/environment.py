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
from swarmy.item import Item
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
        self.width = 1000  #pygame.display.Info().current_w
        self.height = 1000  #pygame.display.Info().current_h
        
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

        # use the space below to add structures like walls or obstacles, e.g. via the function pygame.Rect
        self.structure = []
        # list with objects to be plotted
        self.staticRectList = []
        self.staticCircList = []

        self.staticVisitedList = []

        self.sensor_rays = []
        
        self.dynamicPolyList = []

        self.dynamicObstacles = []  # body of the robots
        self.dynamicItems = []

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

        # draw visited things TODO does this makes sense??
        for x in self.staticVisitedList:
            pygame.draw.rect(self.displaySurface, x[0], x[1], x[2])
                      
        # draw dynamic polygons (agents)
        for x in self.dynamicPolyList:
            pygame.draw.polygon(self.displaySurface, (255,255,255), x[1])  # fill the polygon
            pygame.draw.polygon(self.displaySurface, x[0], x[1], 3)

        for x in self.dynamicObstacles:
            pygame.draw.rect(self.displaySurface, (255, 0, 0), x, 3)

        for x in self.dynamicItems:
            pygame.draw.circle(self.displaySurface, x.color, (x.rect.centerx, x.rect.centery), x.radius, 0)

        # TODO make dynamic draw rays
        for r in self.sensor_rays:
            pygame.draw.line(self.displaySurface, (255, 0, 0), pygame.Vector2(r[0], r[1]), pygame.Vector2(r[2], r[3]))
        self.sensor_rays.clear()
        # reset dynamic buffers
        self.resetDynamicBuffers()                  

        # update content on display and enforce given frames per second
        pygame.display.flip()                       
        self.forceFramerate()       

    def resetDynamicBuffers(self):
        self.dynamicCircList = []
        self.dynamicPolyList = []

    def resetDynamicObstacles(self):
        self.dynamicObstacles = []
        self.dynamicItems = []
            

    def forceFramerate(self):
        """
        This method is used once per frame to enforce a fixed number of frames per second.
        It will delay the simulation to get the desired fps.
        """
        self.clock.tick(self.FPS)  # every second at most fps frames should pass.
        #self.clock.tick_busy_loop(fps)  # more accurate to ensure fps than tick but need more CPU computation power