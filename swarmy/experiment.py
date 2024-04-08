# =============================================================================
# created by:   Samer Al-Magazachi
# created on:   18/02/2021 -- 13/04/2022
# modified by: Eduard Buss  (17.03.2023)
# version:      0.9
# status:       prototype
# =============================================================================
"""
Description:
In this module one specific experiment can be executed.
The module initilizes pygame.
The parameters for the simulation are:
    - simulation speed
    - maximum agent speed
    - number of obstacles
"""

# =============================================================================
# Imports
# =============================================================================
import pygame
import random
import sys
sys.path.insert(0, '..')  # add parent directory to path
# import internal object classes
#from .environment import Environment
#from world.my_world import my_environment
##from .item import Obstacle
from .agent import Agent

# =============================================================================
# Class
# =============================================================================
class Experiment():
    
    def __init__(self, config, agent_controller, agent_sensing, world):
        super(Experiment, self).__init__()

        self.config = config
        self.agent_controller = agent_controller
        self.agent_sensing = agent_sensing
        self.world = world
        



        
    def run(self, rendering):
        """
        Start swarm simulation expermiment
        
        Args:
            rendering               (int):   1 = show simulation; -1 = hide simulation; 0 = black screen (capture mode)           
        """
        # pygame presets
        pygame.init() 					        # initialize pygame
        running = True   				        # termination condition
            
        # tracking variable
        timesteps_counter = 0

        # -----------------------------------------------------------------------------
        # instantiations

        # instantiate environment
        #environment = my_environment(rendering, self.config)
        environment = self.world
        environment.render_init()

        # instatiate agent
        agentList = []
        agent_counter = 0
        controller_counter = 0
        sensing_counter = 0
        while agent_counter <self.config['number_of_agents']:
            x = random.randint(0, self.config['world_width']) ## self.agent_behavior['init_x_y_position']
            y = random.randint(0, self.config['world_height'])
            print(agent_counter/self.config['number_of_agents'])
            if agent_counter/self.config['number_of_agents'] >= self.config['controller_1']:
                print("test")
                controller_counter = 1
            agentList.append(Agent(environment,self.agent_controller[controller_counter],self.agent_sensing, self.config ))
            agent_counter +=1
        #newAgent = Agent(self.agent_behavior['init_x_y_position'], self.agent_behavior['init_direction'], environment, self.agent_behavior, self.config )
    
        # -----------------------------------------------------------------------------
        # initializations
        agentList[0].body.helperLUT()    # global lookup table needs to be calculated only once

        # =============================================================================
        # Run experiment: Loop-Processing
        # =============================================================================
        while running:
            timesteps_counter += 1        
            
            #-----------------------------------------------------------------------------
            # ASYNCHRON 
            
            # get the set of keys pressed and check for user input
            pressedKeys = pygame.key.get_pressed()
                       
            # handle user input
            for event in pygame.event.get():
                
                if event.type == pygame.KEYDOWN:    # Check for KEYDOWN event
                                    
                    # If the Esc key is pressed, then exit the main loop
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        
                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == pygame.QUIT:
                    running = False
     
            #-----------------------------------------------------------------------------
            # SYNCHRON         
     
            # update agents
            for newAgent in agentList:
                newAgent.processing.perform(pressedKeys)
            #### SOLUTION ### Torus
            #newAgent.actuation.position[0] = newAgent.actuation.position[0] % environment.width
            #newAgent.actuation.position[1] = newAgent.actuation.position[1] % environment.height

            # display results
            if(rendering == 1):
                for newAgent in agentList:
                    newAgent.body.render()         # update agent bod
                environment.render()           # update content on display

        pygame.quit()
        return None
