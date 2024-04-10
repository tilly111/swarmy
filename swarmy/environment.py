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
import numpy as np
from abc import abstractmethod

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
    def __init__(self, config):
        """
        Initialize environment object.
        """     
        super(Environment, self).__init__()
        
        # Variables and constants - set screws
        self.FPS = config['FPS']
        self.BACKGROUND_COLOR = config['background_color']
        self.width = config['world_width'] #pygame.display.Info().current_w
        self.height = config['world_height'] #pygame.display.Info().current_h
        self.config = config
        
        # list with objects to be plotted
        self.staticRectList = []
        self.staticCircList = []
        self.dynamicCircList = []
        self.dynamicPolyList = []
        self.dynamicLineList = []
        self.dynamicRectList = []
        self.agentlist = []
        self.agent_object_list = []
        self.bumper_object_list = []

        self.clock = pygame.time.Clock()  # create an object to help track time
        self.add_static_rectangle_object()
        self.add_static_circle_object()
        ### SOLUTION LIGHT DISTRIBUTION ###
        #self.light_dist = np.zeros((self.width,self.height))
        #self.defineLight()

    def render_init(self):
        # init basic rendering surface
        if(self.config['rendering']== 1):
            if(self.width == pygame.display.Info().current_w and self.height == pygame.display.Info().current_h):   # fullscreen size
                self.displaySurface = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
            else:                                                                                                   # size smaller than fullscreen
                self.displaySurface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        elif(self.config['rendering'] == -1):
            self.displaySurface = pygame.display.set_mode((self.width, self.height), pygame.HIDDEN)                 # no screen
        elif(self.config['rendering'] == 0):
            self.displaySurface = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)                # black screen where capture images is possible


    @abstractmethod
    def add_static_rectangle_object(self):
       pass


    def add_dynamic_rectangle_object(self,rectangle):
        self.dynamicRectList.append(rectangle)

    def add_dynamic_line_object(self,line):
        self.dynamicLineList.append(line)

    @abstractmethod
    def add_static_circle_object(self):
        pass

    def add_dynamic_circle_object(self,circle):
        self.dynamicCircList.append(circle)

    @abstractmethod
    def set_background_color(self):
        self.displaySurface.fill(self.BACKGROUND_COLOR)

    def get_static_rect_list(self):
        return self.staticRectList
    def get_dynamic_rect_list(self):
        return self.dynamicRectList
    def get_static_circ_list(self):
        return self.staticCircList
    def get_dynamic_circ_list(self):
        return self.dynamicCircList
    def get_agent_object(self):
        return self.agent_object_list
    def get_dynamic_line_list(self):
        return self.dynamicLineList
    """
    def defineLight(self):
        center = np.array([self.width/2,self.height/2])
        
        light_dist = np.zeros((self.width,self.height,3))
        for i in range(self.width):
            for j in range(self.height):
                p = np.array([i,j])
                dist= int((1-np.linalg.norm((center-p)/self.width))*255)
                light_dist[i][j][0] = int(dist)
        #test = light_dist[:,:,0]
        #test = np.roll(test,+350,axis=1)
        #light_dist[:,:,0] = np.roll(test,+350,axis=0)
        #light_dist1 = light_dist
        light_dist1 =light_dist
        #print(light_dist[:,:,0])


        self.light_dist = light_dist1
        #print(np.min(self.light_dist))
    """


#%% Rendering and Helper functions
    def render(self):
        """
        This method is used to update the environment.
        """
        self.set_background_color()

        # draw static rects (items = sources, sinks, obstacles)
        for x in self.staticRectList:
            pygame.draw.rect(self.displaySurface, x[0], x[1], x[2])

        for x in self.staticCircList:
            pygame.draw.circle(self.displaySurface, x[0], x[1], x[2], x[3])

                      
        # draw dynamic polygons (agents)
        for x in self.dynamicPolyList:
            pygame.draw.polygon(self.displaySurface, (255,255,255), x[1]) # fill the polygon
            pygame.draw.polygon(self.displaySurface, x[0], x[1], 3)


        # draw dynamic circles (agent tokens)
        for x in self.dynamicCircList:
            agent = pygame.draw.circle(self.displaySurface, x[0], x[1], x[2], x[3])
            #print("test", agent)
            #self.agent_object_list.append(agent)

        for x in self.dynamicLineList:
            pygame.draw.line(self.displaySurface, x[0], x[1], x[2])

        for x in self.dynamicRectList:
            pygame.draw.rect(self.displaySurface, x[0], x[1], x[2])


        # reset dynamic buffers
        self.resetDynamicBuffers()                  

        # update content on display and enforce given frames per second
        pygame.display.flip()                       
        self.forceFramerate()       

    def resetDynamicBuffers(self):
        self.dynamicCircList = []
        self.dynamicPolyList = []
        self.dynamicLineList = []
        self.dynamicRectList = []
        
            

    def forceFramerate(self):
        """
        This method is used once per frame to enforce a fixed number of frames per second.
        It will delay the simulation to get the desired fps.
        """
        self.clock.tick(self.FPS)  # every second at most fps frames should pass.
        #self.clock.tick_busy_loop(fps)  # more accurate to ensure fps than tick but need more CPU computation power
        
        
        
        
        