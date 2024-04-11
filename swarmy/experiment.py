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
##from .agent import Agent

# =============================================================================
# Class
# =============================================================================
class Experiment():
    
    def __init__(self, config, agent_controller, agent_sensing, world, agent):
        super(Experiment, self).__init__()

        self.config = config
        self.agent_controller = agent_controller
        self.agent_sensing = agent_sensing
        self.world = world(config)
        self.agent = agent
        



        
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
        environment = self.world
        environment.render_init()

        # instatiate agent
        agentList = []
        agent_counter = 0
        controller_counter = 0
        while agent_counter <self.config['number_of_agents']:
            if agent_counter/self.config['number_of_agents'] >= self.config['controller_1']:
                controller_counter = 1
            newAgent = self.agent(environment,self.agent_controller[controller_counter],self.agent_sensing, self.config)
            newAgent.initial_position()
            newAgent.unique_id = agent_counter
            agentList.append(newAgent)
            agent_counter +=1
        environment.agentlist = agentList
        # -----------------------------------------------------------------------------
        # initializations
        if agentList:
            agentList[0].body.helperLUT()    # global lookup table needs to be calculated only once

        # =============================================================================
        # Run experiment: Loop-Processing
        # =============================================================================
        while running and timesteps_counter < self.config["max_timestep"]:
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
            for agent in agentList:
                environment.agent_object_list.append(
                    pygame.Rect(agent.actuation.position[0] - 15, agent.actuation.position[1] - 15, 30, 30))
            # update agents
            for newAgent in agentList:
                newAgent.processing.perform(pressedKeys)
                #pygame.Rect(5, self.config['world_height'] - 10, self.config['world_width'] - 10, 5)


            # display results
            if(rendering == 1):
                for newAgent in agentList:
                    newAgent.body.render()         # update agent bod
                environment.render()           # update content on display

            environment.agent_object_list = []
        if self.config['save_trajectory']:
            for i,agent in enumerate(agentList):
                if i == len(agentList)-1:
                    agent.save_information(True)
                else:
                    agent.save_information(False)


        print('Experiment finished by manual stopping or maximum timesteps reached. Check config.yaml to increase the maximum timesteps.')
        pygame.quit()
        return None
